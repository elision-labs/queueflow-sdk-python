"""Tests for the hand-written facade, not the generated core.

The generated api clients and models are covered by codegen and the spec drift
guard. What is worth asserting here is the ergonomics layered on top: DAG
validation that must fail before any round-trip, the config assembly in
create_job, the create-then-fetch pairing, and the polling loop that turns a
sequence of responses into a terminal record or a WaitTimeout.

The api clients are replaced with in-memory fakes, so the suite is offline and
runs in milliseconds. Stdlib unittest only, so it works under `pytest`, `tox`,
or plain `python -m unittest`.
"""

from __future__ import annotations

import unittest
from types import SimpleNamespace
from typing import Any, Dict, List, Optional

from queueflow.facade import (
    QueueFlow,
    WaitTimeout,
    WorkflowBuilder,
    WorkflowValidationError,
    wf,
)


def record(status: str, rid: str = "job-1") -> SimpleNamespace:
    """A stand-in for a Job/Workflow: the poll loop only reads `.status`."""
    return SimpleNamespace(id=rid, status=status)


class FakeJobsApi:
    """Records what the facade sends and replays a scripted status sequence."""

    def __init__(self, statuses: Optional[List[str]] = None) -> None:
        self.created: List[Any] = []
        self.idempotency_keys: List[Optional[str]] = []
        self.get_calls = 0
        self._statuses = statuses or ["completed"]

    def create_job(self, req: Any, idempotency_key: Optional[str] = None) -> Any:
        self.created.append(req)
        self.idempotency_keys.append(idempotency_key)
        return SimpleNamespace(job_id="job-1")

    def get_job(self, job_id: str) -> Any:
        idx = min(self.get_calls, len(self._statuses) - 1)
        self.get_calls += 1
        return record(self._statuses[idx], job_id)


class FakeWorkflowsApi:
    def __init__(self, statuses: Optional[List[str]] = None) -> None:
        self.created: List[Any] = []
        self.get_calls = 0
        self._statuses = statuses or ["completed"]

    def create_workflow(self, body: Any) -> Any:
        self.created.append(body)
        return SimpleNamespace(workflow_id="wf-1")

    def get_workflow(self, workflow_id: str) -> Any:
        idx = min(self.get_calls, len(self._statuses) - 1)
        self.get_calls += 1
        return record(self._statuses[idx], workflow_id)


def client(
    job_statuses: Optional[List[str]] = None,
    workflow_statuses: Optional[List[str]] = None,
) -> QueueFlow:
    """A real QueueFlow with its api clients swapped for fakes."""
    qf = QueueFlow("http://qf.test", "test-token")
    qf.jobs = FakeJobsApi(job_statuses)
    qf.workflows = FakeWorkflowsApi(workflow_statuses)
    return qf


class TestWorkflowBuilderValidation(unittest.TestCase):
    """A structurally invalid DAG must never reach the network."""

    def test_empty_name_is_rejected_at_construction(self) -> None:
        with self.assertRaises(WorkflowValidationError):
            WorkflowBuilder("")

    def test_no_steps(self) -> None:
        with self.assertRaisesRegex(WorkflowValidationError, "has no steps"):
            wf("etl").build()

    def test_duplicate_step_name(self) -> None:
        builder = wf("etl").step("a", "task").step("a", "other")
        with self.assertRaisesRegex(WorkflowValidationError, 'duplicate step name "a"'):
            builder.build()

    def test_dangling_dependency(self) -> None:
        builder = wf("etl").step("a", "task", after=["ghost"])
        with self.assertRaisesRegex(WorkflowValidationError, 'unknown step "ghost"'):
            builder.build()

    def test_self_cycle(self) -> None:
        builder = wf("etl").step("a", "task", after=["a"])
        with self.assertRaisesRegex(WorkflowValidationError, "dependency cycle"):
            builder.build()

    def test_direct_cycle(self) -> None:
        builder = wf("etl").step("a", "task", after=["b"]).step("b", "task", after=["a"])
        with self.assertRaisesRegex(WorkflowValidationError, "dependency cycle"):
            builder.build()

    def test_long_cycle(self) -> None:
        builder = (
            wf("etl")
            .step("a", "task", after=["c"])
            .step("b", "task", after=["a"])
            .step("c", "task", after=["b"])
        )
        with self.assertRaisesRegex(WorkflowValidationError, "dependency cycle"):
            builder.build()

    def test_diamond_is_valid(self) -> None:
        # `load` is reachable by two paths; a checker that confuses "visited"
        # with "currently visiting" would wrongly call this a cycle.
        body = (
            wf("etl")
            .step("extract", "fetch")
            .step("left", "normalize", after=["extract"])
            .step("right", "enrich", after=["extract"])
            .step("load", "upsert", after=["left", "right"])
            .build()
        )
        self.assertEqual(body.name, "etl")
        self.assertEqual(len(body.steps), 4)
        self.assertEqual(body.steps[3].depends_on, ["left", "right"])

    def test_context_accumulates_across_calls(self) -> None:
        body = wf("etl").step("a", "task").context(run="2026-06-07").context(tenant="acme").build()
        self.assertEqual(body.context, {"run": "2026-06-07", "tenant": "acme"})

    def test_wf_is_a_workflow_builder(self) -> None:
        self.assertIsInstance(wf("etl"), WorkflowBuilder)


class TestCreateJob(unittest.TestCase):
    def test_creates_then_fetches_the_record(self) -> None:
        qf = client(job_statuses=["pending"])
        job = qf.create_job("echo", payload={"hi": 1})

        self.assertEqual(job.id, "job-1")
        self.assertEqual(len(qf.jobs.created), 1)
        self.assertEqual(qf.jobs.get_calls, 1, "must fetch the full record after creating")
        req = qf.jobs.created[0]
        self.assertEqual(req.task_name, "echo")
        self.assertEqual(req.payload, {"hi": 1})

    def test_payload_defaults_to_empty_dict(self) -> None:
        qf = client(job_statuses=["pending"])
        qf.create_job("echo")
        self.assertEqual(qf.jobs.created[0].payload, {})

    def test_no_config_is_built_when_no_options_are_given(self) -> None:
        # An empty JobConfigRequest would override server-side defaults with
        # nulls, so it must stay absent entirely.
        qf = client(job_statuses=["pending"])
        qf.create_job("echo")
        self.assertIsNone(qf.jobs.created[0].config)

    def test_config_is_assembled_from_options(self) -> None:
        qf = client(job_statuses=["pending"])
        qf.create_job("echo", priority=5, max_retries=2, timeout=30, queue="urgent")

        config = qf.jobs.created[0].config
        self.assertIsNotNone(config)
        self.assertEqual(config.priority, 5)
        self.assertEqual(config.max_retries, 2)
        self.assertEqual(config.timeout, 30)
        self.assertEqual(config.queue, "urgent")

    def test_a_single_option_still_builds_a_config(self) -> None:
        qf = client(job_statuses=["pending"])
        qf.create_job("echo", priority=5)
        self.assertIsNotNone(qf.jobs.created[0].config)

    def test_priority_zero_still_builds_a_config(self) -> None:
        # Guards against an `any(...)` truthiness check: priority=0 is a
        # meaningful value, not an absent one.
        qf = client(job_statuses=["pending"])
        qf.create_job("echo", priority=0)
        config = qf.jobs.created[0].config
        self.assertIsNotNone(config, "priority=0 must not be treated as unset")
        self.assertEqual(config.priority, 0)

    def test_idempotency_key_is_forwarded(self) -> None:
        qf = client(job_statuses=["pending"])
        qf.create_job("echo", idempotency_key="key-1")
        self.assertEqual(qf.jobs.idempotency_keys, ["key-1"])


class TestWaitForJob(unittest.TestCase):
    def test_polls_until_terminal(self) -> None:
        qf = client(job_statuses=["pending", "running", "completed"])
        job = qf.wait_for_job("job-1", timeout=5.0, interval=0.001)

        self.assertEqual(job.status, "completed")
        self.assertEqual(qf.jobs.get_calls, 3, "must stop at the first terminal status")

    def test_failed_and_cancelled_are_terminal(self) -> None:
        for status in ("failed", "cancelled"):
            with self.subTest(status=status):
                qf = client(job_statuses=[status])
                job = qf.wait_for_job("job-1", timeout=1.0, interval=0.001)
                self.assertEqual(job.status, status)

    def test_retrying_is_not_terminal_and_times_out(self) -> None:
        qf = client(job_statuses=["retrying"])
        with self.assertRaises(WaitTimeout):
            qf.wait_for_job("job-1", timeout=0.05, interval=0.01)

    def test_timeout_message_names_the_job(self) -> None:
        qf = client(job_statuses=["pending"])
        with self.assertRaisesRegex(WaitTimeout, "job job-1 did not finish"):
            qf.wait_for_job("job-1", timeout=0.05, interval=0.01)

    def test_wait_timeout_is_a_timeout_error(self) -> None:
        # Callers should be able to catch the stdlib type.
        self.assertTrue(issubclass(WaitTimeout, TimeoutError))


class TestWorkflows(unittest.TestCase):
    def test_create_workflow_validates_before_sending(self) -> None:
        qf = client()
        cyclic = wf("etl").step("a", "task", after=["b"]).step("b", "task", after=["a"])

        with self.assertRaises(WorkflowValidationError):
            qf.create_workflow(cyclic)
        self.assertEqual(qf.workflows.created, [], "no request for a locally-invalid DAG")

    def test_create_workflow_accepts_a_builder(self) -> None:
        qf = client(workflow_statuses=["created"])
        result = qf.create_workflow(wf("etl").step("a", "task"))

        self.assertEqual(result.id, "wf-1")
        self.assertEqual(len(qf.workflows.created), 1)
        self.assertEqual(qf.workflows.get_calls, 1)

    def test_create_workflow_accepts_a_prebuilt_request(self) -> None:
        qf = client(workflow_statuses=["created"])
        body = wf("etl").step("a", "task").build()
        qf.create_workflow(body)
        self.assertIs(qf.workflows.created[0], body)

    def test_partially_failed_is_terminal_for_a_workflow(self) -> None:
        # Terminal for workflows but with no job equivalent, so it is the case
        # most easily missed in the terminal set.
        qf = client(workflow_statuses=["partially_failed"])
        result = qf.wait_for_workflow("wf-1", timeout=1.0, interval=0.001)
        self.assertEqual(result.status, "partially_failed")

    def test_running_workflow_times_out(self) -> None:
        qf = client(workflow_statuses=["running"])
        with self.assertRaises(WaitTimeout):
            qf.wait_for_workflow("wf-1", timeout=0.05, interval=0.01)


if __name__ == "__main__":
    unittest.main()


# --- worker runtime ----------------------------------------------------------

import threading
import time as _time

from queueflow.exceptions import ApiException
from queueflow.facade import NonRetryableError


def lease(task: str = "echo", job_id: str = "j1", token: str = "tok-1") -> SimpleNamespace:
    return SimpleNamespace(
        job=SimpleNamespace(id=job_id, task_name=task, payload={}), lease_token=token
    )


class FakeWorkerApi:
    """Serves a scripted list of leases, then sets `stop` so run_worker exits."""

    def __init__(
        self,
        leases: Optional[List[SimpleNamespace]] = None,
        heartbeat_status: str = "running",
        lease_error: Optional[Exception] = None,
        complete_error: Optional[Exception] = None,
        block_on_empty: bool = False,
        stop_on_empty: bool = True,
    ) -> None:
        self.pending = list(leases or [])
        self.heartbeat_status = heartbeat_status
        self.lease_error = lease_error
        self.complete_error = complete_error
        # Emulate the server's long poll (which urllib3 cannot interrupt):
        # sleep for the requested wait_secs when the queue is empty.
        self.block_on_empty = block_on_empty
        self.stop_on_empty = stop_on_empty
        self.completes: List[Any] = []
        self.fails: List[Any] = []
        self.heartbeats = 0
        self.lease_requests: List[Any] = []
        self.lease_timeouts: List[Any] = []
        self.stop = threading.Event()

    def lease_jobs(self, queue: str, req: Any, _request_timeout: Any = None) -> Any:
        self.lease_requests.append(req)
        self.lease_timeouts.append(_request_timeout)
        if self.lease_error is not None:
            err, self.lease_error = self.lease_error, None
            raise err
        if not self.pending:
            if self.stop_on_empty:
                self.stop.set()
            if self.block_on_empty:
                _time.sleep(req.wait_secs or 0)
            return SimpleNamespace(jobs=[])
        take = min(req.max_jobs or 1, len(self.pending))
        leased, self.pending = self.pending[:take], self.pending[take:]
        return SimpleNamespace(jobs=leased)

    def heartbeat_job(self, job_id: str, req: Any) -> Any:
        self.heartbeats += 1
        return SimpleNamespace(status=self.heartbeat_status)

    def complete_job(self, job_id: str, req: Any) -> None:
        if self.complete_error is not None:
            raise self.complete_error
        self.completes.append((job_id, req))

    def fail_job(self, job_id: str, req: Any) -> None:
        self.fails.append((job_id, req))


def worker_client(api: FakeWorkerApi) -> QueueFlow:
    qf = QueueFlow("http://qf.test", "test-token")
    qf.worker = api
    return qf


class TestWorkerRuntime(unittest.TestCase):
    def run_until_drained(self, api: FakeWorkerApi, handlers: Dict[str, Any], **kw: Any) -> None:
        worker_client(api).run_worker("q", handlers, stop=api.stop, wait_secs=0, **kw)

    def test_happy_path_completes_with_the_handler_result(self) -> None:
        api = FakeWorkerApi([lease()])
        self.run_until_drained(api, {"echo": lambda job: {"ok": job.id}})
        self.assertEqual(len(api.completes), 1)
        job_id, req = api.completes[0]
        self.assertEqual(job_id, "j1")
        self.assertEqual(req.lease_token, "tok-1")
        self.assertEqual(req.result, {"ok": "j1"})
        self.assertEqual(api.fails, [])

    def test_none_result_becomes_an_empty_dict(self) -> None:
        api = FakeWorkerApi([lease()])
        self.run_until_drained(api, {"echo": lambda job: None})
        self.assertEqual(api.completes[0][1].result, {})

    def test_a_raising_handler_fails_retryably(self) -> None:
        def boom(job):
            raise RuntimeError("gateway 503")

        api = FakeWorkerApi([lease()])
        self.run_until_drained(api, {"echo": boom})
        self.assertEqual(api.completes, [])
        _, req = api.fails[0]
        self.assertIn("gateway 503", req.error)
        self.assertNotEqual(req.retryable, False)

    def test_non_retryable_error_dead_letters(self) -> None:
        def reject(job):
            raise NonRetryableError("fraud")

        api = FakeWorkerApi([lease()])
        self.run_until_drained(api, {"echo": reject})
        _, req = api.fails[0]
        self.assertEqual(req.retryable, False)

    def test_unknown_task_fails_non_retryably(self) -> None:
        api = FakeWorkerApi([lease(task="ghost")])
        self.run_until_drained(api, {"echo": lambda job: {}})
        _, req = api.fails[0]
        self.assertEqual(req.retryable, False)
        self.assertIn("ghost", req.error)

    def test_auth_errors_raise_instead_of_spinning(self) -> None:
        api = FakeWorkerApi(lease_error=ApiException(status=403, reason="forbidden"))
        with self.assertRaises(ApiException):
            self.run_until_drained(api, {})

    def test_transient_lease_errors_back_off_and_continue(self) -> None:
        api = FakeWorkerApi([lease()], lease_error=RuntimeError("connection reset"))
        seen: List[Exception] = []
        self.run_until_drained(api, {"echo": lambda job: {}}, on_error=seen.append)
        self.assertEqual(len(seen), 1)
        self.assertEqual(len(api.completes), 1)

    def test_two_argument_handlers_receive_a_context(self) -> None:
        contexts: List[Any] = []

        def handler(job, ctx):
            contexts.append(ctx)
            return {}

        api = FakeWorkerApi([lease()])
        self.run_until_drained(api, {"echo": handler})
        self.assertEqual(len(contexts), 1)
        self.assertFalse(contexts[0].cancelled)

    def test_lost_lease_abandons_reporting_and_cancels_the_context(self) -> None:
        observed = {"cancelled_seen": False}

        def slow(job, ctx):
            # Outlive one 1s heartbeat tick (lease_secs=2); the fake reports
            # the job cancelled, which must flip ctx.cancelled.
            deadline = _time.monotonic() + 4.0
            while _time.monotonic() < deadline:
                if ctx.cancelled:
                    observed["cancelled_seen"] = True
                    return {}
                _time.sleep(0.05)
            return {}

        api = FakeWorkerApi([lease()], heartbeat_status="cancelled")
        self.run_until_drained(api, {"echo": slow}, lease_secs=2)
        self.assertTrue(observed["cancelled_seen"])
        self.assertGreaterEqual(api.heartbeats, 1)
        self.assertEqual(api.completes, [])
        self.assertEqual(api.fails, [])

    def test_a_failed_report_is_never_converted_into_a_job_failure(self) -> None:
        api = FakeWorkerApi([lease()], complete_error=RuntimeError("engine restarting"))
        self.run_until_drained(api, {"echo": lambda job: {"ok": True}})
        self.assertEqual(api.fails, [])  # lease expiry redelivers; no fail() call


class TestWorkerConcurrency(unittest.TestCase):
    def run_until_drained(self, api: FakeWorkerApi, handlers: Dict[str, Any], **kw: Any) -> Any:
        return worker_client(api).run_worker("q", handlers, stop=api.stop, wait_secs=0, **kw)

    def test_default_concurrency_is_one_job_per_lease(self) -> None:
        api = FakeWorkerApi([lease(job_id="j1"), lease(job_id="j2")])
        self.run_until_drained(api, {"echo": lambda job: {}})
        self.assertEqual([r.max_jobs for r in api.lease_requests[:2]], [1, 1])
        self.assertEqual(len(api.completes), 2)

    def test_handlers_run_in_parallel_up_to_concurrency(self) -> None:
        # A barrier of 3 only passes if three handlers run at the same time.
        barrier = threading.Barrier(3, timeout=5.0)

        def handler(job: Any) -> Dict[str, Any]:
            barrier.wait()
            return {"id": job.id}

        api = FakeWorkerApi([lease(job_id=f"j{i}") for i in range(3)])
        result = self.run_until_drained(api, {"echo": handler}, concurrency=3)

        self.assertEqual(api.lease_requests[0].max_jobs, 3, "lease asks for every free slot")
        self.assertEqual(sorted(req.result["id"] for _, req in api.completes), ["j0", "j1", "j2"])
        self.assertEqual(result.unfinished, [])

    def test_in_flight_never_exceeds_concurrency(self) -> None:
        active = {"now": 0, "max": 0}
        guard = threading.Lock()

        def handler(job: Any) -> Dict[str, Any]:
            with guard:
                active["now"] += 1
                active["max"] = max(active["max"], active["now"])
            _time.sleep(0.05)
            with guard:
                active["now"] -= 1
            return {}

        api = FakeWorkerApi([lease(job_id=f"j{i}") for i in range(6)])
        self.run_until_drained(api, {"echo": handler}, concurrency=2)

        self.assertEqual(active["max"], 2, "concurrency cap exceeded")
        self.assertEqual(len(api.completes), 6)
        self.assertTrue(all(r.max_jobs <= 2 for r in api.lease_requests))

    def test_lease_asks_only_for_free_slots(self) -> None:
        # Two jobs leased into two slots; the second lease (after one job
        # finishes while the other still runs) must ask for a single job.
        release = threading.Event()
        started = threading.Event()

        def handler(job: Any) -> Dict[str, Any]:
            if job.id == "slow":
                started.set()
                release.wait(5.0)
            return {}

        api = FakeWorkerApi([lease(job_id="slow"), lease(job_id="quick"), lease(job_id="third")])
        api.stop_on_empty = False
        api.block_on_empty = True
        worker = threading.Thread(
            target=lambda: self.run_until_drained(api, {"echo": handler}, concurrency=2, poll_wait_secs=0),
            daemon=True,
        )
        worker.start()
        self.assertTrue(started.wait(5.0))
        deadline = _time.monotonic() + 5.0
        while len(api.completes) < 2 and _time.monotonic() < deadline:
            _time.sleep(0.01)
        self.assertEqual(len(api.completes), 2, "quick and third should have finished")
        self.assertEqual(api.lease_requests[0].max_jobs, 2)
        self.assertEqual(api.lease_requests[1].max_jobs, 1, "one slot is still busy")
        release.set()
        api.stop.set()
        worker.join(10.0)
        self.assertFalse(worker.is_alive())
        self.assertEqual(len(api.completes), 3)

    def test_concurrency_below_one_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            worker_client(FakeWorkerApi()).run_worker("q", {}, concurrency=0)


class TestWorkerStop(unittest.TestCase):
    def test_wait_secs_is_capped_by_poll_wait_secs_when_stop_is_given(self) -> None:
        api = FakeWorkerApi()
        worker_client(api).run_worker("q", {}, stop=api.stop, wait_secs=20, poll_wait_secs=5)
        self.assertEqual(api.lease_requests[0].wait_secs, 5)
        # The request timeout follows the effective wait, not the client default.
        self.assertEqual(api.lease_timeouts[0], 40.0)

    def test_poll_wait_secs_never_raises_wait_secs(self) -> None:
        api = FakeWorkerApi()
        worker_client(api).run_worker("q", {}, stop=api.stop, wait_secs=2, poll_wait_secs=5)
        self.assertEqual(api.lease_requests[0].wait_secs, 2)
        self.assertEqual(api.lease_timeouts[0], 37.0)

    def test_stop_latency_is_bounded_by_poll_wait_secs(self) -> None:
        # The fake sleeps out the full wait like a real long poll; stop must
        # still take effect within about one poll_wait_secs, not wait_secs.
        api = FakeWorkerApi(block_on_empty=True, stop_on_empty=False)
        worker = threading.Thread(
            target=worker_client(api).run_worker,
            args=("q", {}),
            kwargs={"stop": api.stop, "wait_secs": 20, "poll_wait_secs": 1},
            daemon=True,
        )
        worker.start()
        _time.sleep(0.1)
        t0 = _time.monotonic()
        api.stop.set()
        worker.join(5.0)
        self.assertFalse(worker.is_alive(), "worker did not stop")
        self.assertLess(_time.monotonic() - t0, 2.0)

    def test_stop_drains_in_flight_handlers_and_reports_them(self) -> None:
        started = threading.Event()
        release = threading.Event()

        def handler(job: Any) -> Dict[str, Any]:
            started.set()
            release.wait(5.0)
            return {"ok": True}

        # With one slot and one job in flight no further lease happens, so the
        # test asks for the stop itself once the handler is running.
        api = FakeWorkerApi([lease()])
        results: List[Any] = []
        worker = threading.Thread(
            target=lambda: results.append(
                worker_client(api).run_worker("q", {"echo": handler}, stop=api.stop, wait_secs=0)
            ),
            daemon=True,
        )
        worker.start()
        self.assertTrue(started.wait(5.0))
        api.stop.set()
        _time.sleep(0.1)
        self.assertTrue(worker.is_alive(), "must keep draining while the handler runs")
        self.assertEqual(api.completes, [])
        release.set()
        worker.join(5.0)
        self.assertFalse(worker.is_alive())
        self.assertEqual(results[0].unfinished, [])
        self.assertEqual(len(api.completes), 1)
        self.assertEqual(api.completes[0][1].result, {"ok": True})

    def test_drain_timeout_abandons_slow_handlers_and_reports_them(self) -> None:
        seen: Dict[str, Any] = {}

        def handler(job: Any, ctx: Any) -> Dict[str, Any]:
            seen["ctx"] = ctx
            api.stop.set()  # stop arrives while this handler is still running
            deadline = _time.monotonic() + 5.0
            while not ctx.cancelled and _time.monotonic() < deadline:
                _time.sleep(0.01)
            seen["cancelled"] = ctx.cancelled
            return {"late": True}

        api = FakeWorkerApi([lease(job_id="slow")])
        t0 = _time.monotonic()
        result = worker_client(api).run_worker(
            "q", {"echo": handler}, stop=api.stop, wait_secs=0, drain_timeout=0.2
        )
        self.assertLess(_time.monotonic() - t0, 3.0, "drain must give up after drain_timeout")
        self.assertEqual([j.id for j in result.unfinished], ["slow"])
        self.assertTrue(seen["ctx"].cancelled, "an abandoned handler's ctx.cancelled must flip")
        # Let the abandoned handler notice and return: its outcome must not be reported.
        deadline = _time.monotonic() + 2.0
        while "cancelled" not in seen and _time.monotonic() < deadline:
            _time.sleep(0.01)
        self.assertEqual(api.completes, [])
        self.assertEqual(api.fails, [])

    def test_auth_errors_still_raise_after_draining(self) -> None:
        api = FakeWorkerApi(lease_error=ApiException(status=401, reason="unauthorized"))
        with self.assertRaises(ApiException):
            worker_client(api).run_worker("q", {}, stop=api.stop, wait_secs=0)


class TestTimeouts(unittest.TestCase):
    class FakeRest:
        def __init__(self) -> None:
            self.calls: List[Dict[str, Any]] = []

        def request(self, method: str, url: str, headers: Any = None, body: Any = None,
                    post_params: Any = None, _request_timeout: Any = None) -> Any:
            self.calls.append({"method": method, "url": url, "_request_timeout": _request_timeout})
            return SimpleNamespace(status=200, reason="OK", data=b"{}")

    def test_default_request_timeout_is_30s(self) -> None:
        qf = QueueFlow("http://qf.test", "t")
        self.assertEqual(qf.timeout, 30.0)
        rest = self.FakeRest()
        qf._client.rest_client = rest
        qf._client.call_api("GET", "http://qf.test/health")
        self.assertEqual(rest.calls[0]["_request_timeout"], 30.0)

    def test_explicit_per_call_timeout_wins(self) -> None:
        qf = QueueFlow("http://qf.test", "t")
        rest = self.FakeRest()
        qf._client.rest_client = rest
        qf._client.call_api("GET", "http://qf.test/health", _request_timeout=7.0)
        self.assertEqual(rest.calls[0]["_request_timeout"], 7.0)

    def test_client_timeout_is_configurable_and_applies_to_the_worker_client(self) -> None:
        qf = QueueFlow("http://qf.test", "t", worker_token="w", timeout=(3.0, 90.0))
        self.assertEqual(qf._client.default_timeout, (3.0, 90.0))
        self.assertIsNotNone(qf._worker_client)
        self.assertEqual(qf._worker_client.default_timeout, (3.0, 90.0))

    def test_timeout_none_disables_the_default(self) -> None:
        qf = QueueFlow("http://qf.test", "t", timeout=None)
        rest = self.FakeRest()
        qf._client.rest_client = rest
        qf._client.call_api("GET", "http://qf.test/health")
        self.assertIsNone(rest.calls[0]["_request_timeout"])


class TestQueues(unittest.TestCase):
    def test_queues_unwraps_the_response(self) -> None:
        qf = QueueFlow("http://qf.test", "t")
        stats = SimpleNamespace(queue="default", pending=2, scheduled=0, running=1, oldest_pending_age_secs=7)
        qf.system = SimpleNamespace(list_queues=lambda: SimpleNamespace(queues=[stats]))
        self.assertEqual(qf.queues(), [stats])


# --- 0.5.0 server operations: bulk cancel, bulk replay, queue control, whoami

import inspect as _inspect

from queueflow.api.dlq_api import DlqApi
from queueflow.api.jobs_api import JobsApi
from queueflow.models.cancel_jobs_request import CancelJobsRequest
from queueflow.models.replay_dead_letters_request import ReplayDeadLettersRequest


class FakeBulkJobsApi:
    def __init__(self, cancelled: int = 0) -> None:
        self.requests: List[Any] = []
        self.cancelled = cancelled

    def cancel_jobs(self, req: Any) -> Any:
        self.requests.append(req)
        return SimpleNamespace(cancelled=self.cancelled)


class FakeBulkDlqApi:
    def __init__(self, results: Optional[List[Any]] = None) -> None:
        self.requests: List[Any] = []
        self.results = results or []

    def replay_dead_letters(self, req: Any) -> Any:
        self.requests.append(req)
        return SimpleNamespace(results=self.results, replayed=len(self.results))


class FakeSystemApi:
    def __init__(self) -> None:
        self.paused: List[str] = []
        self.resumed: List[str] = []

    def pause_queue(self, queue: str) -> Any:
        self.paused.append(queue)
        return SimpleNamespace(queue=queue, paused=True, running=1, pending=3)

    def resume_queue(self, queue: str) -> Any:
        self.resumed.append(queue)
        return SimpleNamespace(queue=queue, paused=False, running=1, pending=3)

    def who_am_i(self) -> Any:
        return SimpleNamespace(tenant="tenant1", access="read_write")


class TestCancelJobs(unittest.TestCase):
    def test_returns_the_cancelled_count(self) -> None:
        qf = QueueFlow("http://qf.test", "t")
        qf.jobs = FakeBulkJobsApi(cancelled=7)
        self.assertEqual(qf.cancel_jobs(queue="orders"), 7)

    def test_sends_a_real_request_model_with_every_filter(self) -> None:
        qf = QueueFlow("http://qf.test", "t")
        qf.jobs = FakeBulkJobsApi()
        qf.cancel_jobs(
            queue="orders",
            task_name="send_email",
            status="pending",
            created_after="2026-01-01T00:00:00Z",
            created_before="2026-02-01T00:00:00Z",
            limit=25,
        )
        req = qf.jobs.requests[0]
        self.assertIsInstance(req, CancelJobsRequest)
        self.assertEqual(req.queue, "orders")
        self.assertEqual(req.task_name, "send_email")
        self.assertEqual(req.status, "pending")
        self.assertEqual(req.limit, 25)
        self.assertIsNotNone(req.created_after)
        self.assertIsNotNone(req.created_before)

    def test_no_filters_sends_no_values(self) -> None:
        # Absent filters carry no value, so the server applies its own
        # defaults (every non-terminal status, limit 100).
        qf = QueueFlow("http://qf.test", "t")
        qf.jobs = FakeBulkJobsApi()
        qf.cancel_jobs()
        self.assertTrue(all(v is None for v in qf.jobs.requests[0].to_dict().values()))

    def test_limit_zero_is_forwarded_not_dropped(self) -> None:
        qf = QueueFlow("http://qf.test", "t")
        qf.jobs = FakeBulkJobsApi()
        qf.cancel_jobs(limit=0)
        self.assertEqual(qf.jobs.requests[0].limit, 0)


class TestReplayDeadLetters(unittest.TestCase):
    def test_unwraps_the_results_list(self) -> None:
        results = [
            SimpleNamespace(dead_letter_id=1, job_id="job-9", error=None),
            SimpleNamespace(dead_letter_id=2, job_id=None, error="original job purged"),
        ]
        qf = QueueFlow("http://qf.test", "t")
        qf.dlq = FakeBulkDlqApi(results)
        self.assertEqual(qf.replay_dead_letters(queue="orders"), results)

    def test_sends_a_real_request_model_with_every_filter(self) -> None:
        qf = QueueFlow("http://qf.test", "t")
        qf.dlq = FakeBulkDlqApi()
        qf.replay_dead_letters(
            queue="orders",
            task_name="send_email",
            created_after="2026-01-01T00:00:00Z",
            created_before="2026-02-01T00:00:00Z",
            limit=10,
        )
        req = qf.dlq.requests[0]
        self.assertIsInstance(req, ReplayDeadLettersRequest)
        self.assertEqual(req.queue, "orders")
        self.assertEqual(req.task_name, "send_email")
        self.assertEqual(req.limit, 10)
        self.assertIsNotNone(req.created_after)
        self.assertIsNotNone(req.created_before)

    def test_no_filters_sends_no_values(self) -> None:
        qf = QueueFlow("http://qf.test", "t")
        qf.dlq = FakeBulkDlqApi()
        self.assertEqual(qf.replay_dead_letters(), [])
        self.assertTrue(all(v is None for v in qf.dlq.requests[0].to_dict().values()))


class TestQueueControlAndWhoAmI(unittest.TestCase):
    def test_pause_queue_forwards_the_name_and_returns_the_response(self) -> None:
        qf = QueueFlow("http://qf.test", "t")
        qf.system = FakeSystemApi()
        resp = qf.pause_queue("orders")
        self.assertEqual(qf.system.paused, ["orders"])
        self.assertTrue(resp.paused)
        self.assertEqual((resp.queue, resp.running, resp.pending), ("orders", 1, 3))

    def test_resume_queue_forwards_the_name_and_returns_the_response(self) -> None:
        qf = QueueFlow("http://qf.test", "t")
        qf.system = FakeSystemApi()
        resp = qf.resume_queue("orders")
        self.assertEqual(qf.system.resumed, ["orders"])
        self.assertFalse(resp.paused)

    def test_whoami_returns_tenant_and_access(self) -> None:
        qf = QueueFlow("http://qf.test", "t")
        qf.system = FakeSystemApi()
        me = qf.whoami()
        self.assertEqual((me.tenant, me.access), ("tenant1", "read_write"))


class TestListFilters(unittest.TestCase):
    """The README documents these generated list parameters; guard against drift."""

    def test_list_jobs_accepts_task_name(self) -> None:
        self.assertIn("task_name", _inspect.signature(JobsApi.list_jobs).parameters)

    def test_list_dead_letters_accepts_task_name_and_replayed(self) -> None:
        params = _inspect.signature(DlqApi.list_dead_letters).parameters
        self.assertIn("task_name", params)
        self.assertIn("replayed", params)
