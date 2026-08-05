# CronSchedule

A recurring enqueue schedule. Expressions are standard 5-field crontab (`minute hour day-of-month month day-of-week`), evaluated in **UTC**; a 6/7-field form with leading seconds is also accepted.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**config** | [**JobConfig**](JobConfig.md) |  | [optional] 
**created_at** | **datetime** |  | 
**cron_expr** | **str** |  | 
**enabled** | **bool** |  | 
**id** | **str** |  | 
**last_enqueued_at** | **datetime** |  | [optional] 
**name** | **str** | Unique per tenant. | 
**next_run_at** | **datetime** | The next instant this schedule fires. Missed occurrences (server down) collapse into at most one catch-up firing. | 
**payload** | **Dict[str, object]** |  | [optional] 
**queue_name** | **str** | Queue for the enqueued jobs (the engine default when absent). | [optional] 
**task_name** | **str** |  | 
**tenant_id** | **str** |  | [optional] 

## Example

```python
from queueflow.models.cron_schedule import CronSchedule

# TODO update the JSON string below
json = "{}"
# create an instance of CronSchedule from a JSON string
cron_schedule_instance = CronSchedule.from_json(json)
# print the JSON string representation of the object
print(CronSchedule.to_json())

# convert the object into a dict
cron_schedule_dict = cron_schedule_instance.to_dict()
# create an instance of CronSchedule from a dict
cron_schedule_from_dict = CronSchedule.from_dict(cron_schedule_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


