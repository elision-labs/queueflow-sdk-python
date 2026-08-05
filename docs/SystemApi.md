# queueflow.SystemApi

All URIs are relative to *http://localhost:8000*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_stats**](SystemApi.md#get_stats) | **GET** /api/v1/stats | 
[**list_tasks**](SystemApi.md#list_tasks) | **GET** /api/v1/tasks | 


# **get_stats**
> StatsSnapshot get_stats()



### Example

* Bearer (API Key) Authentication (bearerAuth):

```python
import queueflow
from queueflow.models.stats_snapshot import StatsSnapshot
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
    api_instance = queueflow.SystemApi(api_client)

    try:
        api_response = api_instance.get_stats()
        print("The response of SystemApi->get_stats:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SystemApi->get_stats: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**StatsSnapshot**](StatsSnapshot.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Engine counters. Process-local and reset on restart: in a split api/worker deployment this reflects only the process serving the request; query the database for fleet-wide history. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_tasks**
> TasksResponse list_tasks()



### Example

* Bearer (API Key) Authentication (bearerAuth):

```python
import queueflow
from queueflow.models.tasks_response import TasksResponse
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
    api_instance = queueflow.SystemApi(api_client)

    try:
        api_response = api_instance.list_tasks()
        print("The response of SystemApi->list_tasks:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SystemApi->list_tasks: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**TasksResponse**](TasksResponse.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Registered task handlers |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

