# queueflow.WorkerApi

All URIs are relative to *http://localhost:8000*

Method | HTTP request | Description
------------- | ------------- | -------------
[**complete_job**](WorkerApi.md#complete_job) | **POST** /api/v1/jobs/{id}/complete | 
[**fail_job**](WorkerApi.md#fail_job) | **POST** /api/v1/jobs/{id}/fail | 
[**heartbeat_job**](WorkerApi.md#heartbeat_job) | **POST** /api/v1/jobs/{id}/heartbeat | 
[**lease_jobs**](WorkerApi.md#lease_jobs) | **POST** /api/v1/queues/{queue}/lease | 


# **complete_job**
> complete_job(id, complete_job_request)



### Example

* Bearer (API Key) Authentication (bearerAuth):

```python
import queueflow
from queueflow.models.complete_job_request import CompleteJobRequest
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
    api_instance = queueflow.WorkerApi(api_client)
    id = 'id_example' # str | Job id
    complete_job_request = queueflow.CompleteJobRequest() # CompleteJobRequest | 

    try:
        api_instance.complete_job(id, complete_job_request)
    except Exception as e:
        print("Exception when calling WorkerApi->complete_job: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Job id | 
 **complete_job_request** | [**CompleteJobRequest**](CompleteJobRequest.md)|  | 

### Return type

void (empty response body)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Completed (idempotent: replaying against an already-finished job also succeeds) |  -  |
**401** | Unauthorized |  -  |
**403** | Authenticated, but not with the worker credential |  -  |
**404** | Not found |  -  |
**409** | Lease no longer held (expired and reclaimed) |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **fail_job**
> fail_job(id, fail_job_request)



### Example

* Bearer (API Key) Authentication (bearerAuth):

```python
import queueflow
from queueflow.models.fail_job_request import FailJobRequest
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
    api_instance = queueflow.WorkerApi(api_client)
    id = 'id_example' # str | Job id
    fail_job_request = queueflow.FailJobRequest() # FailJobRequest | 

    try:
        api_instance.fail_job(id, fail_job_request)
    except Exception as e:
        print("Exception when calling WorkerApi->fail_job: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Job id | 
 **fail_job_request** | [**FailJobRequest**](FailJobRequest.md)|  | 

### Return type

void (empty response body)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Failure recorded; the job is retried or dead-lettered per its config |  -  |
**401** | Unauthorized |  -  |
**403** | Authenticated, but not with the worker credential |  -  |
**404** | Not found |  -  |
**409** | Lease no longer held (expired and reclaimed) |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **heartbeat_job**
> HeartbeatResponse heartbeat_job(id, heartbeat_request)



### Example

* Bearer (API Key) Authentication (bearerAuth):

```python
import queueflow
from queueflow.models.heartbeat_request import HeartbeatRequest
from queueflow.models.heartbeat_response import HeartbeatResponse
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
    api_instance = queueflow.WorkerApi(api_client)
    id = 'id_example' # str | Job id
    heartbeat_request = queueflow.HeartbeatRequest() # HeartbeatRequest | 

    try:
        api_response = api_instance.heartbeat_job(id, heartbeat_request)
        print("The response of WorkerApi->heartbeat_job:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkerApi->heartbeat_job: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Job id | 
 **heartbeat_request** | [**HeartbeatRequest**](HeartbeatRequest.md)|  | 

### Return type

[**HeartbeatResponse**](HeartbeatResponse.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Current job status. &#x60;running&#x60; &#x3D; lease extended; anything else (e.g. &#x60;cancelled&#x60;) &#x3D; not extended, stop working on the job. |  -  |
**401** | Unauthorized |  -  |
**403** | Authenticated, but not with the worker credential |  -  |
**404** | Not found |  -  |
**409** | Lease no longer held (expired and reclaimed) |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **lease_jobs**
> LeaseJobsResponse lease_jobs(queue, lease_jobs_request)



### Example

* Bearer (API Key) Authentication (bearerAuth):

```python
import queueflow
from queueflow.models.lease_jobs_request import LeaseJobsRequest
from queueflow.models.lease_jobs_response import LeaseJobsResponse
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
    api_instance = queueflow.WorkerApi(api_client)
    queue = 'queue_example' # str | Queue to lease from
    lease_jobs_request = queueflow.LeaseJobsRequest() # LeaseJobsRequest | 

    try:
        api_response = api_instance.lease_jobs(queue, lease_jobs_request)
        print("The response of WorkerApi->lease_jobs:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkerApi->lease_jobs: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **queue** | **str**| Queue to lease from | 
 **lease_jobs_request** | [**LeaseJobsRequest**](LeaseJobsRequest.md)|  | 

### Return type

[**LeaseJobsResponse**](LeaseJobsResponse.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Zero or more leased jobs (empty if none became available within wait_secs) |  -  |
**401** | Unauthorized |  -  |
**403** | Authenticated, but not with the worker credential |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

