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
