"""Live conformance tests: run the facade against a REAL QueueFlow server.

Skipped unless QUEUEFLOW_URL is set. The server must run in ``--mode all``
with the built-in ``echo`` handler registered (the default ``queueflow serve``).

    QUEUEFLOW_URL           base URL, e.g. http://localhost:8000
    QUEUEFLOW_TOKEN         tenant bearer token (default "dev")
    QUEUEFLOW_WORKER_TOKEN  worker-protocol token (defaults to QUEUEFLOW_TOKEN,
                            which only works when the server has no --worker-token)

Run with ``pytest -m live`` (the marker is registered in pyproject.toml) or
``pytest test/test_live.py``. Plain ``pytest`` collects these too, but they skip
themselves, so CI stays offline.
"""

from __future__ import annotations

import os
import secrets
import threading
import time
from typing import Any, Dict, List

import pytest

from queueflow.exceptions import BadRequestException, NotFoundException
from queueflow.facade import NonRetryableError, QueueFlow, wf
from queueflow.models.lease_jobs_request import LeaseJobsRequest
from queueflow.models.complete_job_request import CompleteJobRequest

URL = os.environ.get("QUEUEFLOW_URL")
TOKEN = os.environ.get("QUEUEFLOW_TOKEN", "dev")
WORKER_TOKEN = os.environ.get("QUEUEFLOW_WORKER_TOKEN", TOKEN)

pytestmark = [
    pytest.mark.live,
    pytest.mark.skipif(not URL, reason="QUEUEFLOW_URL is not set"),
]

WAIT_SECS = 60.0
POLL_SECS = 0.25


@pytest.fixture(scope="module")
def qf() -> QueueFlow:
    assert URL is not None
    return QueueFlow(URL, TOKEN, worker_token=WORKER_TOKEN)


@pytest.fixture(scope="module")
def suffix() -> str:
    return f"{int(time.time()):x}-{secrets.token_hex(3)}"


def test_server_reachable_and_echo_registered(qf: QueueFlow) -> None:
    assert qf.health_api.get_health() is not None
    tasks = qf.system.list_tasks().tasks
    assert "echo" in tasks, f"echo handler not registered: {tasks}"


def test_echo_job_completes_and_echoes_payload(qf: QueueFlow, suffix: str) -> None:
    payload = {"hello": "world", "n": 42, "nested": {"ok": True}}
    key = f"sdk-live-{suffix}"

    created = qf.create_job("echo", payload=payload, idempotency_key=key)
    assert created.task_name == "echo"
    assert created.idempotency_key == key

    fetched = qf.jobs.get_job(created.id)
    assert fetched.id == created.id

    done = qf.wait_for_job(created.id, timeout=WAIT_SECS, interval=POLL_SECS)
    assert done.status == "completed", f"error: {done.error_message}"
    # The built-in echo handler returns the payload plus ``echoed: true``.
    assert done.result == {**payload, "echoed": True}

    # Re-submitting the same idempotency key returns the original job.
    again = qf.create_job("echo", payload=payload, idempotency_key=key)
    assert again.id == created.id


def test_two_step_echo_workflow_completes(qf: QueueFlow, suffix: str) -> None:
    dag = (
        wf(f"sdk-live-wf-{suffix}")
        .step("first", "echo", payload={"step": 1})
        .step("second", "echo", after=["first"], payload={"step": 2})
    )
    workflow = qf.create_workflow(dag)
    assert len(workflow.steps) == 2

    finished = qf.wait_for_workflow(workflow.id, timeout=WAIT_SECS, interval=POLL_SECS)
    assert finished.status == "completed"

    steps = qf.workflows.get_workflow_step_states(workflow.id).steps
    assert len(steps) == 2
    for step in steps:
        assert step.status == "completed", step.name


def test_cron_create_list_pause_resume_delete(qf: QueueFlow, suffix: str) -> None:
    name = f"sdk-live-cron-{suffix}"
    # Fires once a year; the schedule never triggers during the test.
    cron_id = qf.create_cron(name, "0 0 1 1 *", "echo", payload={"from": "cron"})

    cron = qf.cron.get_cron(cron_id)
    assert cron.name == name
    assert cron.enabled is True

    listed = qf.cron.list_crons(limit=100).crons
    assert any(c.id == cron_id for c in listed), "new cron missing from list"

    qf.cron.pause_cron(cron_id)
    assert qf.cron.get_cron(cron_id).enabled is False

    qf.cron.resume_cron(cron_id)
    assert qf.cron.get_cron(cron_id).enabled is True

    qf.cron.delete_cron(cron_id)
    with pytest.raises(NotFoundException):
        qf.cron.get_cron(cron_id)


def test_dead_letter_list_and_stats(qf: QueueFlow) -> None:
    dlq = qf.dlq.list_dead_letters(limit=10)
    assert isinstance(dlq.dead_letters, list)
    assert isinstance(dlq.has_more, bool)

    stats = qf.system.get_stats()
    assert isinstance(stats.jobs_created, int)
    assert stats.jobs_created >= 1, "this module created at least one job"


def test_worker_runtime_completes_job_on_dedicated_queue(qf: QueueFlow, suffix: str) -> None:
    # A queue the server's in-process workers never poll, and a task name only
    # this test's worker knows, so the job can only be completed by run_worker.
    queue = f"sdk-live-q-{suffix}"
    task = f"sdk-live-task-{suffix}"
    payload = {"order": 7}

    job = qf.create_job(task, payload=payload, queue=queue)
    assert job.queue_name == queue
    assert job.status == "pending"

    handled: List[str] = []
    stop = threading.Event()

    def handler(leased: Any) -> Dict[str, Any]:
        handled.append(leased.id)
        # Stop after this job is reported: run_worker checks ``stop`` between leases.
        stop.set()
        return {**(leased.payload or {}), "handled": True}

    worker = threading.Thread(
        target=qf.run_worker,
        args=(queue, {task: handler}),
        kwargs={"lease_secs": 10, "wait_secs": 2, "stop": stop},
        daemon=True,
    )
    worker.start()
    try:
        done = qf.wait_for_job(job.id, timeout=WAIT_SECS, interval=POLL_SECS)
    finally:
        stop.set()
        worker.join(timeout=30)

    assert not worker.is_alive(), "worker loop did not stop"
    assert handled == [job.id]
    assert done.status == "completed", f"error: {done.error_message}"
    assert done.result == {**payload, "handled": True}


def test_worker_runtime_runs_jobs_concurrently_up_to_the_cap(qf: QueueFlow, suffix: str) -> None:
    queue = f"sdk-live-cq-{suffix}"
    task = f"sdk-live-ctask-{suffix}"
    count = 4

    jobs = [qf.create_job(task, payload={"i": i}, queue=queue) for i in range(count)]

    active = {"now": 0, "max": 0}
    guard = threading.Lock()
    started: List[str] = []
    stop = threading.Event()
    results: List[Any] = []

    def handler(leased: Any) -> Dict[str, Any]:
        with guard:
            active["now"] += 1
            active["max"] = max(active["max"], active["now"])
            started.append(leased.id)
        # Long enough that the four leases overlap in time.
        time.sleep(0.75)
        with guard:
            active["now"] -= 1
        return {**(leased.payload or {}), "handled": True}

    worker = threading.Thread(
        target=lambda: results.append(
            qf.run_worker(
                queue,
                {task: handler},
                lease_secs=10,
                wait_secs=20,
                stop=stop,
                concurrency=count,
                poll_wait_secs=1,
            )
        ),
        daemon=True,
    )
    worker.start()
    try:
        finished = [qf.wait_for_job(job.id, timeout=WAIT_SECS, interval=POLL_SECS) for job in jobs]
    finally:
        t0 = time.monotonic()
        stop.set()
        worker.join(timeout=30)

    assert not worker.is_alive(), "worker loop did not stop"
    # Stop latency is bounded by poll_wait_secs (1s here), not wait_secs (20s).
    assert time.monotonic() - t0 < 5.0, "stop waited for the full long poll"
    assert results and results[0].unfinished == []
    assert sorted(started) == sorted(job.id for job in jobs)
    assert active["max"] > 1, f"handlers never overlapped (max active {active['max']})"
    assert active["max"] <= count, f"concurrency cap exceeded ({active['max']} > {count})"
    for job in finished:
        assert job.status == "completed", f"job {job.id}: {job.error_message}"
        assert job.result["handled"] is True

    # Since server 0.5.0 every queue the tenant enqueued to is listed, drained
    # ones with zero counts.
    stats = [q for q in qf.queues() if q.queue == queue]
    assert len(stats) == 1, "the queue this run enqueued to must be listed"
    assert (stats[0].pending, stats[0].running, stats[0].scheduled) == (0, 0, 0)
    assert stats[0].paused is False


# --- 0.5.0 server operations ---------------------------------------------------
#
# The server and database may be shared with other suites running at the same
# time, so every bulk cancel, bulk replay and pause below is scoped to a queue
# (and task name) unique to this run; nothing here can touch another run's jobs.


def test_whoami_reports_the_tenant_and_write_access(qf: QueueFlow) -> None:
    me = qf.whoami()
    assert me.tenant
    assert me.access in ("read_write", "read_only")
    # The rest of this module creates jobs, which needs a read-write credential.
    assert me.access == "read_write", f"QUEUEFLOW_TOKEN is {me.access}"
    assert qf.system.who_am_i().tenant == me.tenant


def test_cancel_jobs_is_scoped_filtered_and_bounded(qf: QueueFlow, suffix: str) -> None:
    # Nothing leases this queue, so every job stays pending until cancelled.
    queue = f"py-live-cancel-{suffix}"
    task = f"py-live-cancel-task-{suffix}"
    other = f"py-live-cancel-other-{suffix}"
    targets = [qf.create_job(task, payload={"i": i}, queue=queue) for i in range(3)]
    bystander = qf.create_job(other, payload={}, queue=queue)

    # The new list filter narrows the queue down to the one task.
    listed = qf.jobs.list_jobs(queue=queue, task_name=task, limit=100).jobs
    assert sorted(j.id for j in listed) == sorted(j.id for j in targets)

    # A terminal status is a 400 before anything is touched.
    with pytest.raises(BadRequestException):
        qf.cancel_jobs(queue=queue, status="completed")
    assert qf.jobs.get_job(targets[0].id).status == "pending"

    # Oldest first, bounded by limit, then the remainder, then nothing.
    assert qf.cancel_jobs(queue=queue, task_name=task, status="pending", limit=2) == 2
    assert qf.jobs.get_job(targets[0].id).status == "cancelled"
    assert qf.jobs.get_job(targets[1].id).status == "cancelled"
    assert qf.jobs.get_job(targets[2].id).status == "pending"
    assert qf.jobs.get_job(bystander.id).status == "pending", "task_name filter ignored"
    assert qf.cancel_jobs(queue=queue, task_name=task) == 1
    assert qf.cancel_jobs(queue=queue, task_name=task) == 0

    # Without the task filter the whole queue is swept.
    assert qf.cancel_jobs(queue=queue) == 1
    assert qf.jobs.get_job(bystander.id).status == "cancelled"
    assert qf.cancel_jobs(queue=queue) == 0


def test_pause_and_resume_queue_gate_claims(qf: QueueFlow, suffix: str) -> None:
    queue = f"py-live-pause-{suffix}"
    task = f"py-live-pause-task-{suffix}"
    job = qf.create_job(task, payload={"gated": True}, queue=queue)

    paused = qf.pause_queue(queue)
    assert paused.queue == queue
    assert paused.paused is True
    assert paused.pending == 1
    assert paused.running == 0
    # Idempotent.
    assert qf.pause_queue(queue).paused is True
    stats = [q for q in qf.queues() if q.queue == queue]
    assert len(stats) == 1 and stats[0].paused is True

    # A worker gets nothing from a paused queue.
    lease_req = LeaseJobsRequest(max_jobs=1, lease_secs=10, wait_secs=0)
    assert qf.worker.lease_jobs(queue, lease_req).jobs == []
    assert qf.jobs.get_job(job.id).status == "pending"

    resumed = qf.resume_queue(queue)
    assert resumed.paused is False
    assert resumed.pending == 1
    assert qf.resume_queue(queue).paused is False

    # Claims flow again: lease the job and complete it through the worker api.
    leased = qf.worker.lease_jobs(queue, LeaseJobsRequest(max_jobs=1, lease_secs=10, wait_secs=5)).jobs
    assert [l.job.id for l in leased] == [job.id]
    qf.worker.complete_job(job.id, CompleteJobRequest(lease_token=leased[0].lease_token, result={"ok": True}))
    done = qf.wait_for_job(job.id, timeout=WAIT_SECS, interval=POLL_SECS)
    assert done.status == "completed"
    drained = [q for q in qf.queues() if q.queue == queue]
    assert len(drained) == 1
    assert (drained[0].pending, drained[0].running, drained[0].paused) == (0, 0, False)


def test_bulk_replay_of_dead_letters_scoped_to_this_run(qf: QueueFlow, suffix: str) -> None:
    queue = f"py-live-dlq-{suffix}"
    task = f"py-live-dlq-task-{suffix}"
    job = qf.create_job(task, payload={"doomed": True}, queue=queue, max_retries=0)

    stop = threading.Event()

    def reject(leased: Any) -> Dict[str, Any]:
        stop.set()
        raise NonRetryableError("permanent: bad input")

    worker = threading.Thread(
        target=qf.run_worker,
        args=(queue, {task: reject}),
        kwargs={"lease_secs": 10, "wait_secs": 2, "stop": stop},
        daemon=True,
    )
    worker.start()
    try:
        failed = qf.wait_for_job(job.id, timeout=WAIT_SECS, interval=POLL_SECS)
    finally:
        stop.set()
        worker.join(timeout=30)
    assert not worker.is_alive()
    assert failed.status == "failed"

    # The new list filters: by task, and by replayed state.
    unreplayed = qf.dlq.list_dead_letters(task_name=task, replayed=False, limit=100).dead_letters
    assert [d.job_id for d in unreplayed] == [job.id]
    entry = unreplayed[0]
    assert entry.replayed_at is None
    assert qf.dlq.list_dead_letters(task_name=task, replayed=True, limit=100).dead_letters == []

    results = qf.replay_dead_letters(queue=queue, task_name=task)
    assert [r.dead_letter_id for r in results] == [entry.id]
    assert results[0].error is None
    assert results[0].job_id is not None and results[0].job_id != job.id
    replayed_job = qf.jobs.get_job(results[0].job_id)
    assert replayed_job.task_name == task
    assert replayed_job.queue_name == queue
    assert replayed_job.payload == {"doomed": True}

    # Replayed entries flip lists and are never replayed twice.
    assert qf.dlq.list_dead_letters(task_name=task, replayed=False, limit=100).dead_letters == []
    after = qf.dlq.list_dead_letters(task_name=task, replayed=True, limit=100).dead_letters
    assert [d.id for d in after] == [entry.id]
    assert after[0].replay_job_id == results[0].job_id
    assert qf.replay_dead_letters(queue=queue, task_name=task) == []

    # Nothing handles the replayed job; sweep it so the queue does not linger.
    assert qf.cancel_jobs(queue=queue, task_name=task) == 1
    assert qf.jobs.get_job(results[0].job_id).status == "cancelled"


# --- 0.6.0 workflows: conditions, fan-out, sub-workflows, retry ----------------
#
# Every step below runs on a queue unique to this run, served by one worker
# thread started for the module, so a shared server never sees these tasks on
# a queue another suite polls. Handlers read their upstream results from the
# `_context` the engine injects into each payload.

import uuid

from queueflow.exceptions import ApiException

V2_QUEUE = f"py-live-{uuid.uuid4()}"
WF_WAIT_SECS = 90.0


@pytest.fixture(scope="module")
def v2_worker(qf: QueueFlow):
    attempts: Dict[str, int] = {}

    def seed(job: Any) -> Dict[str, Any]:
        return {"ok": True, "flags": {"vip": True}, "items": [3, 1, 2]}

    def noop(job: Any) -> Dict[str, Any]:
        context = (job.payload or {}).get("_context", {})
        return {"ran": True, "saw": sorted(context)}

    def square(job: Any) -> Dict[str, Any]:
        payload = job.payload or {}
        return {"n": payload["n"], "sq": payload["n"] ** 2, "index": payload["_index"]}

    def total(job: Any) -> Dict[str, Any]:
        results = (job.payload or {})["_context"]["square"]["results"]
        return {"sum": sum(r["sq"] for r in results)}

    def flaky(job: Any) -> Dict[str, Any]:
        key = job.workflow_id or job.id
        attempts[key] = attempts.get(key, 0) + 1
        if attempts[key] == 1:
            raise NonRetryableError("first attempt rejected on purpose")
        return {"attempt": attempts[key]}

    handlers = {"seed": seed, "noop": noop, "square": square, "total": total, "flaky": flaky}
    stop = threading.Event()
    worker = threading.Thread(
        target=qf.run_worker,
        args=(V2_QUEUE, handlers),
        kwargs={"lease_secs": 10, "wait_secs": 20, "stop": stop, "concurrency": 4, "poll_wait_secs": 1},
        daemon=True,
    )
    worker.start()
    yield attempts
    stop.set()
    worker.join(timeout=30)
    assert not worker.is_alive(), "v2 worker loop did not stop"


def test_condition_skipped_step_still_satisfies_its_dependents(qf: QueueFlow, suffix: str, v2_worker: Any) -> None:
    dag = (
        wf(f"py-live-cond-{suffix}")
        .step("seed", "seed", queue=V2_QUEUE)
        # True: object equality against the seed result.
        .step("vip", "noop", after=["seed"], queue=V2_QUEUE, when={"path": "seed.flags", "value": {"vip": True}})
        # False: the path does not exist, so the step is skipped.
        .step("gated", "noop", after=["seed"], queue=V2_QUEUE, when={"path": "seed.missing", "op": "exists"})
        .step("after_gate", "noop", after=["gated", "vip"], queue=V2_QUEUE)
    )
    workflow = qf.create_workflow(dag)
    assert workflow.steps[2].when is not None
    assert workflow.steps[2].when.path == "seed.missing"
    assert workflow.steps[0].queue == V2_QUEUE

    finished = qf.wait_for_workflow(workflow.id, timeout=WF_WAIT_SECS, interval=POLL_SECS)
    assert finished.status == "completed", finished.error_message

    steps = {s.name: s for s in qf.workflow_steps(workflow.id)}
    assert steps["vip"].status == "completed"
    assert steps["gated"].status == "skipped"
    assert steps["gated"].error == "condition not met"
    assert steps["gated"].job_id is None
    # Unlike a policy skip, a condition skip satisfies its dependents.
    assert steps["after_gate"].status == "completed"
    saw = finished.context["after_gate"]["saw"]
    assert "seed" in saw and "vip" in saw and "gated" not in saw
    assert "gated" not in finished.context
    for name in ("seed", "vip", "after_gate"):
        assert steps[name].started_at is not None, name
        assert steps[name].completed_at is not None, name
        assert steps[name].job_id is not None, name
        assert steps[name].error is None, name


def test_fan_out_runs_once_per_element_and_collects_ordered_results(qf: QueueFlow, suffix: str, v2_worker: Any) -> None:
    dag = (
        wf(f"py-live-fanout-{suffix}")
        .step("seed", "seed", queue=V2_QUEUE)
        .step("square", "square", after=["seed"], queue=V2_QUEUE, fan_out={"path": "seed.items", "item_key": "n"})
        .step("total", "total", after=["square"], queue=V2_QUEUE)
    )
    workflow = qf.create_workflow(dag)
    assert workflow.steps[1].fan_out is not None
    assert workflow.steps[1].fan_out.item_key == "n"

    finished = qf.wait_for_workflow(workflow.id, timeout=WF_WAIT_SECS, interval=POLL_SECS)
    assert finished.status == "completed", finished.error_message
    # Results come back in element order, whatever order the children ran in.
    assert finished.context["square"]["results"] == [
        {"n": 3, "sq": 9, "index": 0},
        {"n": 1, "sq": 1, "index": 1},
        {"n": 2, "sq": 4, "index": 2},
    ]
    assert finished.context["total"] == {"sum": 14}

    steps = {s.name: s for s in qf.workflow_steps(workflow.id)}
    progress = steps["square"].fan_out
    assert progress is not None
    assert (progress.total, progress.completed, progress.failed) == (3, 3, 0)
    assert steps["seed"].fan_out is None
    assert steps["square"].status == "completed"

    # job_id is the first child; every child carries its index and the total.
    first = qf.jobs.get_job(steps["square"].job_id)
    assert first.task_name == "square"
    assert first.queue_name == V2_QUEUE
    assert first.workflow_id == workflow.id
    assert first.workflow_step_id == "square"
    assert first.metadata["fan_out_index"] == 0
    assert first.metadata["fan_out_total"] == 3
    children = [j for j in qf.jobs.list_jobs(queue=V2_QUEUE, task_name="square", limit=100).jobs if j.workflow_id == workflow.id]
    assert sorted(j.metadata["fan_out_index"] for j in children) == [0, 1, 2]


def test_sub_workflow_runs_a_child_linked_to_its_parent(qf: QueueFlow, suffix: str, v2_worker: Any) -> None:
    child = (
        wf(f"py-live-child-{suffix}")
        .step("pick", "seed", queue=V2_QUEUE)
        .step("pack", "noop", after=["pick"], queue=V2_QUEUE)
        .timeout_secs(600)
    )
    dag = (
        wf(f"py-live-parent-{suffix}")
        .step("prep", "seed", queue=V2_QUEUE)
        .sub_workflow("fulfil", child, after=["prep"], payload={"warehouse": "eu-1"})
        .step("done", "noop", after=["fulfil"], queue=V2_QUEUE)
    )
    parent = qf.create_workflow(dag)
    assert not parent.steps[1].task_name, "a sub-workflow step has no task (the server stores it empty)"
    assert parent.steps[1].workflow is not None
    assert parent.steps[1].workflow.name == child.name

    finished = qf.wait_for_workflow(parent.id, timeout=WF_WAIT_SECS, interval=POLL_SECS)
    assert finished.status == "completed", finished.error_message
    assert finished.parent_workflow_id is None

    steps = {s.name: s for s in qf.workflow_steps(parent.id)}
    assert steps["fulfil"].status == "completed"
    child_id = steps["fulfil"].child_workflow_id
    assert child_id, "sub-workflow step must link its child"

    child_wf = qf.workflows.get_workflow(child_id)
    assert child_wf.status == "completed", child_wf.error_message
    assert child_wf.parent_workflow_id == parent.id
    assert child_wf.parent_step_name == "fulfil"
    assert child_wf.timeout_secs == 600
    assert child_wf.deadline_at is not None
    # Child context: its own results, the step payload, and the parent under _parent.
    assert child_wf.context["warehouse"] == "eu-1"
    assert child_wf.context["_parent"]["prep"]["ok"] is True
    assert child_wf.context["pick"]["ok"] is True
    assert "_parent" in child_wf.context["pack"]["saw"]
    # The step's result is the child's final context.
    assert finished.context["fulfil"]["pack"]["ran"] is True
    assert finished.context["fulfil"]["warehouse"] == "eu-1"
    assert "fulfil" in finished.context["done"]["saw"]


def test_retry_reruns_a_failed_workflow_from_where_it_stopped(qf: QueueFlow, suffix: str, v2_worker: Any) -> None:
    dag = (
        wf(f"py-live-retry-{suffix}")
        .step("seed", "seed", queue=V2_QUEUE)
        .step("flaky", "flaky", after=["seed"], queue=V2_QUEUE)
        .step("after", "noop", after=["flaky"], queue=V2_QUEUE)
        .timeout_secs(900)
    )
    workflow = qf.create_workflow(dag)
    assert workflow.timeout_secs == 900
    assert workflow.deadline_at is not None
    assert workflow.retry_count == 0

    # The first flaky attempt is a non-retryable failure; halt cancels the rest.
    failed = qf.wait_for_workflow(workflow.id, timeout=WF_WAIT_SECS, interval=POLL_SECS)
    assert failed.status == "failed"
    assert failed.error_message and "first attempt rejected" in failed.error_message
    steps = {s.name: s for s in qf.workflow_steps(workflow.id)}
    assert steps["seed"].status == "completed"
    assert steps["flaky"].status == "failed"
    assert steps["flaky"].error and "first attempt rejected" in steps["flaky"].error
    assert steps["after"].status == "cancelled"
    seed_job = steps["seed"].job_id

    retried = qf.retry_workflow(workflow.id)
    assert retried.status != "failed"
    assert retried.error_message is None
    assert retried.retry_count == 1
    assert retried.deadline_at is not None and retried.deadline_at >= workflow.deadline_at

    finished = qf.wait_for_workflow(workflow.id, timeout=WF_WAIT_SECS, interval=POLL_SECS)
    assert finished.status == "completed", finished.error_message
    assert finished.context["flaky"] == {"attempt": 2}
    assert finished.context["seed"]["ok"] is True
    assert v2_worker[workflow.id] == 2, "flaky ran exactly twice"
    steps = {s.name: s for s in qf.workflow_steps(workflow.id)}
    assert all(s.status == "completed" for s in steps.values()), steps
    assert steps["seed"].job_id == seed_job, "completed steps keep their state across a retry"
    assert steps["flaky"].error is None

    # Retrying a completed workflow is a 409.
    with pytest.raises(ApiException) as excinfo:
        qf.retry_workflow(workflow.id)
    assert excinfo.value.status == 409
