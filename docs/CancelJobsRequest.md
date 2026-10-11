# CancelJobsRequest

Which jobs a bulk cancel applies to. Every field is optional; an empty body cancels the caller's oldest non-terminal jobs up to `limit`.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**created_after** | **datetime** | Only jobs created at or after this instant (RFC 3339, inclusive). | [optional] 
**created_before** | **datetime** | Only jobs created strictly before this instant (RFC 3339, exclusive). | [optional] 
**limit** | **int** | Cancel at most this many (oldest first). Default 100; the maximum is the server&#39;s batch limit (&#x60;--max-batch&#x60;, 1000 by default). | [optional] 
**queue** | **str** | Only jobs on this queue. | [optional] 
**status** | **str** | Only jobs in this state: &#x60;pending&#x60;, &#x60;retrying&#x60; or &#x60;running&#x60; (all three when omitted). Terminal states are rejected: history is never rewritten. | [optional] 
**task_name** | **str** | Only jobs for this task. | [optional] 

## Example

```python
from queueflow.models.cancel_jobs_request import CancelJobsRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CancelJobsRequest from a JSON string
cancel_jobs_request_instance = CancelJobsRequest.from_json(json)
# print the JSON string representation of the object
print(CancelJobsRequest.to_json())

# convert the object into a dict
cancel_jobs_request_dict = cancel_jobs_request_instance.to_dict()
# create an instance of CancelJobsRequest from a dict
cancel_jobs_request_from_dict = CancelJobsRequest.from_dict(cancel_jobs_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


