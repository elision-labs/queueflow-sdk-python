# queueflow.CronApi

All URIs are relative to *http://localhost:8000*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_cron**](CronApi.md#create_cron) | **POST** /api/v1/cron | 
[**delete_cron**](CronApi.md#delete_cron) | **DELETE** /api/v1/cron/{id} | 
[**get_cron**](CronApi.md#get_cron) | **GET** /api/v1/cron/{id} | 
[**list_crons**](CronApi.md#list_crons) | **GET** /api/v1/cron | 
[**pause_cron**](CronApi.md#pause_cron) | **POST** /api/v1/cron/{id}/pause | 
[**resume_cron**](CronApi.md#resume_cron) | **POST** /api/v1/cron/{id}/resume | 


# **create_cron**
> CreateCronResponse create_cron(create_cron_request)



### Example

* Bearer (API Key) Authentication (bearerAuth):

```python
import queueflow
from queueflow.models.create_cron_request import CreateCronRequest
from queueflow.models.create_cron_response import CreateCronResponse
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
    api_instance = queueflow.CronApi(api_client)
    create_cron_request = queueflow.CreateCronRequest() # CreateCronRequest | 

    try:
        api_response = api_instance.create_cron(create_cron_request)
        print("The response of CronApi->create_cron:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CronApi->create_cron: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **create_cron_request** | [**CreateCronRequest**](CreateCronRequest.md)|  | 

### Return type

[**CreateCronResponse**](CreateCronResponse.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Schedule created; first firing is the next occurrence (UTC) |  -  |
**400** | Invalid request (e.g. a bad cron expression) |  -  |
**401** | Unauthorized |  -  |
**409** | A schedule with this name already exists |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_cron**
> delete_cron(id)



### Example

* Bearer (API Key) Authentication (bearerAuth):

```python
import queueflow
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
    api_instance = queueflow.CronApi(api_client)
    id = 'id_example' # str | Cron schedule id

    try:
        api_instance.delete_cron(id)
    except Exception as e:
        print("Exception when calling CronApi->delete_cron: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Cron schedule id | 

### Return type

void (empty response body)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Deleted; already-enqueued jobs are unaffected |  -  |
**401** | Unauthorized |  -  |
**403** | Forbidden |  -  |
**404** | Not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_cron**
> CronSchedule get_cron(id)



### Example

* Bearer (API Key) Authentication (bearerAuth):

```python
import queueflow
from queueflow.models.cron_schedule import CronSchedule
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
    api_instance = queueflow.CronApi(api_client)
    id = 'id_example' # str | Cron schedule id

    try:
        api_response = api_instance.get_cron(id)
        print("The response of CronApi->get_cron:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CronApi->get_cron: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Cron schedule id | 

### Return type

[**CronSchedule**](CronSchedule.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Cron schedule |  -  |
**401** | Unauthorized |  -  |
**403** | Forbidden |  -  |
**404** | Not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_crons**
> ListCronsResponse list_crons(status=status, queue=queue, limit=limit, offset=offset, order_by=order_by, include_total=include_total, cursor=cursor)



### Example

* Bearer (API Key) Authentication (bearerAuth):

```python
import queueflow
from queueflow.models.list_crons_response import ListCronsResponse
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
    api_instance = queueflow.CronApi(api_client)
    status = 'status_example' # str | Filter by status (e.g. `pending`, `completed`). (optional)
    queue = 'queue_example' # str | Filter by queue name (jobs only). (optional)
    limit = 56 # int | Page size, 1..=100 (default 50). (optional)
    offset = 56 # int | Number of records to skip (default 0). (optional)
    order_by = 'order_by_example' # str | `created_at ASC` or `created_at DESC` (default DESC). (optional)
    include_total = True # bool | Include the exact `total` count in the response (default false; the count is an extra full scan over the filtered set). (optional)
    cursor = 'cursor_example' # str | Opaque keyset cursor from a previous page's `next_cursor`. When set, `offset` is ignored and listing continues where that page ended. (optional)

    try:
        api_response = api_instance.list_crons(status=status, queue=queue, limit=limit, offset=offset, order_by=order_by, include_total=include_total, cursor=cursor)
        print("The response of CronApi->list_crons:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CronApi->list_crons: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **status** | **str**| Filter by status (e.g. &#x60;pending&#x60;, &#x60;completed&#x60;). | [optional] 
 **queue** | **str**| Filter by queue name (jobs only). | [optional] 
 **limit** | **int**| Page size, 1..&#x3D;100 (default 50). | [optional] 
 **offset** | **int**| Number of records to skip (default 0). | [optional] 
 **order_by** | **str**| &#x60;created_at ASC&#x60; or &#x60;created_at DESC&#x60; (default DESC). | [optional] 
 **include_total** | **bool**| Include the exact &#x60;total&#x60; count in the response (default false; the count is an extra full scan over the filtered set). | [optional] 
 **cursor** | **str**| Opaque keyset cursor from a previous page&#39;s &#x60;next_cursor&#x60;. When set, &#x60;offset&#x60; is ignored and listing continues where that page ended. | [optional] 

### Return type

[**ListCronsResponse**](ListCronsResponse.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Page of cron schedules (&#x60;status&#x60;/&#x60;queue&#x60; filters do not apply) |  -  |
**401** | Unauthorized |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **pause_cron**
> pause_cron(id)



### Example

* Bearer (API Key) Authentication (bearerAuth):

```python
import queueflow
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
    api_instance = queueflow.CronApi(api_client)
    id = 'id_example' # str | Cron schedule id

    try:
        api_instance.pause_cron(id)
    except Exception as e:
        print("Exception when calling CronApi->pause_cron: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Cron schedule id | 

### Return type

void (empty response body)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Paused: no further firings until resumed |  -  |
**401** | Unauthorized |  -  |
**403** | Forbidden |  -  |
**404** | Not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **resume_cron**
> resume_cron(id)



### Example

* Bearer (API Key) Authentication (bearerAuth):

```python
import queueflow
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
    api_instance = queueflow.CronApi(api_client)
    id = 'id_example' # str | Cron schedule id

    try:
        api_instance.resume_cron(id)
    except Exception as e:
        print("Exception when calling CronApi->resume_cron: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Cron schedule id | 

### Return type

void (empty response body)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Resumed: fires at its next future occurrence (missed runs are not caught up) |  -  |
**401** | Unauthorized |  -  |
**403** | Forbidden |  -  |
**404** | Not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

