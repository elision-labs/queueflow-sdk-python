"""
QueueFlow Python SDK - Production-ready client for QueueFlow API
"""

import asyncio
import aiohttp
import json
import time
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import logging
from contextlib import asynccontextmanager
import backoff


# Job status enum
class JobStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    RETRYING = "retrying"
    CANCELLED = "cancelled"


# Workflow status enum
class WorkflowStatus(str, Enum):
    CREATED = "created"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    PARTIALLY_FAILED = "partially_failed"


# Configuration classes
@dataclass
class JobConfig:
    """Job configuration"""
    priority: int = 0
    max_retries: int = 3
    timeout: int = 300  # seconds
    queue: str = "default"


@dataclass
class WorkflowStep:
    """Workflow step definition"""
    name: str
    task_name: str
    payload: Dict[str, Any] = field(default_factory=dict)
    depends_on: List[str] = field(default_factory=list)
    config: Optional[JobConfig] = None


# Response models
@dataclass
class Job:
    """Job model"""
    id: str
    queue_name: str
    task_name: str
    payload: Dict[str, Any]
    status: JobStatus
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    retry_count: int = 0
    workflow_id: Optional[str] = None
    workflow_step_id: Optional[str] = None
    result: Optional[Dict[str, Any]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Workflow:
    """Workflow model"""
    id: str
    name: str
    status: WorkflowStatus
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    context: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ListResponse:
    """Paginated list response"""
    items: List[Any]
    total: int
    limit: int
    offset: int
    has_more: bool


# Exceptions
class QueueFlowError(Exception):
    """Base exception for QueueFlow SDK"""
    pass


class QueueFlowAPIError(QueueFlowError):
    """API request failed"""
    def __init__(self, message: str, status_code: int, response_body: Optional[str] = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_body = response_body


class QueueFlowAuthError(QueueFlowError):
    """Authentication failed"""
    pass


class QueueFlowRateLimitError(QueueFlowError):
    """Rate limit exceeded"""
    def __init__(self, message: str, retry_after: int):
        super().__init__(message)
        self.retry_after = retry_after


class QueueFlowTimeoutError(QueueFlowError):
    """Request timed out"""
    pass


# Main client class
class QueueFlowClient:
    """
    QueueFlow Python SDK Client
    
    Example:
        async with QueueFlowClient("http://localhost:8080", "your-api-key") as client:
            job_id = await client.create_job("send_email", {"to": "user@example.com"})
            job = await client.wait_for_job(job_id)
            print(f"Job completed: {job.status}")
    """
    
    def __init__(
        self,
        base_url: str,
        api_key: str,
        timeout: int = 30,
        max_retries: int = 3,
        enable_logging: bool = True,
        log_level: str = "INFO"
    ):
        self.base_url = base_url.rstrip('/') + '/api/v1'
        self.api_key = api_key
        self.timeout = timeout
        self.max_retries = max_retries
        self.session: Optional[aiohttp.ClientSession] = None
        
        # Setup logging
        self.logger = logging.getLogger(__name__)
        if enable_logging:
            logging.basicConfig(level=getattr(logging, log_level))
    
    async def __aenter__(self):
        """Async context manager entry"""
        connector = aiohttp.TCPConnector(limit=100, ttl_dns_cache=300)
        timeout_config = aiohttp.ClientTimeout(total=self.timeout)
        
        self.session = aiohttp.ClientSession(
            connector=connector,
            timeout=timeout_config,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json",
                "User-Agent": "QueueFlow-Python-SDK/1.0"
            }
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    @backoff.on_exception(
        backoff.expo,
        (aiohttp.ClientError, asyncio.TimeoutError),
        max_tries=3,
        max_time=30
    )
    async def _request(
        self,
        method: str,
        endpoint: str,
        json_data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make HTTP request with retry logic"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            async with self.session.request(
                method,
                url,
                json=json_data,
                params=params
            ) as response:
                response_text = await response.text()
                
                if response.status == 401:
                    raise QueueFlowAuthError("Authentication failed")
                
                if response.status == 429:
                    retry_after = int(response.headers.get('Retry-After', '60'))
                    raise QueueFlowRateLimitError("Rate limit exceeded", retry_after)
                
                if response.status >= 400:
                    try:
                        error_data = json.loads(response_text)
                        error_message = error_data.get("error", response_text)
                    except:
                        error_message = response_text
                    
                    raise QueueFlowAPIError(
                        f"API request failed: {error_message}",
                        status_code=response.status,
                        response_body=response_text
                    )
                
                return json.loads(response_text) if response_text else {}
                
        except aiohttp.ClientError as e:
            raise QueueFlowError(f"Network error: {e}")
        except asyncio.TimeoutError:
            raise QueueFlowTimeoutError(f"Request timed out after {self.timeout}s")
    
    # Job management methods
    async def create_job(
        self,
        task_name: str,
        payload: Optional[Dict[str, Any]] = None,
        config: Optional[JobConfig] = None,
        idempotency_key: Optional[str] = None
    ) -> str:
        """Create a new job"""
        config = config or JobConfig()
        payload = payload or {}
        
        request_data = {
            "task_name": task_name,
            "payload": payload,
            "config": {
                "priority": config.priority,
                "max_retries": config.max_retries,
                "timeout": config.timeout,
                "queue": config.queue
            }
        }
        
        headers = {}
        if idempotency_key:
            headers["Idempotency-Key"] = idempotency_key
        
        # Add headers to session temporarily
        if headers:
            self.session.headers.update(headers)
        
        try:
            response = await self._request("POST", "/jobs", json_data=request_data)
            return response["job_id"]
        finally:
            # Remove temporary headers
            if headers:
                for key in headers:
                    self.session.headers.pop(key, None)
    
    async def get_job(self, job_id: str) -> Job:
        """Get job details"""
        response = await self._request("GET", f"/jobs/{job_id}")
        
        # Convert timestamps
        response['created_at'] = datetime.fromisoformat(response['created_at'].replace('Z', '+00:00'))
        if response.get('started_at'):
            response['started_at'] = datetime.fromisoformat(response['started_at'].replace('Z', '+00:00'))
        if response.get('completed_at'):
            response['completed_at'] = datetime.fromisoformat(response['completed_at'].replace('Z', '+00:00'))
        
        return Job(**response)
    
    async def cancel_job(self, job_id: str) -> bool:
        """Cancel a job"""
        response = await self._request("POST", f"/jobs/{job_id}/cancel")
        return response.get("cancelled", False)
    
    async def get_job_logs(self, job_id: str) -> List[str]:
        """Get job logs"""
        response = await self._request("GET", f"/jobs/{job_id}/logs")
        return response.get("logs", [])
    
    async def list_jobs(
        self,
        limit: int = 50,
        offset: int = 0,
        status: Optional[str] = None,
        queue: Optional[str] = None
    ) -> ListResponse:
        """List jobs with filtering"""
        params = {"limit": limit, "offset": offset}
        if status:
            params["status"] = status
        if queue:
            params["queue"] = queue
        
        response = await self._request("GET", "/jobs", params=params)
        
        # Convert job timestamps
        jobs = []
        for job_data in response.get("jobs", []):
            job_data['created_at'] = datetime.fromisoformat(job_data['created_at'].replace('Z', '+00:00'))
            if job_data.get('started_at'):
                job_data['started_at'] = datetime.fromisoformat(job_data['started_at'].replace('Z', '+00:00'))
            if job_data.get('completed_at'):
                job_data['completed_at'] = datetime.fromisoformat(job_data['completed_at'].replace('Z', '+00:00'))
            jobs.append(Job(**job_data))
        
        return ListResponse(
            items=jobs,
            total=response["total"],
            limit=response["limit"],
            offset=response["offset"],
            has_more=response.get("has_more", False)
        )
    
    async def create_batch_jobs(
        self,
        jobs: List[Dict[str, Any]],
        config: Optional[JobConfig] = None
    ) -> List[str]:
        """Create multiple jobs in batch"""
        config = config or JobConfig()
        
        batch_request = {
            "jobs": [
                {
                    "task_name": job["task_name"],
                    "payload": job.get("payload", {}),
                    "config": {
                        "priority": job.get("config", {}).get("priority", config.priority),
                        "max_retries": job.get("config", {}).get("max_retries", config.max_retries),
                        "timeout": job.get("config", {}).get("timeout", config.timeout),
                        "queue": job.get("config", {}).get("queue", config.queue)
                    }
                }
                for job in jobs
            ]
        }
        
        response = await self._request("POST", "/jobs/batch", json_data=batch_request)
        return response["job_ids"]
    
    async def wait_for_job(
        self,
        job_id: str,
        timeout: int = 300,
        poll_interval: int = 2
    ) -> Job:
        """Wait for job completion"""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            job = await self.get_job(job_id)
            
            if job.status in [JobStatus.COMPLETED, JobStatus.FAILED, JobStatus.CANCELLED]:
                return job
            
            await asyncio.sleep(poll_interval)
        
        raise QueueFlowTimeoutError(f"Job {job_id} did not complete within {timeout}s")
    
    # Workflow management
    async def create_workflow(
        self,
        name: str,
        steps: List[WorkflowStep],
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """Create a workflow"""
        request_data = {
            "name": name,
            "steps": [
                {
                    "name": step.name,
                    "task_name": step.task_name,
                    "payload": step.payload,
                    "depends_on": step.depends_on,
                    "config": {
                        "priority": step.config.priority if step.config else 0,
                        "max_retries": step.config.max_retries if step.config else 3,
                        "timeout": step.config.timeout if step.config else 300,
                        "queue": step.config.queue if step.config else "default"
                    } if step.config else None
                }
                for step in steps
            ]
        }
        
        if metadata:
            request_data["metadata"] = metadata
        
        response = await self._request("POST", "/workflows", json_data=request_data)
        return response["workflow_id"]
    
    async def get_workflow(self, workflow_id: str) -> Workflow:
        """Get workflow details"""
        response = await self._request("GET", f"/workflows/{workflow_id}")
        
        # Convert timestamps
        response['created_at'] = datetime.fromisoformat(response['created_at'].replace('Z', '+00:00'))
        if response.get('started_at'):
            response['started_at'] = datetime.fromisoformat(response['started_at'].replace('Z', '+00:00'))
        if response.get('completed_at'):
            response['completed_at'] = datetime.fromisoformat(response['completed_at'].replace('Z', '+00:00'))
        
        return Workflow(**response)
    
    async def cancel_workflow(self, workflow_id: str) -> bool:
        """Cancel a workflow"""
        response = await self._request("POST", f"/workflows/{workflow_id}/cancel")
        return response.get("cancelled", False)
    
    async def list_workflows(
        self,
        limit: int = 50,
        offset: int = 0,
        status: Optional[str] = None
    ) -> ListResponse:
        """List workflows with filtering"""
        params = {"limit": limit, "offset": offset}
        if status:
            params["status"] = status
        
        response = await self._request("GET", "/workflows", params=params)
        
        # Convert workflow timestamps
        workflows = []
        for wf_data in response.get("workflows", []):
            wf_data['created_at'] = datetime.fromisoformat(wf_data['created_at'].replace('Z', '+00:00'))
            if wf_data.get('started_at'):
                wf_data['started_at'] = datetime.fromisoformat(wf_data['started_at'].replace('Z', '+00:00'))
            if wf_data.get('completed_at'):
                wf_data['completed_at'] = datetime.fromisoformat(wf_data['completed_at'].replace('Z', '+00:00'))
            workflows.append(Workflow(**wf_data))
        
        return ListResponse(
            items=workflows,
            total=response["total"],
            limit=response["limit"],
            offset=response["offset"],
            has_more=response.get("has_more", False)
        )
    
    async def wait_for_workflow(
        self,
        workflow_id: str,
        timeout: int = 600,
        poll_interval: int = 5
    ) -> Workflow:
        """Wait for workflow completion"""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            workflow = await self.get_workflow(workflow_id)
            
            if workflow.status in [WorkflowStatus.COMPLETED, WorkflowStatus.FAILED, 
                                 WorkflowStatus.CANCELLED, WorkflowStatus.PARTIALLY_FAILED]:
                return workflow
            
            await asyncio.sleep(poll_interval)
        
        raise QueueFlowTimeoutError(f"Workflow {workflow_id} did not complete within {timeout}s")
    
    # Utility methods
    async def health_check(self) -> Dict[str, Any]:
        """Check system health"""
        return await self._request("GET", "/health")
    
    async def get_stats(self) -> Dict[str, Any]:
        """Get system statistics"""
        return await self._request("GET", "/stats")


# Synchronous wrapper
class QueueFlowClientSync:
    """
    Synchronous wrapper for QueueFlow client
    
    Example:
        client = QueueFlowClientSync("http://localhost:8080", "your-api-key")
        job_id = client.create_job("send_email", {"to": "user@example.com"})
        job = client.wait_for_job(job_id)
        print(f"Job completed: {job.status}")
    """
    
    def __init__(self, base_url: str, api_key: str, **kwargs):
        self.base_url = base_url
        self.api_key = api_key
        self.kwargs = kwargs
        self._loop = None
    
    def _run_async(self, coro):
        """Run async function in sync context"""
        if self._loop is None:
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)
        
        return self._loop.run_until_complete(coro)
    
    async def _execute(self, func_name: str, *args, **kwargs):
        """Execute async method"""
        async with QueueFlowClient(self.base_url, self.api_key, **self.kwargs) as client:
            method = getattr(client, func_name)
            return await method(*args, **kwargs)
    
    def create_job(self, *args, **kwargs) -> str:
        return self._run_async(self._execute("create_job", *args, **kwargs))
    
    def get_job(self, *args, **kwargs) -> Job:
        return self._run_async(self._execute("get_job", *args, **kwargs))
    
    def cancel_job(self, *args, **kwargs) -> bool:
        return self._run_async(self._execute("cancel_job", *args, **kwargs))
    
    def wait_for_job(self, *args, **kwargs) -> Job:
        return self._run_async(self._execute("wait_for_job", *args, **kwargs))
    
    def create_workflow(self, *args, **kwargs) -> str:
        return self._run_async(self._execute("create_workflow", *args, **kwargs))
    
    def get_workflow(self, *args, **kwargs) -> Workflow:
        return self._run_async(self._execute("get_workflow", *args, **kwargs))
    
    def list_jobs(self, *args, **kwargs) -> ListResponse:
        return self._run_async(self._execute("list_jobs", *args, **kwargs))
    
    def health_check(self) -> Dict[str, Any]:
        return self._run_async(self._execute("health_check"))
    
    def __del__(self):
        """Cleanup event loop"""
        if self._loop:
            self._loop.close()


# Helper functions
def create_step(
    name: str,
    task_name: str,
    payload: Optional[Dict[str, Any]] = None,
    depends_on: Optional[List[str]] = None,
    config: Optional[JobConfig] = None
) -> WorkflowStep:
    """Helper to create workflow step"""
    return WorkflowStep(
        name=name,
        task_name=task_name,
        payload=payload or {},
        depends_on=depends_on or [],
        config=config
    )