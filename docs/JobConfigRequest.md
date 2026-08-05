# JobConfigRequest

Optional per-job configuration overrides.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**max_retries** | **int** |  | [optional] 
**priority** | **int** | Higher is claimed first within a queue (ties: oldest first). | [optional] 
**queue** | **str** | Override the destination queue. | [optional] 
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


