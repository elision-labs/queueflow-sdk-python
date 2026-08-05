# Workflow

A workflow instance and its steps.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**completed_at** | **datetime** |  | [optional] 
**context** | **Dict[str, object]** | Accumulated step results, keyed by step name. Passed to downstream steps under the &#x60;_context&#x60; payload key. | [optional] 
**created_at** | **datetime** |  | 
**id** | **str** |  | 
**metadata** | **Dict[str, object]** |  | [optional] 
**name** | **str** |  | 
**started_at** | **datetime** |  | [optional] 
**status** | [**WorkflowStatus**](WorkflowStatus.md) |  | 
**steps** | [**List[WorkflowStep]**](WorkflowStep.md) |  | 
**tenant_id** | **str** |  | [optional] 

## Example

```python
from queueflow.models.workflow import Workflow

# TODO update the JSON string below
json = "{}"
# create an instance of Workflow from a JSON string
workflow_instance = Workflow.from_json(json)
# print the JSON string representation of the object
print(Workflow.to_json())

# convert the object into a dict
workflow_dict = workflow_instance.to_dict()
# create an instance of Workflow from a dict
workflow_from_dict = Workflow.from_dict(workflow_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


