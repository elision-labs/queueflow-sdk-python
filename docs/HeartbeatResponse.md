# HeartbeatResponse

Response for `POST /api/v1/jobs/{id}/heartbeat`.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | [**JobStatus**](JobStatus.md) | The job&#39;s current status. &#x60;running&#x60; means the lease was extended; anything else (&#x60;cancelled&#x60;, &#x60;completed&#x60;, ...) means it was not, and the worker should stop working on the job. | 

## Example

```python
from queueflow.models.heartbeat_response import HeartbeatResponse

# TODO update the JSON string below
json = "{}"
# create an instance of HeartbeatResponse from a JSON string
heartbeat_response_instance = HeartbeatResponse.from_json(json)
# print the JSON string representation of the object
print(HeartbeatResponse.to_json())

# convert the object into a dict
heartbeat_response_dict = heartbeat_response_instance.to_dict()
# create an instance of HeartbeatResponse from a dict
heartbeat_response_from_dict = HeartbeatResponse.from_dict(heartbeat_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


