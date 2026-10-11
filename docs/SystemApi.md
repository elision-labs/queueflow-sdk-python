# queueflow.SystemApi

All URIs are relative to *http://localhost:8000*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_stats**](SystemApi.md#get_stats) | **GET** /api/v1/stats | 
[**list_queues**](SystemApi.md#list_queues) | **GET** /api/v1/queues | 
[**list_tasks**](SystemApi.md#list_tasks) | **GET** /api/v1/tasks | 
[**pause_queue**](SystemApi.md#pause_queue) | **POST** /api/v1/queues/{queue}/pause | 
[**resume_queue**](SystemApi.md#resume_queue) | **POST** /api/v1/queues/{queue}/resume | 
[**who_am_i**](SystemApi.md#who_am_i) | **GET** /api/v1/whoami | 


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
**200** | Durable counts for the caller&#39;s tenant, read from the store: jobs in the store (&#x60;jobs_created&#x60;), jobs completed / failed, the sum of retries, dead letters, and the same for workflows. Fleet-wide and restart-safe, but retention deletes history, so counts can go down. Process-local engine counters are exposed on the Prometheus metrics port instead. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_queues**
> QueuesResponse list_queues()



### Example

* Bearer (API Key) Authentication (bearerAuth):

```python
import queueflow
from queueflow.models.queues_response import QueuesResponse
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
        api_response = api_instance.list_queues()
        print("The response of SystemApi->list_queues:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SystemApi->list_queues: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**QueuesResponse**](QueuesResponse.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Backlog per queue for the caller&#39;s tenant: claimable (&#x60;pending&#x60;), waiting for a future run time (&#x60;scheduled&#x60;), and &#x60;running&#x60; counts, how long the oldest claimable job has waited, and whether the queue is &#x60;paused&#x60;. Lists every queue the tenant has enqueued to (since 0.5.0) and any with non-terminal jobs. |  -  |

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

# **pause_queue**
> QueueControlResponse pause_queue(queue)



### Example

* Bearer (API Key) Authentication (bearerAuth):

```python
import queueflow
from queueflow.models.queue_control_response import QueueControlResponse
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
    queue = 'queue_example' # str | Queue name

    try:
        api_response = api_instance.pause_queue(queue)
        print("The response of SystemApi->pause_queue:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SystemApi->pause_queue: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **queue** | **str**| Queue name | 

### Return type

[**QueueControlResponse**](QueueControlResponse.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Claims of the caller&#39;s jobs on this queue are paused: pending jobs wait, running jobs finish. The queue is drained once &#x60;running&#x60; reaches zero. Idempotent. |  -  |
**400** | Invalid queue name |  -  |
**401** | Unauthorized |  -  |
**403** | Forbidden |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **resume_queue**
> QueueControlResponse resume_queue(queue)



### Example

* Bearer (API Key) Authentication (bearerAuth):

```python
import queueflow
from queueflow.models.queue_control_response import QueueControlResponse
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
    queue = 'queue_example' # str | Queue name

    try:
        api_response = api_instance.resume_queue(queue)
        print("The response of SystemApi->resume_queue:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SystemApi->resume_queue: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **queue** | **str**| Queue name | 

### Return type

[**QueueControlResponse**](QueueControlResponse.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Claims resume immediately; parked workers are woken. Idempotent. |  -  |
**400** | Invalid queue name |  -  |
**401** | Unauthorized |  -  |
**403** | Forbidden |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **who_am_i**
> WhoAmIResponse who_am_i()



### Example

* Bearer (API Key) Authentication (bearerAuth):

```python
import queueflow
from queueflow.models.who_am_i_response import WhoAmIResponse
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
        api_response = api_instance.who_am_i()
        print("The response of SystemApi->who_am_i:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SystemApi->who_am_i: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**WhoAmIResponse**](WhoAmIResponse.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The tenant and access level of the bearer token |  -  |
**401** | Unauthorized |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

