# QueueControlResponse

Pause or resume outcome: the queue's live counts with its new flag.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**paused** | **bool** | Claims of the caller&#39;s jobs on this queue are paused. | 
**pending** | **int** | Claimable jobs of the caller waiting on this queue. | 
**queue** | **str** |  | 
**running** | **int** | Jobs of the caller still leased by workers. A paused queue is drained once this reaches zero. | 

## Example

```python
from queueflow.models.queue_control_response import QueueControlResponse

# TODO update the JSON string below
json = "{}"
# create an instance of QueueControlResponse from a JSON string
queue_control_response_instance = QueueControlResponse.from_json(json)
# print the JSON string representation of the object
print(QueueControlResponse.to_json())

# convert the object into a dict
queue_control_response_dict = queue_control_response_instance.to_dict()
# create an instance of QueueControlResponse from a dict
queue_control_response_from_dict = QueueControlResponse.from_dict(queue_control_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


