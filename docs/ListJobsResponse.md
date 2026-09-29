# ListJobsResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**has_more** | **bool** |  | 
**jobs** | [**List[Job]**](Job.md) |  | 
**limit** | **int** |  | 
**next_cursor** | **str** | Opaque keyset cursor for the next page (present when &#x60;has_more&#x60;). Pass it back as &#x60;cursor&#x60; to continue where this page ended; cheaper than deep OFFSET paging. | [optional] 
**offset** | **int** |  | 
**total** | **int** | Exact total match count. Only present when the request set &#x60;include_total&#x3D;true&#x60;; computing it costs a full count over the filtered set, so it is opt-in. | [optional] 

## Example

```python
from queueflow.models.list_jobs_response import ListJobsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ListJobsResponse from a JSON string
list_jobs_response_instance = ListJobsResponse.from_json(json)
# print the JSON string representation of the object
print(ListJobsResponse.to_json())

# convert the object into a dict
list_jobs_response_dict = list_jobs_response_instance.to_dict()
# create an instance of ListJobsResponse from a dict
list_jobs_response_from_dict = ListJobsResponse.from_dict(list_jobs_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


