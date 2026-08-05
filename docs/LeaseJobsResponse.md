# LeaseJobsResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**jobs** | [**List[LeasedJob]**](LeasedJob.md) |  | 

## Example

```python
from queueflow.models.lease_jobs_response import LeaseJobsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of LeaseJobsResponse from a JSON string
lease_jobs_response_instance = LeaseJobsResponse.from_json(json)
# print the JSON string representation of the object
print(LeaseJobsResponse.to_json())

# convert the object into a dict
lease_jobs_response_dict = lease_jobs_response_instance.to_dict()
# create an instance of LeaseJobsResponse from a dict
lease_jobs_response_from_dict = LeaseJobsResponse.from_dict(lease_jobs_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


