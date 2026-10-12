# FanOut

Dynamic fan-out: run the step's task once per element of the array found at `path` in the workflow context. Each child job receives the step payload plus the element under `item_key` and its position under `_index`. The step completes when every child has, with the result `{\"results\": [...]}` in element order; a failed child follows the step's `on_failure` policy.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**item_key** | **str** | Payload key the element is passed under (default &#x60;item&#x60;). | [optional] 
**max_items** | **int** | Upper bound on elements; more than this fails the step before any child runs. Default [&#x60;limits::MAX_FAN_OUT&#x60;]. | [optional] 
**path** | **str** | Dotted path into the context, for example &#x60;fetch.images&#x60;. | 

## Example

```python
from queueflow.models.fan_out import FanOut

# TODO update the JSON string below
json = "{}"
# create an instance of FanOut from a JSON string
fan_out_instance = FanOut.from_json(json)
# print the JSON string representation of the object
print(FanOut.to_json())

# convert the object into a dict
fan_out_dict = fan_out_instance.to_dict()
# create an instance of FanOut from a dict
fan_out_from_dict = FanOut.from_dict(fan_out_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


