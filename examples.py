"""
QueueFlow Python SDK Examples
"""

import asyncio
from datetime import datetime
from queueflow import (
    QueueFlowClient, QueueFlowClientSync,
    JobConfig, WorkflowStep, JobStatus,
    create_step
)


async def async_examples():
    """Async examples using the QueueFlow client"""
    
    # Initialize client
    async with QueueFlowClient("http://localhost:8080", "your-api-key") as client:
        
        # Example 1: Create a simple job
        job_id = await client.create_job(
            "send_email",
            {
                "to": "user@example.com",
                "subject": "Welcome!",
                "body": "Thank you for signing up."
            }
        )
        print(f"Created job: {job_id}")
        
        # Example 2: Create a job with configuration
        job_id2 = await client.create_job(
            "process_data",
            {
                "file_url": "https://example.com/data.csv",
                "format": "csv"
            },
            config=JobConfig(
                priority=5,
                max_retries=5,
                timeout=600,  # 10 minutes
                queue="high-priority"
            )
        )
        print(f"Created high-priority job: {job_id2}")
        
        # Example 3: Create batch jobs
        batch_jobs = [
            {
                "task_name": "resize_image",
                "payload": {
                    "image_url": f"https://example.com/image{i}.jpg",
                    "width": 800,
                    "height": 600
                }
            }
            for i in range(1, 6)
        ]
        
        job_ids = await client.create_batch_jobs(batch_jobs)
        print(f"Created batch jobs: {job_ids}")
        
        # Example 4: Create a workflow
        steps = [
            WorkflowStep(
                name="download",
                task_name="download_file",
                payload={"url": "https://example.com/video.mp4"}
            ),
            WorkflowStep(
                name="transcode",
                task_name="transcode_video",
                payload={"format": "webm"},
                depends_on=["download"]
            ),
            WorkflowStep(
                name="thumbnail",
                task_name="generate_thumbnail",
                payload={},
                depends_on=["download"]
            ),
            WorkflowStep(
                name="upload",
                task_name="upload_to_cdn",
                payload={},
                depends_on=["transcode", "thumbnail"]
            )
        ]
        
        workflow_id = await client.create_workflow("video_processing", steps)
        print(f"Created workflow: {workflow_id}")
        
        # Example 5: Monitor job status
        job = await client.get_job(job_id)
        print(f"Job status: {job.status}")
        print(f"Created at: {job.created_at}")
        
        # Example 6: Wait for job completion with timeout
        try:
            completed_job = await client.wait_for_job(job_id, timeout=300)
            print(f"Job completed with status: {completed_job.status}")
            if completed_job.result:
                print(f"Result: {completed_job.result}")
        except Exception as e:
            print(f"Job failed or timed out: {e}")
        
        # Example 7: List jobs with filtering
        jobs_list = await client.list_jobs(
            limit=10,
            status="pending",
            queue="default"
        )
        print(f"Found {len(jobs_list.items)} pending jobs (total: {jobs_list.total})")
        
        # Example 8: Cancel a job
        cancelled = await client.cancel_job(job_id2)
        if cancelled:
            print(f"Successfully cancelled job: {job_id2}")
        
        # Example 9: Get job logs
        logs = await client.get_job_logs(job_id)
        for log in logs:
            print(f"Log: {log}")
        
        # Example 10: Monitor workflow
        workflow = await client.get_workflow(workflow_id)
        print(f"Workflow status: {workflow.status}")
        
        # Example 11: Wait for workflow completion
        try:
            completed_workflow = await client.wait_for_workflow(workflow_id, timeout=600)
            print(f"Workflow completed with status: {completed_workflow.status}")
        except Exception as e:
            print(f"Workflow failed or timed out: {e}")
        
        # Example 12: Health check
        health = await client.health_check()
        print(f"System health: {health}")
        
        # Example 13: Get statistics
        stats = await client.get_stats()
        print(f"System stats: {stats}")
        
        # Example 14: Create job with idempotency key
        idempotent_job_id = await client.create_job(
            "important_task",
            {"data": "critical"},
            idempotency_key="unique-operation-123"
        )
        print(f"Created idempotent job: {idempotent_job_id}")
        
        # Example 15: Create workflow with helper function
        steps_with_helper = [
            create_step("step1", "task1", {"data": 1}),
            create_step("step2", "task2", {"data": 2}, depends_on=["step1"]),
            create_step("step3", "task3", {"data": 3}, depends_on=["step1", "step2"])
        ]
        
        workflow_id2 = await client.create_workflow("complex_workflow", steps_with_helper)
        print(f"Created complex workflow: {workflow_id2}")


def sync_examples():
    """Synchronous examples using the sync wrapper"""
    
    # Initialize sync client
    client = QueueFlowClientSync("http://localhost:8080", "your-api-key")
    
    # Example 1: Create and wait for a job synchronously
    job_id = client.create_job(
        "send_email",
        {
            "to": "admin@example.com",
            "subject": "Daily Report",
            "body": "Here is your daily report."
        }
    )
    print(f"Created job (sync): {job_id}")
    
    # Example 2: Wait for job completion
    job = client.wait_for_job(job_id, timeout=300)
    print(f"Job completed (sync): {job.status}")
    
    # Example 3: List jobs
    jobs = client.list_jobs(limit=5)
    print(f"Recent jobs (sync): {len(jobs.items)}")
    
    # Example 4: Health check
    health = client.health_check()
    print(f"Health check (sync): {health}")


def workflow_examples():
    """Advanced workflow examples"""
    
    # Example: Data processing pipeline
    data_pipeline = [
        WorkflowStep(
            name="fetch_data",
            task_name="fetch_from_api",
            payload={"endpoint": "https://api.example.com/data"}
        ),
        WorkflowStep(
            name="validate",
            task_name="validate_data",
            payload={"schema": "v2"},
            depends_on=["fetch_data"]
        ),
        WorkflowStep(
            name="transform",
            task_name="transform_data",
            payload={"format": "parquet"},
            depends_on=["validate"]
        ),
        WorkflowStep(
            name="store",
            task_name="store_to_warehouse",
            payload={"table": "processed_data"},
            depends_on=["transform"]
        ),
        WorkflowStep(
            name="notify",
            task_name="send_notification",
            payload={"channel": "slack"},
            depends_on=["store"]
        )
    ]
    
    # Example: Parallel processing workflow
    parallel_workflow = [
        WorkflowStep(
            name="split",
            task_name="split_file",
            payload={"chunks": 4}
        ),
        # Parallel processing steps
        WorkflowStep(
            name="process_chunk_1",
            task_name="process_chunk",
            payload={"chunk_id": 1},
            depends_on=["split"]
        ),
        WorkflowStep(
            name="process_chunk_2",
            task_name="process_chunk",
            payload={"chunk_id": 2},
            depends_on=["split"]
        ),
        WorkflowStep(
            name="process_chunk_3",
            task_name="process_chunk",
            payload={"chunk_id": 3},
            depends_on=["split"]
        ),
        WorkflowStep(
            name="process_chunk_4",
            task_name="process_chunk",
            payload={"chunk_id": 4},
            depends_on=["split"]
        ),
        # Merge results
        WorkflowStep(
            name="merge",
            task_name="merge_results",
            payload={},
            depends_on=[
                "process_chunk_1",
                "process_chunk_2",
                "process_chunk_3",
                "process_chunk_4"
            ]
        )
    ]
    
    return data_pipeline, parallel_workflow


if __name__ == "__main__":
    # Run async examples
    print("Running async examples...")
    asyncio.run(async_examples())
    
    print("\n" + "="*50 + "\n")
    
    # Run sync examples
    print("Running sync examples...")
    sync_examples()
    
    print("\n" + "="*50 + "\n")
    
    # Show workflow examples
    print("Workflow examples:")
    data_pipeline, parallel_workflow = workflow_examples()
    print(f"Data pipeline steps: {len(data_pipeline)}")
    print(f"Parallel workflow steps: {len(parallel_workflow)}")