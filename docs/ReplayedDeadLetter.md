# ReplayedDeadLetter

One dead letter's outcome in a bulk replay.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**dead_letter_id** | **int** |  | 
**error** | **str** | Why it did not, for example the original job was purged by retention. | [optional] 
**job_id** | **str** | The fresh job, when the replay succeeded. | [optional] 

## Example

```python
from queueflow.models.replayed_dead_letter import ReplayedDeadLetter

# TODO update the JSON string below
json = "{}"
# create an instance of ReplayedDeadLetter from a JSON string
replayed_dead_letter_instance = ReplayedDeadLetter.from_json(json)
# print the JSON string representation of the object
print(ReplayedDeadLetter.to_json())

# convert the object into a dict
replayed_dead_letter_dict = replayed_dead_letter_instance.to_dict()
# create an instance of ReplayedDeadLetter from a dict
replayed_dead_letter_from_dict = ReplayedDeadLetter.from_dict(replayed_dead_letter_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


