# FanOutProgress

Counts over a fan-out step's child jobs.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**completed** | **int** |  | 
**failed** | **int** | Failed or cancelled children. | 
**total** | **int** |  | 

## Example

```python
from queueflow.models.fan_out_progress import FanOutProgress

# TODO update the JSON string below
json = "{}"
# create an instance of FanOutProgress from a JSON string
fan_out_progress_instance = FanOutProgress.from_json(json)
# print the JSON string representation of the object
print(FanOutProgress.to_json())

# convert the object into a dict
fan_out_progress_dict = fan_out_progress_instance.to_dict()
# create an instance of FanOutProgress from a dict
fan_out_progress_from_dict = FanOutProgress.from_dict(fan_out_progress_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


