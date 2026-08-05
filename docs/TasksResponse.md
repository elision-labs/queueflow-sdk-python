# TasksResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**tasks** | **List[str]** |  | 

## Example

```python
from queueflow.models.tasks_response import TasksResponse

# TODO update the JSON string below
json = "{}"
# create an instance of TasksResponse from a JSON string
tasks_response_instance = TasksResponse.from_json(json)
# print the JSON string representation of the object
print(TasksResponse.to_json())

# convert the object into a dict
tasks_response_dict = tasks_response_instance.to_dict()
# create an instance of TasksResponse from a dict
tasks_response_from_dict = TasksResponse.from_dict(tasks_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


