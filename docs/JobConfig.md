# JobConfig

Per-job execution configuration. All durations are in seconds.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**jitter_factor** | **float** | Optional jitter in &#x60;0.0..&#x3D;1.0&#x60;. &#x60;0.1&#x60; &#x3D;&gt; +/-10% randomization of each retry delay, which spreads out thundering-herd retries. | [optional] 
**max_retries** | **int** |  | 
**priority** | **int** | Higher is claimed first within a queue; ties break on &#x60;scheduled_at&#x60;, then &#x60;created_at&#x60;. | 
**retry_backoff** | [**BackoffStrategy**](BackoffStrategy.md) |  | [optional] 
**retry_delay_secs** | **int** |  | 
**retry_max_delay_secs** | **int** |  | 
**timeout_secs** | **int** |  | 

## Example

```python
from queueflow.models.job_config import JobConfig

# TODO update the JSON string below
json = "{}"
# create an instance of JobConfig from a JSON string
job_config_instance = JobConfig.from_json(json)
# print the JSON string representation of the object
print(JobConfig.to_json())

# convert the object into a dict
job_config_dict = job_config_instance.to_dict()
# create an instance of JobConfig from a dict
job_config_from_dict = JobConfig.from_dict(job_config_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


