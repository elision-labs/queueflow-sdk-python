# QueuesResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**queues** | [**List[QueueStats]**](QueueStats.md) | One entry per queue the caller has enqueued to (since 0.5.0, whether or not it currently has jobs) or that currently has non-terminal jobs, sorted by name. | 

## Example

```python
from queueflow.models.queues_response import QueuesResponse

# TODO update the JSON string below
json = "{}"
# create an instance of QueuesResponse from a JSON string
queues_response_instance = QueuesResponse.from_json(json)
# print the JSON string representation of the object
print(QueuesResponse.to_json())

# convert the object into a dict
queues_response_dict = queues_response_instance.to_dict()
# create an instance of QueuesResponse from a dict
queues_response_from_dict = QueuesResponse.from_dict(queues_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


