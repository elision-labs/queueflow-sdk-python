# WorkflowStep

A node in a workflow DAG. Steps are addressed by their unique `name`; `depends_on` lists the names of steps that must complete first.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**config** | [**JobConfig**](JobConfig.md) |  | [optional] 
**depends_on** | **List[str]** |  | [optional] 
**metadata** | **Dict[str, object]** |  | [optional] 
**name** | **str** |  | 
**on_failure** | [**OnFailure**](OnFailure.md) |  | [optional] 
**on_success** | [**OnSuccess**](OnSuccess.md) |  | [optional] 
**payload** | **Dict[str, object]** |  | [optional] 
**task_name** | **str** |  | 

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


