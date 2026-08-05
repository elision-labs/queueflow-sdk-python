# CreateBatchJobsRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**jobs** | [**List[CreateJobRequest]**](CreateJobRequest.md) |  | 

## Example

```python
from queueflow.models.create_batch_jobs_request import CreateBatchJobsRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateBatchJobsRequest from a JSON string
create_batch_jobs_request_instance = CreateBatchJobsRequest.from_json(json)
# print the JSON string representation of the object
print(CreateBatchJobsRequest.to_json())

# convert the object into a dict
create_batch_jobs_request_dict = create_batch_jobs_request_instance.to_dict()
# create an instance of CreateBatchJobsRequest from a dict
create_batch_jobs_request_from_dict = CreateBatchJobsRequest.from_dict(create_batch_jobs_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


