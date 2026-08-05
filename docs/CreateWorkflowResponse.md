# CreateWorkflowResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**workflow_id** | **str** |  | 

## Example

```python
from queueflow.models.create_workflow_response import CreateWorkflowResponse

# TODO update the JSON string below
json = "{}"
# create an instance of CreateWorkflowResponse from a JSON string
create_workflow_response_instance = CreateWorkflowResponse.from_json(json)
# print the JSON string representation of the object
print(CreateWorkflowResponse.to_json())

# convert the object into a dict
create_workflow_response_dict = create_workflow_response_instance.to_dict()
# create an instance of CreateWorkflowResponse from a dict
create_workflow_response_from_dict = CreateWorkflowResponse.from_dict(create_workflow_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


