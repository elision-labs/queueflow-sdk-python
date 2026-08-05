# CreateBatchJobsResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**count** | **int** |  | 
**job_ids** | **List[str]** |  | 

## Example

```python
from queueflow.models.create_batch_jobs_response import CreateBatchJobsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of CreateBatchJobsResponse from a JSON string
create_batch_jobs_response_instance = CreateBatchJobsResponse.from_json(json)
# print the JSON string representation of the object
print(CreateBatchJobsResponse.to_json())

# convert the object into a dict
create_batch_jobs_response_dict = create_batch_jobs_response_instance.to_dict()
# create an instance of CreateBatchJobsResponse from a dict
create_batch_jobs_response_from_dict = CreateBatchJobsResponse.from_dict(create_batch_jobs_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


