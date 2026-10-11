# CancelJobsResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**cancelled** | **int** | How many jobs this call cancelled. Less than &#x60;limit&#x60; means the matching set is exhausted (jobs finishing concurrently are left as they ended, never overwritten). | 

## Example

```python
from queueflow.models.cancel_jobs_response import CancelJobsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of CancelJobsResponse from a JSON string
cancel_jobs_response_instance = CancelJobsResponse.from_json(json)
# print the JSON string representation of the object
print(CancelJobsResponse.to_json())

# convert the object into a dict
cancel_jobs_response_dict = cancel_jobs_response_instance.to_dict()
# create an instance of CancelJobsResponse from a dict
cancel_jobs_response_from_dict = CancelJobsResponse.from_dict(cancel_jobs_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


