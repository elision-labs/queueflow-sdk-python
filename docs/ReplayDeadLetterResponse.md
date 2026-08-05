# ReplayDeadLetterResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**job_id** | **str** | The fresh job created from the dead-lettered one. | 

## Example

```python
from queueflow.models.replay_dead_letter_response import ReplayDeadLetterResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ReplayDeadLetterResponse from a JSON string
replay_dead_letter_response_instance = ReplayDeadLetterResponse.from_json(json)
# print the JSON string representation of the object
print(ReplayDeadLetterResponse.to_json())

# convert the object into a dict
replay_dead_letter_response_dict = replay_dead_letter_response_instance.to_dict()
# create an instance of ReplayDeadLetterResponse from a dict
replay_dead_letter_response_from_dict = ReplayDeadLetterResponse.from_dict(replay_dead_letter_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


