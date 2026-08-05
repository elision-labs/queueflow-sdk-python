# CreateJobResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**job_id** | **str** |  | 

## Example

```python
from queueflow.models.create_job_response import CreateJobResponse

# TODO update the JSON string below
json = "{}"
# create an instance of CreateJobResponse from a JSON string
create_job_response_instance = CreateJobResponse.from_json(json)
# print the JSON string representation of the object
print(CreateJobResponse.to_json())

# convert the object into a dict
create_job_response_dict = create_job_response_instance.to_dict()
# create an instance of CreateJobResponse from a dict
create_job_response_from_dict = CreateJobResponse.from_dict(create_job_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


