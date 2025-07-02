"""
QueueFlow Client SDK - Enhanced Version
Easy-to-use client library with improved developer experience
"""

import asyncio
import aiohttp
import json
import time
from typing import Dict, List, Optional, Any, Callable, Union, TypeVar, Generic, Awaitable
from dataclasses import dataclass, asdict, field
from datetime import datetime, timedelta
from enum import Enum
import logging
from contextlib import asynccontextmanager
from functools import wraps
import backoff


# Type definitions
T = TypeVar('T')
TaskHandler = Callable[[Dict[str, Any]], Awaitable[Optional[Dict[str, Any]]]]
MiddlewareFunc = Callable[[TaskHandler], TaskHandler]


# Enhanced configuration classes
@dataclass
class JobConfig:
    """Enhanced job configuration with validation"""
    priority: int = 0
    max_retries: int = 3
    retry_delay: int = 60
    timeout: int = 300
    ttl: Optional[int] = None
    retry_backoff: str = "exponential"
    retry_max_delay: int = 3600
    
    def __post_init__(self):
        # Validation
        if self.priority < -100 or self.priority > 100:
            raise ValueError("Priority must be between -100 and 100")
        if self.max_retries < 0 or self.max_retries > 10:
            raise ValueError("Max retries must be between 0 and 10")
        if self.timeout < 1 or self.timeout > 3600:
            raise ValueError("Timeout must be between 1 and 3600 seconds")
        if self.retry_backoff not in ["linear", "exponential"]:
            raise ValueError("Retry backoff must be 'linear' or 'exponential'")


@dataclass
class WorkflowStep:
    """Enhanced workflow step with validation and builder pattern"""
    name: str
    task_name: str
    payload: Dict[str, Any] = field(default_factory=dict)
    depends_on: List[str] = field(default_factory=list)
    config: Optional[JobConfig] = None
    condition: Optional[str] = None  # Expression to evaluate
    on_failure: Optional[str] = None
    on_success: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        if self.config is None:
            self.config = JobConfig()
        
        # Validate step name
        if not self.name or not self.name.replace("_", "").replace("-", "").isalnum():
            raise ValueError("Step name must be alphanumeric with underscores/hyphens")
    
    def with_config(self, **kwargs) -> 'WorkflowStep':
        """Builder pattern for configuration"""
        self.config = JobConfig(**kwargs)
        return self
    
    def depends(self, *steps: str) -> 'WorkflowStep':
        """Builder pattern for dependencies"""
        self.depends_on.extend(steps)
        return self
    
    def with_metadata(self, **metadata) -> 'WorkflowStep':
        """Builder pattern for metadata"""
        self.metadata.update(metadata)
        return self


@dataclass
class BatchJobRequest:
    """Request for batch job processing"""
    task_name: str
    payloads: List[Dict[str, Any]]
    config: Optional[JobConfig] = None
    queue_name: Optional[str] = None


# Enhanced exceptions
class QueueFlowError(Exception):
    """Base exception with context"""
    def __init__(self, message: str, context: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.context = context or {}


class JobNotFoundError(QueueFlowError):
    """Job not found"""
    pass


class WorkflowNotFoundError(QueueFlowError):
    """Workflow not found"""
    pass


class QueueFlowTimeoutError(QueueFlowError):
    """Operation timed out"""
    pass


class QueueFlowAPIError(QueueFlowError):
    """API request failed"""
    def __init__(self, message: str, status_code: int, response_body: Optional[str] = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_body = response_body


# Result wrapper for better error handling
@dataclass
class Result(Generic[T]):
    """Result wrapper for operations"""
    success: bool
    data: Optional[T] = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @classmethod
    def ok(cls, data: T, **metadata) -> 'Result[T]':
        return cls(success=True, data=data, metadata=metadata)
    
    @classmethod
    def fail(cls, error: str, **metadata) -> 'Result[T]':
        return cls(success=False, error=error, metadata=metadata)


# Enhanced SDK Client
class QueueFlowSDK:
    """
    Production-ready QueueFlow SDK with enhanced features
    """
    
    def __init__(
        self,
        api_url: str,
        api_key: str,
        timeout: int = 30,
        max_retries: int = 3,
        retry_delay: int = 1,
        enable_logging: bool = True,
        log_level: str = "INFO"
    ):
        self.api_url = api_url.rstrip('/')
        self.api_key = api_key
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.session: Optional[aiohttp.ClientSession] = None
        
        # Setup logging
        self.logger = logging.getLogger(__name__)
        if enable_logging:
            logging.basicConfig(level=getattr(logging, log_level))
        
        # Metrics tracking
        self.metrics = {
            "requests_made": 0,
            "requests_failed": 0,
            "jobs_created": 0,
            "workflows_created": 0
        }
    
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
                "User-Agent": "QueueFlow-SDK/1.0"
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
        url = f"{self.api_url}{endpoint}"
        self.metrics["requests_made"] += 1
        
        try:
            async with self.session.request(
                method,
                url,
                json=json_data,
                params=params
            ) as response:
                response_text = await response.text()
                
                if response.status >= 400:
                    self.metrics["requests_failed"] += 1
                    
                    # Parse error response
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
            self.metrics["requests_failed"] += 1
            raise QueueFlowError(f"Network error: {e}")
        except asyncio.TimeoutError:
            self.metrics["requests_failed"] += 1
            raise QueueFlowTimeoutError(f"Request timed out after {self.timeout}s")
    
    # Job management methods
    async def create_job(
        self,
        task_name: str,
        payload: Optional[Dict[str, Any]] = None,
        config: Optional[JobConfig] = None,
        queue_name: Optional[str] = None,
        idempotency_key: Optional[str] = None
    ) -> Result[str]:
        """
        Create a new job with enhanced error handling
        
        Returns:
            Result object containing job ID or error
        """
        try:
            config = config or JobConfig()
            payload = payload or {}
            
            request_data = {
                "task_name": task_name,
                "payload": payload,
                "config": asdict(config)
            }
            
            if queue_name:
                request_data["queue_name"] = queue_name
            
            if idempotency_key:
                request_data["idempotency_key"] = idempotency_key
            
            response = await self._request("POST", "/jobs", json_data=request_data)
            job_id = response["job_id"]
            
            self.metrics["jobs_created"] += 1
            self.logger.info(f"Created job {job_id} for task {task_name}")
            
            return Result.ok(job_id, task_name=task_name)
            
        except Exception as e:
            self.logger.error(f"Failed to create job: {e}")
            return Result.fail(str(e), task_name=task_name)
    
    async def create_batch_jobs(
        self,
        batch_request: BatchJobRequest,
        max_concurrent: int = 10
    ) -> Result[List[str]]:
        """Create multiple jobs in batch with concurrency control"""
        try:
            semaphore = asyncio.Semaphore(max_concurrent)
            
            async def create_single(payload):
                async with semaphore:
                    result = await self.create_job(
                        batch_request.task_name,
                        payload,
                        batch_request.config,
                        batch_request.queue_name
                    )
                    return result
            
            results = await asyncio.gather(
                *[create_single(p) for p in batch_request.payloads],
                return_exceptions=True
            )
            
            job_ids = []
            failures = []
            
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    failures.append({"index": i, "error": str(result)})
                elif result.success:
                    job_ids.append(result.data)
                else:
                    failures.append({"index": i, "error": result.error})
            
            if failures:
                return Result.fail(
                    f"Failed to create {len(failures)} jobs",
                    job_ids=job_ids,
                    failures=failures
                )
            
            return Result.ok(job_ids)
            
        except Exception as e:
            self.logger.error(f"Batch job creation failed: {e}")
            return Result.fail(str(e))
    
    async def get_job_status(self, job_id: str) -> Result[Dict[str, Any]]:
        """Get job status with enhanced error handling"""
        try:
            response = await self._request("GET", f"/jobs/{job_id}")
            return Result.ok(response)
        except QueueFlowAPIError as e:
            if e.status_code == 404:
                return Result.fail(f"Job {job_id} not found")
            return Result.fail(str(e))
        except Exception as e:
            return Result.fail(str(e))
    
    async def wait_for_job(
        self,
        job_id: str,
        timeout: int = 300,
        poll_interval: int = 2,
        progress_callback: Optional[Callable[[Dict[str, Any]], None]] = None
    ) -> Result[Dict[str, Any]]:
        """
        Wait for job completion with progress updates
        
        Args:
            job_id: Job ID to wait for
            timeout: Maximum time to wait
            poll_interval: How often to check status
            progress_callback: Optional callback for progress updates
        """
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            result = await self.get_job_status(job_id)
            
            if not result.success:
                return result
            
            status = result.data
            
            if progress_callback:
                progress_callback(status)
            
            if status["status"] in ["completed", "failed", "cancelled"]:
                return Result.ok(status)
            
            await asyncio.sleep(poll_interval)
        
        return Result.fail(f"Job {job_id} did not complete within {timeout}s", timeout=True)
    
    # Workflow management
    async def create_workflow(
        self,
        name: str,
        steps: List[WorkflowStep],
        queue_name: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        dry_run: bool = False
    ) -> Result[Union[str, Dict[str, Any]]]:
        """
        Create workflow with validation and dry run support
        
        Args:
            name: Workflow name
            steps: List of workflow steps
            queue_name: Optional queue name
            metadata: Optional metadata
            dry_run: If True, validate without creating
        """
        try:
            # Validate workflow
            validation_errors = self._validate_workflow(steps)
            if validation_errors:
                return Result.fail("Workflow validation failed", errors=validation_errors)
            
            request_data = {
                "name": name,
                "steps": [
                    {
                        "name": step.name,
                        "task_name": step.task_name,
                        "payload": step.payload,
                        "depends_on": step.depends_on,
                        "config": asdict(step.config) if step.config else {},
                        "metadata": step.metadata
                    }
                    for step in steps
                ],
                "metadata": metadata or {}
            }
            
            if queue_name:
                request_data["queue_name"] = queue_name
            
            if dry_run:
                return Result.ok({"valid": True, "workflow": request_data})
            
            response = await self._request("POST", "/workflows", json_data=request_data)
            workflow_id = response["workflow_id"]
            
            self.metrics["workflows_created"] += 1
            self.logger.info(f"Created workflow {workflow_id}: {name}")
            
            return Result.ok(workflow_id, name=name)
            
        except Exception as e:
            self.logger.error(f"Failed to create workflow: {e}")
            return Result.fail(str(e))
    
    def _validate_workflow(self, steps: List[WorkflowStep]) -> List[str]:
        """Validate workflow structure"""
        errors = []
        step_names = {step.name for step in steps}
        
        for step in steps:
            # Check dependencies exist
            for dep in step.depends_on:
                if dep not in step_names:
                    errors.append(f"Step '{step.name}' depends on non-existent step '{dep}'")
            
            # Check for circular dependencies
            if self._has_circular_dependency(steps, step.name):
                errors.append(f"Circular dependency detected involving step '{step.name}'")
        
        return errors
    
    def _has_circular_dependency(self, steps: List[WorkflowStep], start_step: str) -> bool:
        """Check for circular dependencies"""
        step_map = {step.name: step for step in steps}
        visited = set()
        rec_stack = set()
        
        def visit(step_name: str) -> bool:
            if step_name in rec_stack:
                return True
            if step_name in visited:
                return False
            
            visited.add(step_name)
            rec_stack.add(step_name)
            
            step = step_map.get(step_name)
            if step:
                for dep in step.depends_on:
                    if visit(dep):
                        return True
            
            rec_stack.remove(step_name)
            return False
        
        return visit(start_step)
    
    async def get_workflow_status(
        self,
        workflow_id: str,
        include_step_details: bool = True
    ) -> Result[Dict[str, Any]]:
        """Get workflow status with optional step details"""
        try:
            params = {"include_steps": include_step_details}
            response = await self._request("GET", f"/workflows/{workflow_id}", params=params)
            return Result.ok(response)
        except QueueFlowAPIError as e:
            if e.status_code == 404:
                return Result.fail(f"Workflow {workflow_id} not found")
            return Result.fail(str(e))
        except Exception as e:
            return Result.fail(str(e))
    
    async def wait_for_workflow(
        self,
        workflow_id: str,
        timeout: int = 600,
        poll_interval: int = 5,
        progress_callback: Optional[Callable[[Dict[str, Any]], None]] = None
    ) -> Result[Dict[str, Any]]:
        """Wait for workflow completion with progress updates"""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            result = await self.get_workflow_status(workflow_id)
            
            if not result.success:
                return result
            
            status = result.data
            
            if progress_callback:
                progress_callback(status)
            
            if status["status"] in ["completed", "failed", "cancelled", "partially_failed"]:
                return Result.ok(status)
            
            await asyncio.sleep(poll_interval)
        
        return Result.fail(f"Workflow {workflow_id} did not complete within {timeout}s", timeout=True)
    
    # Utility methods
    async def list_jobs(
        self,
        limit: int = 50,
        offset: int = 0,
        status: Optional[str] = None,
        queue_name: Optional[str] = None,
        created_after: Optional[datetime] = None
    ) -> Result[Dict[str, Any]]:
        """List jobs with filtering"""
        try:
            params = {"limit": limit, "offset": offset}
            
            if status:
                params["status"] = status
            if queue_name:
                params["queue_name"] = queue_name
            if created_after:
                params["created_after"] = created_after.isoformat()
            
            response = await self._request("GET", "/jobs", params=params)
            return Result.ok(response)
        except Exception as e:
            return Result.fail(str(e))
    
    async def list_workflows(
        self,
        limit: int = 50,
        offset: int = 0,
        status: Optional[str] = None,
        created_after: Optional[datetime] = None
    ) -> Result[Dict[str, Any]]:
        """List workflows with filtering"""
        try:
            params = {"limit": limit, "offset": offset}
            
            if status:
                params["status"] = status
            if created_after:
                params["created_after"] = created_after.isoformat()
            
            response = await self._request("GET", "/workflows", params=params)
            return Result.ok(response)
        except Exception as e:
            return Result.fail(str(e))
    
    async def get_stats(self) -> Result[Dict[str, Any]]:
        """Get system statistics"""
        try:
            response = await self._request("GET", "/stats")
            return Result.ok(response)
        except Exception as e:
            return Result.fail(str(e))
    
    async def health_check(self) -> Result[Dict[str, Any]]:
        """Check system health"""
        try:
            response = await self._request("GET", "/health")
            return Result.ok(response)
        except Exception as e:
            return Result.fail(str(e))
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get SDK metrics"""
        return self.metrics.copy()


# Synchronous wrapper for non-async environments
class QueueFlowClient:
    """
    Synchronous wrapper for QueueFlow SDK
    Use in non-async environments like Flask, Django, or scripts
    """
    
    def __init__(self, api_url: str, api_key: str, **kwargs):
        self.api_url = api_url
        self.api_key = api_key
        self.sdk_kwargs = kwargs
        self._loop: Optional[asyncio.AbstractEventLoop] = None
    
    def _get_loop(self) -> asyncio.AbstractEventLoop:
        """Get or create event loop"""
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            if self._loop is None or self._loop.is_closed():
                self._loop = asyncio.new_event_loop()
                asyncio.set_event_loop(self._loop)
            loop = self._loop
        return loop
    
    def _run_async(self, coro):
        """Run async function in sync context"""
        loop = self._get_loop()
        return loop.run_until_complete(coro)
    
    async def _execute_with_sdk(self, func_name: str, *args, **kwargs):
        """Execute SDK method"""
        async with QueueFlowSDK(self.api_url, self.api_key, **self.sdk_kwargs) as sdk:
            method = getattr(sdk, func_name)
            return await method(*args, **kwargs)
    
    def create_job(
        self,
        task_name: str,
        payload: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Result[str]:
        """Create job synchronously"""
        return self._run_async(
            self._execute_with_sdk("create_job", task_name, payload, **kwargs)
        )
    
    def get_job_status(self, job_id: str) -> Result[Dict[str, Any]]:
        """Get job status synchronously"""
        return self._run_async(
            self._execute_with_sdk("get_job_status", job_id)
        )
    
    def wait_for_job(self, job_id: str, **kwargs) -> Result[Dict[str, Any]]:
        """Wait for job synchronously"""
        return self._run_async(
            self._execute_with_sdk("wait_for_job", job_id, **kwargs)
        )
    
    def create_workflow(
        self,
        name: str,
        steps: List[WorkflowStep],
        **kwargs
    ) -> Result[str]:
        """Create workflow synchronously"""
        return self._run_async(
            self._execute_with_sdk("create_workflow", name, steps, **kwargs)
        )
    
    def get_workflow_status(self, workflow_id: str, **kwargs) -> Result[Dict[str, Any]]:
        """Get workflow status synchronously"""
        return self._run_async(
            self._execute_with_sdk("get_workflow_status", workflow_id, **kwargs)
        )
    
    def list_jobs(self, **kwargs) -> Result[Dict[str, Any]]:
        """List jobs synchronously"""
        return self._run_async(
            self._execute_with_sdk("list_jobs", **kwargs)
        )
    
    def get_stats(self) -> Result[Dict[str, Any]]:
        """Get stats synchronously"""
        return self._run_async(
            self._execute_with_sdk("get_stats")
        )
    
    def __del__(self):
        """Cleanup event loop"""
        if self._loop and not self._loop.is_closed():
            self._loop.close()


# Helper functions and utilities
def create_step(
    name: str,
    task_name: str,
    payload: Optional[Dict[str, Any]] = None,
    **kwargs
) -> WorkflowStep:
    """Helper to create workflow step"""
    return WorkflowStep(name=name, task_name=task_name, payload=payload or {}, **kwargs)


def parallel_steps(*steps: WorkflowStep) -> List[WorkflowStep]:
    """Helper to create parallel steps (no dependencies between them)"""
    return list(steps)


def sequential_steps(*steps: WorkflowStep) -> List[WorkflowStep]:
    """Helper to create sequential steps"""
    result = []
    for i, step in enumerate(steps):
        if i > 0:
            step.depends_on = [steps[i-1].name]
        result.append(step)
    return result


# Decorator for task handlers
def task_handler(
    name: Optional[str] = None,
    timeout: Optional[int] = None,
    retries: Optional[int] = None
):
    """Decorator to mark a function as a task handler"""
    def decorator(func: Callable) -> Callable:
        # Store metadata on the function
        func._task_name = name or func.__name__
        func._task_timeout = timeout
        func._task_retries = retries
        func._is_task_handler = True
        return func
    return decorator


# Middleware example
def logging_middleware(next_handler: TaskHandler) -> TaskHandler:
    """Example middleware that logs task execution"""
    @wraps(next_handler)
    async def wrapper(payload: Dict[str, Any], **kwargs) -> Optional[Dict[str, Any]]:
        start_time = time.time()
        task_id = kwargs.get("task_id", "unknown")
        
        logging.info(f"Task {task_id} starting with payload: {payload}")
        
        try:
            result = await next_handler(payload, **kwargs)
            duration = time.time() - start_time
            logging.info(f"Task {task_id} completed in {duration:.2f}s")
            return result
        except Exception as e:
            duration = time.time() - start_time
            logging.error(f"Task {task_id} failed after {duration:.2f}s: {e}")
            raise
    
    return wrapper


# Metrics middleware
def metrics_middleware(metrics_collector) -> MiddlewareFunc:
    """Middleware that collects task metrics"""
    def middleware(next_handler: TaskHandler) -> TaskHandler:
        @wraps(next_handler)
        async def wrapper(payload: Dict[str, Any], **kwargs) -> Optional[Dict[str, Any]]:
            task_name = kwargs.get("task_name", "unknown")
            start_time = time.time()
            
            try:
                result = await next_handler(payload, **kwargs)
                duration = time.time() - start_time
                
                metrics_collector.record_task_success(task_name, duration)
                return result
            except Exception as e:
                duration = time.time() - start_time
                metrics_collector.record_task_failure(task_name, duration, str(e))
                raise
        
        return wrapper
    return middleware