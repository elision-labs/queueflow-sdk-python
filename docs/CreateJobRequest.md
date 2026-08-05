# CreateJobRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**config** | [**JobConfigRequest**](JobConfigRequest.md) |  | [optional] 
**payload** | **Dict[str, object]** | Arbitrary JSON object passed to the handler. | [optional] 
**run_at** | **datetime** | Don&#39;t run before this instant (RFC 3339). The job is created immediately but stays invisible to workers until then. | [optional] 
**task_name** | **str** | The registered task handler to invoke. | 

## Example

```python
from queueflow.models.create_job_request import CreateJobRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateJobRequest from a JSON string
create_job_request_instance = CreateJobRequest.from_json(json)
# print the JSON string representation of the object
print(CreateJobRequest.to_json())

# convert the object into a dict
create_job_request_dict = create_job_request_instance.to_dict()
# create an instance of CreateJobRequest from a dict
create_job_request_from_dict = CreateJobRequest.from_dict(create_job_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


