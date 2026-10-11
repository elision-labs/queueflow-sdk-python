# WhoAmIResponse

The caller's identity, as the server resolved it from the bearer token.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**access** | **str** | &#x60;read_write&#x60;, or &#x60;read_only&#x60; for a &#x60;:ro&#x60; key or a &#x60;scope: read&#x60; JWT. | 
**tenant** | **str** | The tenant every request with this credential is scoped to. | 

## Example

```python
from queueflow.models.who_am_i_response import WhoAmIResponse

# TODO update the JSON string below
json = "{}"
# create an instance of WhoAmIResponse from a JSON string
who_am_i_response_instance = WhoAmIResponse.from_json(json)
# print the JSON string representation of the object
print(WhoAmIResponse.to_json())

# convert the object into a dict
who_am_i_response_dict = who_am_i_response_instance.to_dict()
# create an instance of WhoAmIResponse from a dict
who_am_i_response_from_dict = WhoAmIResponse.from_dict(who_am_i_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


