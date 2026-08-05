# LeaseJobsRequest

Body for `POST /api/v1/queues/{queue}/lease`.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**lease_secs** | **int** | Lease duration in seconds (1..&#x3D;3600, default 30). Heartbeat to extend. | [optional] 
**max_jobs** | **int** | Maximum jobs to lease in one call (1..&#x3D;100, default 1). | [optional] 
**wait_secs** | **int** | Long-poll wait when the queue is empty, in seconds (0..&#x3D;30, default 0). | [optional] 

## Example

```python
from queueflow.models.lease_jobs_request import LeaseJobsRequest

# TODO update the JSON string below
json = "{}"
# create an instance of LeaseJobsRequest from a JSON string
lease_jobs_request_instance = LeaseJobsRequest.from_json(json)
# print the JSON string representation of the object
print(LeaseJobsRequest.to_json())

# convert the object into a dict
lease_jobs_request_dict = lease_jobs_request_instance.to_dict()
# create an instance of LeaseJobsRequest from a dict
lease_jobs_request_from_dict = LeaseJobsRequest.from_dict(lease_jobs_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


