# Workflow

A workflow instance and its steps.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**completed_at** | **datetime** |  | [optional] 
**context** | **Dict[str, object]** | Accumulated step results, keyed by step name. Passed to downstream steps under the &#x60;_context&#x60; payload key. | [optional] 
**created_at** | **datetime** |  | 
**deadline_at** | **datetime** | When the janitor fails the workflow if it is still running (set from &#x60;timeout_secs&#x60;; pushed forward by a retry). | [optional] 
**error_message** | **str** | Why the workflow ended &#x60;failed&#x60; or &#x60;cancelled&#x60;, when known (an upstream failure, a timeout, a user cancel). | [optional] 
**id** | **str** |  | 
**metadata** | **Dict[str, object]** |  | [optional] 
**name** | **str** |  | 
**parent_step_name** | **str** | The parent&#39;s step that spawned this child. | [optional] 
**parent_workflow_id** | **str** | Set on a child workflow spawned by a sub-workflow step. | [optional] 
**retry_count** | **int** | How many times &#x60;POST /workflows/{id}/retry&#x60; re-ran this workflow. | [optional] 
**started_at** | **datetime** |  | [optional] 
**status** | [**WorkflowStatus**](WorkflowStatus.md) |  | 
**steps** | [**List[WorkflowStep]**](WorkflowStep.md) |  | 
**tenant_id** | **str** |  | [optional] 
**timeout_secs** | **int** | The whole-workflow time budget it was created with, if any. | [optional] 

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


