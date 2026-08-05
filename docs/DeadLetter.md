# DeadLetter

A dead-lettered job: a terminal failure recorded for inspection and replay. The original job row remains (subject to retention); this entry captures why it died and, once replayed, which fresh job took its place.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**created_at** | **datetime** |  | 
**error_message** | **str** |  | [optional] 
**id** | **int** |  | 
**job_id** | **str** |  | 
**queue_name** | **str** |  | [optional] 
**reason** | **str** | Why the job dead-lettered: &#x60;max_attempts_exceeded&#x60;, &#x60;non_retryable&#x60;, or &#x60;handler_not_found&#x60;. | 
**replay_job_id** | **str** | The fresh job created by the replay. | [optional] 
**replayed_at** | **datetime** | Set once this entry has been replayed; a dead letter replays at most once. | [optional] 
**task_name** | **str** |  | [optional] 
**tenant_id** | **str** |  | [optional] 

## Example

```python
from queueflow.models.dead_letter import DeadLetter

# TODO update the JSON string below
json = "{}"
# create an instance of DeadLetter from a JSON string
dead_letter_instance = DeadLetter.from_json(json)
# print the JSON string representation of the object
print(DeadLetter.to_json())

# convert the object into a dict
dead_letter_dict = dead_letter_instance.to_dict()
# create an instance of DeadLetter from a dict
dead_letter_from_dict = DeadLetter.from_dict(dead_letter_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


