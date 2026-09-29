# WorkflowStepState

Runtime status of one workflow step (the live progress view).

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**job_id** | **str** | The job executing this step, once one has been scheduled. | [optional] 
**name** | **str** | The step&#39;s name (its address within the workflow). | 
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


