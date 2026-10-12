# WorkflowEvent

One `status` event of the workflow stream: the workflow's status and every step's live state.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**error_message** | **str** |  | [optional] 
**status** | [**WorkflowStatus**](WorkflowStatus.md) |  | 
**steps** | [**List[WorkflowStepState]**](WorkflowStepState.md) |  | 
**workflow_id** | **str** |  | 

## Example

```python
from queueflow.models.workflow_event import WorkflowEvent

# TODO update the JSON string below
json = "{}"
# create an instance of WorkflowEvent from a JSON string
workflow_event_instance = WorkflowEvent.from_json(json)
# print the JSON string representation of the object
print(WorkflowEvent.to_json())

# convert the object into a dict
workflow_event_dict = workflow_event_instance.to_dict()
# create an instance of WorkflowEvent from a dict
workflow_event_from_dict = WorkflowEvent.from_dict(workflow_event_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


