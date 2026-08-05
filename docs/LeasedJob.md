# LeasedJob

A job leased to a (possibly remote) worker, together with the lease token needed to heartbeat, complete, or fail it.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**job** | [**Job**](Job.md) |  | 
**lease_token** | **str** | Opaque, unguessable proof of lease ownership, regenerated on every claim. Pass it back on heartbeat/complete/fail; a stale token (the lease expired and the job was reclaimed) is rejected. | 

## Example

```python
from queueflow.models.leased_job import LeasedJob

# TODO update the JSON string below
json = "{}"
# create an instance of LeasedJob from a JSON string
leased_job_instance = LeasedJob.from_json(json)
# print the JSON string representation of the object
print(LeasedJob.to_json())

# convert the object into a dict
leased_job_dict = leased_job_instance.to_dict()
# create an instance of LeasedJob from a dict
leased_job_from_dict = LeasedJob.from_dict(leased_job_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


