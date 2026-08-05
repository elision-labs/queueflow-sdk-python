# HeartbeatRequest

Body for `POST /api/v1/jobs/{id}/heartbeat`.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**extend_secs** | **int** | New lease duration in seconds, measured from now (1..&#x3D;3600). | 
**lease_token** | **str** | The lease token returned by the lease call. | 

## Example

```python
from queueflow.models.heartbeat_request import HeartbeatRequest

# TODO update the JSON string below
json = "{}"
# create an instance of HeartbeatRequest from a JSON string
heartbeat_request_instance = HeartbeatRequest.from_json(json)
# print the JSON string representation of the object
print(HeartbeatRequest.to_json())

# convert the object into a dict
heartbeat_request_dict = heartbeat_request_instance.to_dict()
# create an instance of HeartbeatRequest from a dict
heartbeat_request_from_dict = HeartbeatRequest.from_dict(heartbeat_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


