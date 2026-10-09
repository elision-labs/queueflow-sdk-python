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

from queueflow.exceptions import NotFoundException
from queueflow.facade import QueueFlow, wf

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
