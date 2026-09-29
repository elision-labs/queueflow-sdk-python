# ListDeadLettersResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**dead_letters** | [**List[DeadLetter]**](DeadLetter.md) |  | 
**has_more** | **bool** |  | 
**limit** | **int** |  | 
**next_cursor** | **str** | Opaque keyset cursor for the next page (present when &#x60;has_more&#x60;). Pass it back as &#x60;cursor&#x60; to continue where this page ended; cheaper than deep OFFSET paging. | [optional] 
**offset** | **int** |  | 
**total** | **int** | Exact total match count; only present when &#x60;include_total&#x3D;true&#x60;. | [optional] 

## Example

```python
from queueflow.models.list_dead_letters_response import ListDeadLettersResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ListDeadLettersResponse from a JSON string
list_dead_letters_response_instance = ListDeadLettersResponse.from_json(json)
# print the JSON string representation of the object
print(ListDeadLettersResponse.to_json())

# convert the object into a dict
list_dead_letters_response_dict = list_dead_letters_response_instance.to_dict()
# create an instance of ListDeadLettersResponse from a dict
list_dead_letters_response_from_dict = ListDeadLettersResponse.from_dict(list_dead_letters_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


