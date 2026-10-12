# StepCondition

A predicate over the workflow context, evaluated when a step becomes ready. Exactly one of `path`, `all`, `any` or `not` is set. A leaf names a dotted `path` into the context (step results live under their step name, so `validate.ok` is the `ok` key of the `validate` step's result) and compares it with `value` using `op`. A false condition skips the step with the reason `condition not met`; its dependents still run, seeing no result for it.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**all** | [**List[StepCondition]**](StepCondition.md) | True when every member is true. | [optional] 
**any** | [**List[StepCondition]**](StepCondition.md) | True when at least one member is true. | [optional] 
**var_not** | [**StepCondition**](StepCondition.md) |  | [optional] 
**op** | [**ConditionOp**](ConditionOp.md) |  | [optional] 
**path** | **str** |  | [optional] 
**value** | **object** |  | [optional] 

## Example

```python
from queueflow.models.step_condition import StepCondition

# TODO update the JSON string below
json = "{}"
# create an instance of StepCondition from a JSON string
step_condition_instance = StepCondition.from_json(json)
# print the JSON string representation of the object
print(StepCondition.to_json())

# convert the object into a dict
step_condition_dict = step_condition_instance.to_dict()
# create an instance of StepCondition from a dict
step_condition_from_dict = StepCondition.from_dict(step_condition_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


