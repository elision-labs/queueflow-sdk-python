# queueflow.DlqApi

All URIs are relative to *http://localhost:8000*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_dead_letter**](DlqApi.md#get_dead_letter) | **GET** /api/v1/dlq/{id} | 
[**list_dead_letters**](DlqApi.md#list_dead_letters) | **GET** /api/v1/dlq | 
[**replay_dead_letter**](DlqApi.md#replay_dead_letter) | **POST** /api/v1/dlq/{id}/replay | 
[**replay_dead_letters**](DlqApi.md#replay_dead_letters) | **POST** /api/v1/dlq/replay | 


# **get_dead_letter**
> DeadLetter get_dead_letter(id)



### Example

* Bearer (API Key) Authentication (bearerAuth):

```python
import queueflow
from queueflow.models.dead_letter import DeadLetter
from queueflow.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:8000
# See configuration.py for a list of all supported configuration parameters.
configuration = queueflow.Configuration(
    host = "http://localhost:8000"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (API Key): bearerAuth
configuration = queueflow.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with queueflow.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = queueflow.DlqApi(api_client)
    id = 56 # int | Dead letter id

    try:
        api_response = api_instance.get_dead_letter(id)
        print("The response of DlqApi->get_dead_letter:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DlqApi->get_dead_letter: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**| Dead letter id | 

### Return type

[**DeadLetter**](DeadLetter.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Dead letter |  -  |
**401** | Unauthorized |  -  |
**403** | Forbidden |  -  |
**404** | Not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_dead_letters**
> ListDeadLettersResponse list_dead_letters(status=status, queue=queue, task_name=task_name, replayed=replayed, limit=limit, offset=offset, order_by=order_by, include_total=include_total, cursor=cursor, created_after=created_after, created_before=created_before)



### Example

* Bearer (API Key) Authentication (bearerAuth):

```python
import queueflow
from queueflow.models.list_dead_letters_response import ListDeadLettersResponse
from queueflow.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:8000
# See configuration.py for a list of all supported configuration parameters.
configuration = queueflow.Configuration(
    host = "http://localhost:8000"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (API Key): bearerAuth
configuration = queueflow.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with queueflow.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = queueflow.DlqApi(api_client)
    status = 'status_example' # str | Filter by status (e.g. `pending`, `completed`). (optional)
    queue = 'queue_example' # str | Filter by queue name (jobs only). (optional)
    task_name = 'task_name_example' # str | Filter by task name (jobs and dead letters). (optional)
    replayed = True # bool | Dead letters only: `false` lists entries not yet replayed, `true` the replayed ones; both when omitted. (optional)
    limit = 56 # int | Page size, 1..=100 (default 50). (optional)
    offset = 56 # int | Number of records to skip (default 0). (optional)
    order_by = 'order_by_example' # str | `created_at ASC` or `created_at DESC` (default DESC). (optional)
    include_total = True # bool | Include the exact `total` count in the response (default false; the count is an extra full scan over the filtered set). (optional)
    cursor = 'cursor_example' # str | Opaque keyset cursor from a previous page's `next_cursor`. When set, `offset` is ignored and listing continues where that page ended. (optional)
    created_after = '2013-10-20T19:20:30+01:00' # datetime | Only rows created at or after this instant (RFC 3339, inclusive). With `created_before` this forms the half-open range `[after, before)` — the natural shape for walking history period by period. (optional)
    created_before = '2013-10-20T19:20:30+01:00' # datetime | Only rows created strictly before this instant (RFC 3339, exclusive). (optional)

    try:
        api_response = api_instance.list_dead_letters(status=status, queue=queue, task_name=task_name, replayed=replayed, limit=limit, offset=offset, order_by=order_by, include_total=include_total, cursor=cursor, created_after=created_after, created_before=created_before)
        print("The response of DlqApi->list_dead_letters:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DlqApi->list_dead_letters: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **status** | **str**| Filter by status (e.g. &#x60;pending&#x60;, &#x60;completed&#x60;). | [optional] 
 **queue** | **str**| Filter by queue name (jobs only). | [optional] 
 **task_name** | **str**| Filter by task name (jobs and dead letters). | [optional] 
 **replayed** | **bool**| Dead letters only: &#x60;false&#x60; lists entries not yet replayed, &#x60;true&#x60; the replayed ones; both when omitted. | [optional] 
 **limit** | **int**| Page size, 1..&#x3D;100 (default 50). | [optional] 
 **offset** | **int**| Number of records to skip (default 0). | [optional] 
 **order_by** | **str**| &#x60;created_at ASC&#x60; or &#x60;created_at DESC&#x60; (default DESC). | [optional] 
 **include_total** | **bool**| Include the exact &#x60;total&#x60; count in the response (default false; the count is an extra full scan over the filtered set). | [optional] 
 **cursor** | **str**| Opaque keyset cursor from a previous page&#39;s &#x60;next_cursor&#x60;. When set, &#x60;offset&#x60; is ignored and listing continues where that page ended. | [optional] 
 **created_after** | **datetime**| Only rows created at or after this instant (RFC 3339, inclusive). With &#x60;created_before&#x60; this forms the half-open range &#x60;[after, before)&#x60; — the natural shape for walking history period by period. | [optional] 
 **created_before** | **datetime**| Only rows created strictly before this instant (RFC 3339, exclusive). | [optional] 

### Return type

[**ListDeadLettersResponse**](ListDeadLettersResponse.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Page of dead letters, newest first. &#x60;queue&#x60;, &#x60;task_name&#x60;, &#x60;replayed&#x60; and the time window apply; &#x60;status&#x60; does not. |  -  |
**401** | Unauthorized |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **replay_dead_letter**
> ReplayDeadLetterResponse replay_dead_letter(id)



### Example

* Bearer (API Key) Authentication (bearerAuth):

```python
import queueflow
from queueflow.models.replay_dead_letter_response import ReplayDeadLetterResponse
from queueflow.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:8000
# See configuration.py for a list of all supported configuration parameters.
configuration = queueflow.Configuration(
    host = "http://localhost:8000"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (API Key): bearerAuth
configuration = queueflow.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with queueflow.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = queueflow.DlqApi(api_client)
    id = 56 # int | Dead letter id

    try:
        api_response = api_instance.replay_dead_letter(id)
        print("The response of DlqApi->replay_dead_letter:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DlqApi->replay_dead_letter: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**| Dead letter id | 

### Return type

[**ReplayDeadLetterResponse**](ReplayDeadLetterResponse.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | A fresh job was created from the dead-lettered one (same task/payload/queue/config; workflow linkage is not resurrected) |  -  |
**401** | Unauthorized |  -  |
**403** | Forbidden |  -  |
**404** | Not found (the entry, or its original job after retention) |  -  |
**409** | Already replayed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **replay_dead_letters**
> ReplayDeadLettersResponse replay_dead_letters(replay_dead_letters_request)



### Example

* Bearer (API Key) Authentication (bearerAuth):

```python
import queueflow
from queueflow.models.replay_dead_letters_request import ReplayDeadLettersRequest
from queueflow.models.replay_dead_letters_response import ReplayDeadLettersResponse
from queueflow.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:8000
# See configuration.py for a list of all supported configuration parameters.
configuration = queueflow.Configuration(
    host = "http://localhost:8000"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (API Key): bearerAuth
configuration = queueflow.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with queueflow.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = queueflow.DlqApi(api_client)
    replay_dead_letters_request = queueflow.ReplayDeadLettersRequest() # ReplayDeadLettersRequest | 

    try:
        api_response = api_instance.replay_dead_letters(replay_dead_letters_request)
        print("The response of DlqApi->replay_dead_letters:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DlqApi->replay_dead_letters: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **replay_dead_letters_request** | [**ReplayDeadLettersRequest**](ReplayDeadLettersRequest.md)|  | 

### Return type

[**ReplayDeadLettersResponse**](ReplayDeadLettersResponse.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Every unreplayed dead letter matching the filter (oldest first, up to &#x60;limit&#x60;) was replayed as a fresh job, or is listed with the reason it could not be. |  -  |
**401** | Unauthorized |  -  |
**403** | Forbidden |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

