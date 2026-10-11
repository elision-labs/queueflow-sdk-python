# QueueStats

Live, per-queue backlog figures read from the store: what an operator watches to decide whether to add workers. Only non-terminal jobs are counted, so the query stays cheap on a large history table. Durable totals live in [`StatsSnapshot`] via `JobStore::count_stats`.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**oldest_pending_age_secs** | **int** | Seconds the oldest claimable job has been waiting, &#x60;None&#x60; when nothing is claimable. The queue&#39;s primary health signal: it grows when workers cannot keep up and stays near zero when they can. | [optional] 
**pending** | **int** | Claimable now: &#x60;pending&#x60; or &#x60;retrying&#x60; with &#x60;scheduled_at&#x60; in the past. | 
**queue** | **str** |  | 
**running** | **int** | Currently leased by a worker. | 
**scheduled** | **int** | Waiting for a future &#x60;scheduled_at&#x60; (a &#x60;run_at&#x60; job or a backoff retry). | 

## Example

```python
from queueflow.models.queue_stats import QueueStats

# TODO update the JSON string below
json = "{}"
# create an instance of QueueStats from a JSON string
queue_stats_instance = QueueStats.from_json(json)
# print the JSON string representation of the object
print(QueueStats.to_json())

# convert the object into a dict
queue_stats_dict = queue_stats_instance.to_dict()
# create an instance of QueueStats from a dict
queue_stats_from_dict = QueueStats.from_dict(queue_stats_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


