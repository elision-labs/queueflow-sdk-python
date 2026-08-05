# CompleteJobRequest

Body for `POST /api/v1/jobs/{id}/complete`.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**lease_token** | **str** | The lease token returned by the lease call. | 
**result** | **Dict[str, object]** | Handler result, recorded on the job and merged into workflow context. | [optional] 

## Example

```python
from queueflow.models.complete_job_request import CompleteJobRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CompleteJobRequest from a JSON string
complete_job_request_instance = CompleteJobRequest.from_json(json)
# print the JSON string representation of the object
print(CompleteJobRequest.to_json())

# convert the object into a dict
complete_job_request_dict = complete_job_request_instance.to_dict()
# create an instance of CompleteJobRequest from a dict
complete_job_request_from_dict = CompleteJobRequest.from_dict(complete_job_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


