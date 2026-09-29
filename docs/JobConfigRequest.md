# JobConfigRequest

Optional per-job configuration overrides.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**jitter_factor** | **float** | Retry-delay jitter in &#x60;0.0..&#x3D;1.0&#x60; (e.g. &#x60;0.1&#x60; &#x3D; +/-10%). | [optional] 
**max_retries** | **int** |  | [optional] 
**priority** | **int** | Higher is claimed first within a queue (ties: oldest first). | [optional] 
**queue** | **str** | Override the destination queue. | [optional] 
**retry_backoff** | [**BackoffStrategy**](BackoffStrategy.md) | How retry delays grow between attempts (default exponential). | [optional] 
**retry_delay_secs** | **int** | Base retry delay, in seconds. | [optional] 
**retry_max_delay_secs** | **int** | Upper bound on any computed retry delay, in seconds. | [optional] 
**timeout** | **int** | Per-attempt timeout, in seconds. | [optional] 

## Example

```python
from queueflow.models.job_config_request import JobConfigRequest

# TODO update the JSON string below
json = "{}"
# create an instance of JobConfigRequest from a JSON string
job_config_request_instance = JobConfigRequest.from_json(json)
# print the JSON string representation of the object
print(JobConfigRequest.to_json())

# convert the object into a dict
job_config_request_dict = job_config_request_instance.to_dict()
# create an instance of JobConfigRequest from a dict
job_config_request_from_dict = JobConfigRequest.from_dict(job_config_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


