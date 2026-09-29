# ListCronsResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**crons** | [**List[CronSchedule]**](CronSchedule.md) |  | 
**has_more** | **bool** |  | 
**limit** | **int** |  | 
**next_cursor** | **str** | Opaque keyset cursor for the next page (present when &#x60;has_more&#x60;). Pass it back as &#x60;cursor&#x60; to continue where this page ended; cheaper than deep OFFSET paging. | [optional] 
**offset** | **int** |  | 
**total** | **int** | Exact total match count; only present when &#x60;include_total&#x3D;true&#x60;. | [optional] 

## Example

```python
from queueflow.models.list_crons_response import ListCronsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ListCronsResponse from a JSON string
list_crons_response_instance = ListCronsResponse.from_json(json)
# print the JSON string representation of the object
print(ListCronsResponse.to_json())

# convert the object into a dict
list_crons_response_dict = list_crons_response_instance.to_dict()
# create an instance of ListCronsResponse from a dict
list_crons_response_from_dict = ListCronsResponse.from_dict(list_crons_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


