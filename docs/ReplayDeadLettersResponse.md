# ReplayDeadLettersResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**replayed** | **int** | How many of &#x60;results&#x60; produced a job. | 
**results** | [**List[ReplayedDeadLetter]**](ReplayedDeadLetter.md) | Entries that were replayed (&#x60;job_id&#x60; set) or could not be (&#x60;error&#x60; set), oldest first. Entries already replayed are not listed. | 

## Example

```python
from queueflow.models.replay_dead_letters_response import ReplayDeadLettersResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ReplayDeadLettersResponse from a JSON string
replay_dead_letters_response_instance = ReplayDeadLettersResponse.from_json(json)
# print the JSON string representation of the object
print(ReplayDeadLettersResponse.to_json())

# convert the object into a dict
replay_dead_letters_response_dict = replay_dead_letters_response_instance.to_dict()
# create an instance of ReplayDeadLettersResponse from a dict
replay_dead_letters_response_from_dict = ReplayDeadLettersResponse.from_dict(replay_dead_letters_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


