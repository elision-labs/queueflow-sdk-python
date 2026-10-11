# ReplayDeadLettersRequest

Which dead letters a bulk replay applies to. Every field is optional; an empty body replays the caller's oldest unreplayed dead letters up to `limit`.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**created_after** | **datetime** | Only entries created at or after this instant (RFC 3339, inclusive). | [optional] 
**created_before** | **datetime** | Only entries created strictly before this instant (RFC 3339, exclusive). | [optional] 
**limit** | **int** | Consider at most this many entries (oldest first). Default 100; the maximum is the server&#39;s batch limit (&#x60;--max-batch&#x60;). | [optional] 
**queue** | **str** | Only dead letters from this queue. | [optional] 
**task_name** | **str** | Only dead letters for this task. | [optional] 

## Example

```python
from queueflow.models.replay_dead_letters_request import ReplayDeadLettersRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ReplayDeadLettersRequest from a JSON string
replay_dead_letters_request_instance = ReplayDeadLettersRequest.from_json(json)
# print the JSON string representation of the object
print(ReplayDeadLettersRequest.to_json())

# convert the object into a dict
replay_dead_letters_request_dict = replay_dead_letters_request_instance.to_dict()
# create an instance of ReplayDeadLettersRequest from a dict
replay_dead_letters_request_from_dict = ReplayDeadLettersRequest.from_dict(replay_dead_letters_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


