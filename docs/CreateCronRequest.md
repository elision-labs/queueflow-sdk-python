# CreateCronRequest

Request body for creating a cron schedule.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**config** | [**JobConfig**](JobConfig.md) |  | [optional] 
**cron_expr** | **str** | 5-field crontab (UTC); 6/7 fields with leading seconds also accepted. | 
**name** | **str** | Unique per tenant. | 
**payload** | **Dict[str, object]** |  | [optional] 
**queue** | **str** |  | [optional] 
**task_name** | **str** |  | 

## Example

```python
from queueflow.models.create_cron_request import CreateCronRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateCronRequest from a JSON string
create_cron_request_instance = CreateCronRequest.from_json(json)
# print the JSON string representation of the object
print(CreateCronRequest.to_json())

# convert the object into a dict
create_cron_request_dict = create_cron_request_instance.to_dict()
# create an instance of CreateCronRequest from a dict
create_cron_request_from_dict = CreateCronRequest.from_dict(create_cron_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


