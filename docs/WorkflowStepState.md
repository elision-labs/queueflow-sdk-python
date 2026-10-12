# WorkflowStepState

Runtime status of one workflow step (the live progress view).

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**child_workflow_id** | **str** | The child workflow of a sub-workflow step, once spawned. | [optional] 
**completed_at** | **datetime** | When the step reached a terminal status. | [optional] 
**error** | **str** | Why the step failed, was skipped (&#x60;condition not met&#x60; for a false &#x60;when&#x60;) or was cancelled. | [optional] 
**fan_out** | [**FanOutProgress**](FanOutProgress.md) | Progress of a fan-out step&#39;s children, once spawned. | [optional] 
**job_id** | **str** | The job executing this step, once one has been scheduled (the first child, for a fan-out). | [optional] 
**name** | **str** | The step&#39;s name (its address within the workflow). | 
**started_at** | **datetime** | When the step was scheduled (its job or child workflow created). | [optional] 
**status** | [**StepStatus**](StepStatus.md) |  | 

## Example

```python
from queueflow.models.workflow_step_state import WorkflowStepState

# TODO update the JSON string below
json = "{}"
# create an instance of WorkflowStepState from a JSON string
workflow_step_state_instance = WorkflowStepState.from_json(json)
# print the JSON string representation of the object
print(WorkflowStepState.to_json())

# convert the object into a dict
workflow_step_state_dict = workflow_step_state_instance.to_dict()
# create an instance of WorkflowStepState from a dict
workflow_step_state_from_dict = WorkflowStepState.from_dict(workflow_step_state_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


