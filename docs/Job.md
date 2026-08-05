# Job

A single unit of work.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**completed_at** | **datetime** |  | [optional] 
**config** | [**JobConfig**](JobConfig.md) |  | 
**created_at** | **datetime** |  | 
**delivery_count** | **int** | How many times this job has been claimed (delivered to a worker). Greater than &#x60;retry_count + 1&#x60; means a lease expired without a report — i.e. a worker crashed mid-run. | [optional] 
**error_message** | **str** |  | [optional] 
**id** | **str** |  | 
**idempotency_key** | **str** | Client-supplied key that makes job creation idempotent per tenant: re-submitting the same key returns the original job instead of creating a duplicate. | [optional] 
**metadata** | **Dict[str, object]** |  | [optional] 
**next_retry_at** | **datetime** | When this job&#39;s next retry becomes claimable (mirrors &#x60;scheduled_at&#x60; while the job is &#x60;retrying&#x60;; kept for audit/inspection). | [optional] 
**payload** | **Dict[str, object]** |  | [optional] 
**queue_name** | **str** |  | 
**result** | **Dict[str, object]** |  | [optional] 
**retry_count** | **int** |  | 
**scheduled_at** | **datetime** | When the job becomes claimable. &#x60;created_at&#x60; for immediate jobs, the requested &#x60;run_at&#x60; for scheduled jobs, and the next backoff instant while retrying — the durable delay lives in the row itself. | 
**started_at** | **datetime** |  | [optional] 
**status** | [**JobStatus**](JobStatus.md) |  | 
**task_name** | **str** |  | 
**tenant_id** | **str** |  | [optional] 
**workflow_id** | **str** |  | [optional] 
**workflow_step_id** | **str** | The owning workflow step&#39;s name (steps are addressed by name). | [optional] 

## Example

```python
from queueflow.models.job import Job

# TODO update the JSON string below
json = "{}"
# create an instance of Job from a JSON string
job_instance = Job.from_json(json)
# print the JSON string representation of the object
print(Job.to_json())

# convert the object into a dict
job_dict = job_instance.to_dict()
# create an instance of Job from a dict
job_from_dict = Job.from_dict(job_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


