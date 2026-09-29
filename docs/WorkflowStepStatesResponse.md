# WorkflowStepStatesResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**steps** | [**List[WorkflowStepState]**](WorkflowStepState.md) | One entry per step, in declaration order. | 

## Example

```python
from queueflow.models.workflow_step_states_response import WorkflowStepStatesResponse

# TODO update the JSON string below
json = "{}"
# create an instance of WorkflowStepStatesResponse from a JSON string
workflow_step_states_response_instance = WorkflowStepStatesResponse.from_json(json)
# print the JSON string representation of the object
print(WorkflowStepStatesResponse.to_json())

# convert the object into a dict
workflow_step_states_response_dict = workflow_step_states_response_instance.to_dict()
# create an instance of WorkflowStepStatesResponse from a dict
workflow_step_states_response_from_dict = WorkflowStepStatesResponse.from_dict(workflow_step_states_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


