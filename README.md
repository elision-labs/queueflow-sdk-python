# queueflow

Python client for [QueueFlow](https://queueflow.dev), a PostgreSQL-native distributed job queue and
workflow engine.

- **Typed end-to-end**: request/response models (pydantic v2) mirror the server's OpenAPI 3.1 spec.
- **Ergonomic**: `qf.create_job(...)`, `wait_for_*` pollers, and a workflow builder DSL.
- **Worker runtime**: `qf.run_worker(...)` runs Python task handlers against a remote server.
- **Thin facade over a generated core**: the facade (`queueflow.facade`) adds what codegen cannot;
  the generated `queueflow.api.*` clients and `queueflow.models.*` stay available for everything else.

Python 3.9 or newer.

## Install

```bash
pip install queueflow
```

## Quick start

```python
from queueflow.facade import QueueFlow, wf

qf = QueueFlow("http://localhost:8000", "dev")

# Enqueue a job and wait for the result.
job = qf.create_job("echo", payload={"hello": "world"}, max_retries=3, timeout=30)
done = qf.wait_for_job(job.id)
print(done.status, done.result)   # completed {'hello': 'world', 'echoed': True}

# Declare and run a DAG workflow.
dag = (
    wf("etl")
    .step("extract", "echo")
    .step("transform", "echo", after=["extract"])
    .step("load", "echo", after=["transform"], on_failure="halt")
)
workflow = qf.create_workflow(dag)
finished = qf.wait_for_workflow(workflow.id)
print(finished.status, finished.context)
```

`echo` is a handler built into the server; it returns the payload plus `"echoed": true`.

## API

### Client

```python
qf = QueueFlow(
    base_url,             # required, e.g. "http://localhost:8000"
    token,                # required: tenant bearer token (any non-empty token on the dev server)
    worker_token=None,    # credential for qf.worker and run_worker (defaults to token; dev mode only)
)
```

The generated per-tag clients hang off the facade for anything the helpers do not cover:
`qf.jobs`, `qf.workflows`, `qf.worker`, `qf.cron`, `qf.dlq`, `qf.system`, `qf.health_api`.

### Jobs

| Method | Description |
| --- | --- |
| `qf.create_job(task, payload=None, priority=None, max_retries=None, timeout=None, queue=None, retry_backoff=None, retry_delay_secs=None, retry_max_delay_secs=None, jitter_factor=None, idempotency_key=None, run_at=None)` | Enqueue a job and return the created `Job`. |
| `qf.wait_for_job(job_id, timeout=60.0, interval=0.5)` | Poll until `completed` / `failed` / `cancelled`; raises `WaitTimeout`. |
| `qf.jobs.get_job(id)` | Fetch a job. |
| `qf.jobs.list_jobs(status=..., queue=..., limit=..., offset=..., order_by=..., include_total=..., cursor=..., created_after=..., created_before=...)` | List jobs. |
| `qf.jobs.cancel_job(id)` | Cancel a job. |
| `qf.jobs.create_batch_jobs(CreateBatchJobsRequest(...))` | Enqueue up to 1000 jobs at once. |

`idempotency_key` is sent as the `Idempotency-Key` header: re-submitting the same key returns the
original job instead of creating a duplicate. `run_at` (a `datetime`) delays the first run.

List responses carry `next_cursor` when there are more pages; pass it back as `cursor` for keyset
pagination (cheaper than deep `offset`).

### Workflows

| Method | Description |
| --- | --- |
| `qf.create_workflow(builder_or_request)` | Create a workflow from a `wf()` builder or a raw `CreateWorkflowRequest`. |
| `qf.wait_for_workflow(workflow_id, timeout=60.0, interval=0.5)` | Poll until a terminal workflow state. |
| `qf.workflows.get_workflow(id)` / `list_workflows(...)` / `cancel_workflow(id)` | Fetch / list / cancel. |
| `qf.workflows.get_workflow_step_states(id)` | Runtime status of every step, in declaration order. |
| `qf.workflows.get_workflow_diagram(id)` | Mermaid (`graph TD`) diagram of the DAG. |

### Workflow builder

```python
from queueflow.facade import wf

dag = (
    wf("order_123")
    .step("validate", "validate_order")
    .step("pay", "process_payment", after=["validate"])
    .step("ship", "create_shipment", after=["pay"], on_failure="continue")
    .context(source="web")
)
# .build() runs locally first: duplicate names, dangling deps, and cycles raise
# WorkflowValidationError before any network round-trip.
```

`step()` also accepts `payload=`, `on_success=`, and `config=` (a `models.JobConfig` override).

### Worker

Run task handlers in this process against a remote QueueFlow server:

```python
import threading
from queueflow.facade import QueueFlow, NonRetryableError

qf = QueueFlow("http://localhost:8000", "tenant-key", worker_token="worker-secret")

def send_email(job):
    if not job.payload.get("to"):
        raise NonRetryableError("no recipient")   # straight to the dead-letter queue
    ...                                           # raising anything else retries per policy
    return {"sent": True}

def transcode(job, ctx):
    for chunk in chunks(job.payload):
        if ctx.cancelled:                         # lease lost / cancelled mid-run: stop,
            return {}                             # the server owns the outcome now
        process(chunk)
    return {"ok": True}

stop = threading.Event()                          # set it (e.g. from a signal handler) to drain
qf.run_worker("orders", {"send_email": send_email, "transcode": transcode}, stop=stop)
```

`run_worker(queue, handlers, lease_secs=30, wait_secs=20, stop=None, on_error=None)` leases one
job at a time, heartbeats each in-flight job at half the lease interval, stops reporting when the
lease is lost, and applies the server's retry policy on errors. Handlers take `(job)` or
`(job, ctx)` and return the result dict (or `None` for `{}`). Delivery is at-least-once, so make
handlers idempotent. The low-level calls (`qf.worker.lease_jobs`, `heartbeat_job`, `complete_job`,
`fail_job`) are also exposed.

Rules the runtime enforces, and that any hand-rolled loop over `qf.worker` must honour too:

1. Worker routes authenticate with the **worker token**, not a tenant token. Pass it as
   `worker_token=`; without it `qf.worker` reuses the tenant token, which only works in the
   server's development mode. `run_worker` raises on 401/403 rather than spinning.
2. Every in-flight job is heartbeated at half its lease interval. A heartbeat showing the job no
   longer running (or an HTTP 409) abandons reporting and flips `ctx.cancelled`.
3. Raise `NonRetryableError` (or any exception with `retryable = False`) for permanent failures so
   they dead-letter immediately. A failed outcome *report* is never converted into a job failure;
   the lease expires and the engine redelivers.

### Cron

| Method | Description |
| --- | --- |
| `qf.create_cron(name, schedule, task, payload=None, queue=None)` | Register a recurring enqueue (5-field crontab, UTC); returns the schedule id. |
| `qf.cron.get_cron(id)` / `list_crons(...)` / `delete_cron(id)` | Fetch / list / delete. |
| `qf.cron.pause_cron(id)` / `resume_cron(id)` | Stop firings / resume at the next future occurrence. |

### Dead letters

| Method | Description |
| --- | --- |
| `qf.dlq.list_dead_letters(...)` / `get_dead_letter(id)` | Inspect terminally-failed jobs. |
| `qf.replay_dead_letter(id)` | Re-run one as a fresh job and return it (at most once; a second replay is a 409). |

### System

```python
qf.system.get_stats()    # engine counters
qf.system.list_tasks()   # registered task handler names
qf.health_api.get_health()
qf.health_api.get_ready()
```

## Authentication

Every request carries `Authorization: Bearer <token>`. Two credentials exist:

- The **tenant token** (`token`) authenticates the job, workflow, cron, DLQ and system routes. On a
  server started without `--api-keys`, any non-empty token is accepted (development mode).
- The **worker token** (`worker_token`) authenticates the worker-protocol routes (lease, heartbeat,
  complete, fail). Configure it on the server with `--worker-token` / `QUEUEFLOW_WORKER_TOKEN`.
  It is a separate secret, never a tenant token.

## Error handling

Generated calls raise `queueflow.exceptions.ApiException` (with `.status`, `.reason`, `.body`) and
its subclasses `BadRequestException` (400), `UnauthorizedException` (401), `ForbiddenException`
(403), `NotFoundException` (404), `ServiceException` (5xx). The facade adds `WaitTimeout` (a
`wait_for_*` deadline passed), `WorkflowValidationError` (a bad DAG, raised before any request),
and `NonRetryableError` (raise from a handler to dead-letter immediately).

```python
from queueflow.exceptions import ApiException, NotFoundException
from queueflow.facade import WaitTimeout

try:
    job = qf.wait_for_job("missing", timeout=10)
except NotFoundException:
    ...
except WaitTimeout:
    ...
except ApiException as err:
    print(err.status, err.body)
```

## Known limitation: `stream_job_events`

`JobsApi.stream_job_events` cannot stream: it buffers the whole SSE response until the server
closes it (terminal status or the 15-minute cap). Use `wait_for_job` (polling) instead, or the
`stream_job_events_without_preload_content` variant with a hand-rolled SSE parser.

## Conformance tests

`test/test_live.py` runs the facade against a real QueueFlow server (started with the default
`queueflow serve`, i.e. `--mode all`, so the built-in `echo` handler is registered). It creates
and waits on an `echo` job, checks idempotent re-creation, runs a two-step workflow, exercises the
cron and dead-letter endpoints, reads stats, and runs `run_worker` against a dedicated queue. The
tests are marked `live` and skip themselves unless `QUEUEFLOW_URL` is set, so plain `pytest` and
CI stay offline.

```bash
QUEUEFLOW_URL=http://localhost:8000 \
QUEUEFLOW_TOKEN=dev \
QUEUEFLOW_WORKER_TOKEN=worker-secret \
pytest -m live
```

`QUEUEFLOW_TOKEN` is the tenant token (default `dev`). `QUEUEFLOW_WORKER_TOKEN` is the server's
`--worker-token`; it defaults to the tenant token, which only works when the server runs without
one.

## Architecture

This package is a thin hand-written **facade** over a **generated core**:

```
queueflow-sdk-python/
├── queueflow/
│   ├── facade.py        the hand-written facade (QueueFlow, wf, run_worker, errors)
│   ├── api/             generated per-tag clients (JobsApi, WorkflowsApi, WorkerApi, ...)
│   ├── models/          generated pydantic models
│   └── api_client.py, configuration.py, rest.py, exceptions.py   generated transport
├── docs/                generated per-endpoint and per-model reference
└── test/                test_facade.py (offline), test_live.py (conformance), generated model tests
```

The core is generated by openapi-generator from the server's
[OpenAPI spec](https://github.com/elision-labs/queueflow-core/blob/main/spec/openapi.yaml)
(`scripts/generate-sdks.sh python` in queueflow-core). The facade is injected at generation time
from `sdk-templates/python/facade.mustache` in that repo, so edit the template, not
`queueflow/facade.py`. Per-endpoint reference for the generated layer lives in [`docs/`](./docs).

### Development

```bash
pip install -e . -r test-requirements.txt
pytest                 # offline tests (facade + generated model tests)
mypy                   # type-check queueflow/ and test/
```

## Links

- Documentation: [docs.queueflow.dev](https://docs.queueflow.dev)
- Server: [github.com/elision-labs/queueflow-core](https://github.com/elision-labs/queueflow-core)
- This SDK: [github.com/elision-labs/queueflow-sdk-python](https://github.com/elision-labs/queueflow-sdk-python)

## License

[MIT](./LICENSE)
