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
    timeout=30.0,         # default per-request timeout in seconds; a (connect, read) pair or None also work
)
```

Any generated api method accepts `_request_timeout=` to override the default for one call.

The generated per-tag clients hang off the facade for anything the helpers do not cover:
`qf.jobs`, `qf.workflows`, `qf.worker`, `qf.cron`, `qf.dlq`, `qf.system`, `qf.health_api`.

### Jobs

| Method | Description |
| --- | --- |
| `qf.create_job(task, payload=None, priority=None, max_retries=None, timeout=None, queue=None, retry_backoff=None, retry_delay_secs=None, retry_max_delay_secs=None, jitter_factor=None, idempotency_key=None, run_at=None)` | Enqueue a job and return the created `Job`. |
| `qf.wait_for_job(job_id, timeout=60.0, interval=0.5)` | Poll until `completed` / `failed` / `cancelled`; raises `WaitTimeout`. |
| `qf.jobs.get_job(id)` | Fetch a job. |
| `qf.jobs.list_jobs(status=..., queue=..., task_name=..., limit=..., offset=..., order_by=..., include_total=..., cursor=..., created_after=..., created_before=...)` | List jobs. |
| `qf.jobs.cancel_job(id)` | Cancel a job. |
| `qf.cancel_jobs(queue=None, task_name=None, status=None, created_after=None, created_before=None, limit=None)` | Cancel every matching non-terminal job of your tenant, oldest first, up to `limit` (default 100); returns the count. |
| `qf.jobs.create_batch_jobs(CreateBatchJobsRequest(...))` | Enqueue up to 1000 jobs at once. |

`idempotency_key` is sent as the `Idempotency-Key` header: re-submitting the same key returns the
original job instead of creating a duplicate. `run_at` (a `datetime`) delays the first run.

List responses carry `next_cursor` when there are more pages; pass it back as `cursor` for keyset
pagination (cheaper than deep `offset`).

`cancel_jobs` takes optional filters that combine: `queue`, `task_name`, `status` (`pending`,
`retrying` or `running`; all three when omitted, a terminal status is a 400) and the half-open
`datetime` window `[created_after, created_before)`. A count below `limit` means the matching set is
exhausted, so loop until then to drain a large backlog:

```python
while qf.cancel_jobs(queue="orders", task_name="send_email", limit=500) == 500:
    pass
```

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
result = qf.run_worker(
    "orders",
    {"send_email": send_email, "transcode": transcode},
    stop=stop,
    concurrency=4,
)
for job in result.unfinished:                     # handlers still running when the drain gave up
    print("abandoned", job.id)
```

```python
run_worker(
    queue, handlers,
    lease_secs=30,        # lease per job; each in-flight job is heartbeated at half this
    wait_secs=20,         # long-poll wait when the queue is empty
    stop=None,            # threading.Event: set it to stop
    on_error=None,        # called on transient lease errors (default: throttled log)
    concurrency=1,        # handlers running at once, on a ThreadPoolExecutor
    poll_wait_secs=5,     # cap on wait_secs while `stop` is provided (bounds stop latency)
    drain_timeout=30.0,   # seconds to wait for in-flight handlers after stop
) -> WorkerRunResult      # .unfinished: jobs still running when the drain gave up
```

`run_worker` heartbeats each in-flight job at half the lease interval, stops reporting when the
lease is lost, and applies the server's retry policy on errors. Handlers take `(job)` or
`(job, ctx)` and return the result dict (or `None` for `{}`). Delivery is at-least-once, so make
handlers idempotent. The low-level calls (`qf.worker.lease_jobs`, `heartbeat_job`, `complete_job`,
`fail_job`) are also exposed.

Concurrency: up to `concurrency` handlers run at once. Each lease asks for as many jobs as there
are free slots, and no lease is issued while every slot is busy.

Stop and drain: set `stop`. The generated urllib3 client cannot cancel an in-flight long poll, so
while `stop` is provided each lease waits at most `poll_wait_secs` (never more than `wait_secs`),
which bounds stop latency to about that long; without `stop`, the full `wait_secs` is used. After
the loop exits, handlers already running get up to `drain_timeout` seconds to finish and report.
Any handler still running after that is abandoned: its `ctx.cancelled` flips, nothing is reported
(the lease expires and the server redelivers), and the job is listed in the returned
`WorkerRunResult.unfinished`. Python cannot kill a thread, so an abandoned handler keeps its pool
thread until it returns; long handlers should check `ctx.cancelled`.

Timeouts: every request uses the client-wide `timeout` (30s by default, see Client), except the
lease long poll, which gets its own timeout of the effective wait plus 35 seconds.

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
| `qf.dlq.list_dead_letters(task_name=..., replayed=..., limit=..., offset=..., order_by=..., include_total=..., cursor=..., created_after=..., created_before=...)` / `get_dead_letter(id)` | Inspect terminally-failed jobs. `replayed=False` lists only entries not yet replayed, `True` only the replayed ones. |
| `qf.replay_dead_letter(id)` | Re-run one as a fresh job and return it (at most once; a second replay is a 409). |
| `qf.replay_dead_letters(queue=None, task_name=None, created_after=None, created_before=None, limit=None)` | Replay every unreplayed entry matching the filter, oldest first, up to `limit` (default 100). Returns a `ReplayedDeadLetter` per entry: `job_id` on success, otherwise `error`. |

```python
for r in qf.replay_dead_letters(queue="orders", task_name="send_email"):
    if r.error:
        print("dead letter", r.dead_letter_id, "not replayed:", r.error)
    else:
        print("dead letter", r.dead_letter_id, "replayed as", r.job_id)
```

Already-replayed entries are never considered again, so repeating the call walks a large backlog;
an empty list means nothing was left to replay.

### System

```python
qf.whoami()              # the tenant this token is scoped to and its access level
qf.system.get_stats()    # engine counters
qf.system.list_tasks()   # registered task handler names
qf.queues()              # live per-queue backlog: pending, scheduled, running, oldest pending age, paused
qf.pause_queue(name)     # stop claims of your jobs on a queue; running jobs finish
qf.resume_queue(name)    # let claims flow again
qf.health_api.get_health()
qf.health_api.get_ready()
```

`qf.whoami()` (`GET /api/v1/whoami`) returns a `WhoAmIResponse` with `tenant` and `access`
(`read_write`, or `read_only` for a read-only key), handy for validating a credential at startup.

`qf.queues()` (`GET /api/v1/queues`) returns a `QueueStats` per queue so you can decide whether to
add workers. A 0.5.0 or later server lists every queue your tenant has enqueued to (drained ones
with zero counts); older servers list only queues with non-terminal jobs. Its `paused` flag says
whether claims are paused for your tenant. `qf.system.list_queues()` is the raw call.

`qf.pause_queue(name)` / `qf.resume_queue(name)` (`POST /api/v1/queues/{queue}/pause` and
`/resume`) gate workers' claims of your tenant's jobs on that queue. Pausing lets running jobs
finish while pending ones wait, so the queue is drained once the returned `running` count reaches
zero; resuming wakes parked workers immediately. Both are idempotent and return a
`QueueControlResponse` (`queue`, `paused`, `running`, `pending`).

```python
import time

qf.pause_queue("orders")
while qf.pause_queue("orders").running > 0:   # idempotent, so it doubles as a status poll
    time.sleep(1)
deploy_new_handlers()
qf.resume_queue("orders")
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
cron and dead-letter endpoints, reads stats, runs `run_worker` against a dedicated queue, and
exercises `whoami`, bulk cancel, queue pause/resume and bulk dead-letter replay, each scoped to a
queue unique to the run. The tests are marked `live` and skip themselves unless `QUEUEFLOW_URL` is
set, so plain `pytest` and CI stay offline.

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
