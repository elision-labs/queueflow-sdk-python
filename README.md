# QueueFlow Python SDK

The official Python SDK for QueueFlow distributed job queue system.

## Installation

```bash
pip install queueflow
```

## Quick Start

### Synchronous Client

```python
from queueflow import QueueFlowClient

# Create client
client = QueueFlowClient("http://localhost:8080", "your-api-key")

# Create a job
job = client.create_job(
    task_name="process_data",
    payload={"user_id": 123, "action": "send_email"},
    config={
        "priority": "high",
        "retries": 3,
        "timeout": 300
    }
)

print(f"Job created: {job['id']}")

# Get job status
status = client.get_job(job['id'])
print(f"Job status: {status['status']}")
```

### Asynchronous Client

```python
import asyncio
from queueflow import AsyncQueueFlowClient

async def main():
    # Create async client
    client = AsyncQueueFlowClient("http://localhost:8080", "your-api-key")
    
    # Create a job
    job = await client.create_job(
        task_name="process_data",
        payload={"user_id": 123, "action": "send_email"}
    )
    
    print(f"Job created: {job['id']}")
    
    # Get job status
    status = await client.get_job(job['id'])
    print(f"Job status: {status['status']}")
    
    await client.close()

asyncio.run(main())
```

## Features

- ✅ Synchronous and asynchronous clients
- ✅ Create and manage jobs
- ✅ Batch job operations
- ✅ Job status monitoring  
- ✅ Workflow support
- ✅ Type hints for better IDE support
- ✅ Automatic retries with exponential backoff
- ✅ Context manager support

## API Reference

### Synchronous Client

```python
from queueflow import QueueFlowClient

# Create client
client = QueueFlowClient(base_url, api_key)

# Jobs
job = client.create_job(task_name, payload, config=None)
job = client.get_job(job_id)
client.cancel_job(job_id)
jobs = client.list_jobs(status=None, limit=10, offset=0)

# Batches  
batch = client.create_batch(jobs)
batch = client.get_batch(batch_id)

# Workflows
workflow = client.create_workflow(name, steps)
workflow = client.get_workflow(workflow_id)
```

### Asynchronous Client

```python
from queueflow import AsyncQueueFlowClient

# Create client
client = AsyncQueueFlowClient(base_url, api_key)

# All methods are async versions of sync client
job = await client.create_job(task_name, payload)
job = await client.get_job(job_id)
await client.cancel_job(job_id)

# Context manager support
async with AsyncQueueFlowClient(base_url, api_key) as client:
    job = await client.create_job("task", {"data": "value"})
```

## Configuration

### Job Configuration

```python
config = {
    "priority": "high",      # low, normal, high, critical
    "retries": 3,           # number of retries
    "timeout": 300,         # timeout in seconds
    "delay": 30,            # delay before execution (seconds)
    "queue": "priority"     # queue name
}

job = client.create_job("task_name", payload, config=config)
```

### Client Configuration

```python
# Custom timeout
client = QueueFlowClient(base_url, api_key, timeout=60)

# Custom session with retries
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

session = requests.Session()
retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504]
)
adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("http://", adapter)
session.mount("https://", adapter)

client = QueueFlowClient(base_url, api_key, session=session)
```

## Error Handling

```python
from queueflow import QueueFlowError, NotFoundError, ValidationError

try:
    job = client.create_job("task", payload)
except ValidationError as e:
    print(f"Validation error: {e}")
except NotFoundError as e:
    print(f"Resource not found: {e}")
except QueueFlowError as e:
    print(f"QueueFlow error: {e}")
```

## Examples

### Batch Processing

```python
# Create multiple jobs at once
jobs = [
    {"task_name": "process_user", "payload": {"user_id": i}}
    for i in range(100)
]

batch = client.create_batch(jobs)
print(f"Batch created: {batch['id']}")

# Monitor batch progress
while True:
    batch = client.get_batch(batch['id'])
    if batch['status'] in ['completed', 'failed']:
        break
    time.sleep(5)
```

### Workflow Orchestration

```python
# Create a data processing workflow
workflow = client.create_workflow(
    name="data_pipeline",
    steps=[
        {
            "name": "extract",
            "task_name": "extract_data",
            "payload": {"source": "database"}
        },
        {
            "name": "transform",
            "task_name": "transform_data", 
            "depends_on": ["extract"],
            "payload": {"format": "json"}
        },
        {
            "name": "load",
            "task_name": "load_data",
            "depends_on": ["transform"],
            "payload": {"destination": "warehouse"}
        }
    ]
)
```

### Context Manager

```python
# Automatic resource cleanup
with QueueFlowClient(base_url, api_key) as client:
    job = client.create_job("task", {"data": "value"})
    status = client.get_job(job['id'])

# Async context manager
async with AsyncQueueFlowClient(base_url, api_key) as client:
    job = await client.create_job("task", {"data": "value"})
```

## Development

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run tests with coverage
pytest --cov=queueflow

# Format code
black queueflow/
isort queueflow/

# Type checking
mypy queueflow/
```

## License

MIT License