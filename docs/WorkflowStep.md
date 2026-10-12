# WorkflowStep

A node in a workflow DAG. Steps are addressed by their unique `name`; `depends_on` lists the names of steps that must complete first.  A step is one of three kinds: a plain task (`task_name`), a fan-out (`task_name` plus `fan_out`), or a sub-workflow (`workflow`, in which case `task_name` may be empty). `when` gates any kind on the context.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**config** | [**JobConfig**](JobConfig.md) |  | [optional] 
**depends_on** | **List[str]** |  | [optional] 
**fan_out** | [**FanOut**](FanOut.md) | Run the task once per element of an array in the context. | [optional] 
**metadata** | **Dict[str, object]** |  | [optional] 
**name** | **str** |  | 
**on_failure** | [**OnFailure**](OnFailure.md) |  | [optional] 
**on_success** | [**OnSuccess**](OnSuccess.md) |  | [optional] 
**payload** | **Dict[str, object]** |  | [optional] 
**queue** | **str** | Queue for this step&#39;s job(s); the server&#39;s default queue when absent. | [optional] 
**task_name** | **str** | The task handler to run. May be omitted for a sub-workflow step. | [optional] 
**when** | [**StepCondition**](StepCondition.md) | Run only when this condition holds against the workflow context at the moment the step becomes ready; otherwise the step is skipped with reason &#x60;condition not met&#x60; and its dependents proceed. | [optional] 
**workflow** | [**CreateWorkflowRequest**](CreateWorkflowRequest.md) | Run an inline child workflow instead of a task. The child&#39;s context is its own declared context plus this step&#39;s payload, with the parent&#39;s context under &#x60;_parent&#x60;; the step&#39;s result is the child&#39;s final context. | [optional] 

## Example

```python
from queueflow.models.workflow_step import WorkflowStep

# TODO update the JSON string below
json = "{}"
# create an instance of WorkflowStep from a JSON string
workflow_step_instance = WorkflowStep.from_json(json)
# print the JSON string representation of the object
print(WorkflowStep.to_json())

# convert the object into a dict
workflow_step_dict = workflow_step_instance.to_dict()
# create an instance of WorkflowStep from a dict
workflow_step_from_dict = WorkflowStep.from_dict(workflow_step_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


