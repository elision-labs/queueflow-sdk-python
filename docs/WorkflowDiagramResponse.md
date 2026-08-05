# WorkflowDiagramResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**diagram** | **str** | The diagram document (Mermaid &#x60;graph TD&#x60;). | 
**format** | **str** | Diagram source format. Always &#x60;mermaid&#x60; today. | 

## Example

```python
from queueflow.models.workflow_diagram_response import WorkflowDiagramResponse

# TODO update the JSON string below
json = "{}"
# create an instance of WorkflowDiagramResponse from a JSON string
workflow_diagram_response_instance = WorkflowDiagramResponse.from_json(json)
# print the JSON string representation of the object
print(WorkflowDiagramResponse.to_json())

# convert the object into a dict
workflow_diagram_response_dict = workflow_diagram_response_instance.to_dict()
# create an instance of WorkflowDiagramResponse from a dict
workflow_diagram_response_from_dict = WorkflowDiagramResponse.from_dict(workflow_diagram_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


