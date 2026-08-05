# FailJobRequest

Body for `POST /api/v1/jobs/{id}/fail`.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**error** | **str** | Human-readable failure reason. | 
**lease_token** | **str** | The lease token returned by the lease call. | 
**retryable** | **bool** | Whether the engine may retry (subject to the job&#39;s max_retries). Defaults to true; send false for permanent failures (e.g. bad input). | [optional] 

## Example

```python
from queueflow.models.fail_job_request import FailJobRequest

# TODO update the JSON string below
json = "{}"
# create an instance of FailJobRequest from a JSON string
fail_job_request_instance = FailJobRequest.from_json(json)
# print the JSON string representation of the object
print(FailJobRequest.to_json())

# convert the object into a dict
fail_job_request_dict = fail_job_request_instance.to_dict()
# create an instance of FailJobRequest from a dict
fail_job_request_from_dict = FailJobRequest.from_dict(fail_job_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


