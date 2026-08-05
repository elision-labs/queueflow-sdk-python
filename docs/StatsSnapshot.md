# StatsSnapshot

Plain snapshot of [`EngineStats`].

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**jobs_completed** | **int** |  | 
**jobs_created** | **int** |  | 
**jobs_dead_lettered** | **int** |  | 
**jobs_failed** | **int** |  | 
**jobs_retried** | **int** |  | 
**workflows_completed** | **int** |  | 
**workflows_created** | **int** |  | 
**workflows_failed** | **int** |  | 

## Example

```python
from queueflow.models.stats_snapshot import StatsSnapshot

# TODO update the JSON string below
json = "{}"
# create an instance of StatsSnapshot from a JSON string
stats_snapshot_instance = StatsSnapshot.from_json(json)
# print the JSON string representation of the object
print(StatsSnapshot.to_json())

# convert the object into a dict
stats_snapshot_dict = stats_snapshot_instance.to_dict()
# create an instance of StatsSnapshot from a dict
stats_snapshot_from_dict = StatsSnapshot.from_dict(stats_snapshot_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


