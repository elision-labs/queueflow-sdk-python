# queueflow.JobsApi

All URIs are relative to *http://localhost:8000*

Method | HTTP request | Description
------------- | ------------- | -------------
[**cancel_job**](JobsApi.md#cancel_job) | **POST** /api/v1/jobs/{id}/cancel | 
[**create_batch_jobs**](JobsApi.md#create_batch_jobs) | **POST** /api/v1/jobs/batch | 
[**create_job**](JobsApi.md#create_job) | **POST** /api/v1/jobs | 
[**get_job**](JobsApi.md#get_job) | **GET** /api/v1/jobs/{id} | 
[**list_jobs**](JobsApi.md#list_jobs) | **GET** /api/v1/jobs | 
[**stream_job_events**](JobsApi.md#stream_job_events) | **GET** /api/v1/jobs/{id}/events | Stream a job&#39;s status transitions as Server-Sent Events until it reaches a terminal state. Lets clients await completion without polling the REST endpoint themselves.


# **cancel_job**
> cancel_job(id)



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
    api_instance = queueflow.JobsApi(api_client)
    id = 'id_example' # str | Job id

    try:
        api_instance.cancel_job(id)
    except Exception as e:
        print("Exception when calling JobsApi->cancel_job: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Job id | 

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
**204** | Cancelled |  -  |
**401** | Unauthorized |  -  |
**403** | Forbidden |  -  |
**404** | Not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_batch_jobs**
> CreateBatchJobsResponse create_batch_jobs(create_batch_jobs_request)



### Example

* Bearer (API Key) Authentication (bearerAuth):

```python
import queueflow
from queueflow.models.create_batch_jobs_request import CreateBatchJobsRequest
from queueflow.models.create_batch_jobs_response import CreateBatchJobsResponse
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
    api_instance = queueflow.JobsApi(api_client)
    create_batch_jobs_request = queueflow.CreateBatchJobsRequest() # CreateBatchJobsRequest | 

    try:
        api_response = api_instance.create_batch_jobs(create_batch_jobs_request)
        print("The response of JobsApi->create_batch_jobs:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling JobsApi->create_batch_jobs: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **create_batch_jobs_request** | [**CreateBatchJobsRequest**](CreateBatchJobsRequest.md)|  | 

### Return type

[**CreateBatchJobsResponse**](CreateBatchJobsResponse.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Jobs created |  -  |
**400** | Invalid request |  -  |
**401** | Unauthorized |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_job**
> CreateJobResponse create_job(create_job_request, idempotency_key=idempotency_key)



### Example

* Bearer (API Key) Authentication (bearerAuth):

```python
import queueflow
from queueflow.models.create_job_request import CreateJobRequest
from queueflow.models.create_job_response import CreateJobResponse
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
    api_instance = queueflow.JobsApi(api_client)
    create_job_request = queueflow.CreateJobRequest() # CreateJobRequest | 
    idempotency_key = 'idempotency_key_example' # str | Optional client-supplied key making this create idempotent per tenant: retrying with the same key returns the original job instead of creating a duplicate. (optional)

    try:
        api_response = api_instance.create_job(create_job_request, idempotency_key=idempotency_key)
        print("The response of JobsApi->create_job:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling JobsApi->create_job: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **create_job_request** | [**CreateJobRequest**](CreateJobRequest.md)|  | 
 **idempotency_key** | **str**| Optional client-supplied key making this create idempotent per tenant: retrying with the same key returns the original job instead of creating a duplicate. | [optional] 

### Return type

[**CreateJobResponse**](CreateJobResponse.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Job created (or replayed idempotently) |  -  |
**400** | Invalid request |  -  |
**401** | Unauthorized |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_job**
> Job get_job(id)



### Example

* Bearer (API Key) Authentication (bearerAuth):

```python
import queueflow
from queueflow.models.job import Job
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
    api_instance = queueflow.JobsApi(api_client)
    id = 'id_example' # str | Job id

    try:
        api_response = api_instance.get_job(id)
        print("The response of JobsApi->get_job:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling JobsApi->get_job: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Job id | 

### Return type

[**Job**](Job.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Job |  -  |
**403** | Forbidden |  -  |
**404** | Not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_jobs**
> ListJobsResponse list_jobs(status=status, queue=queue, limit=limit, offset=offset, order_by=order_by, include_total=include_total)



### Example

* Bearer (API Key) Authentication (bearerAuth):

```python
import queueflow
from queueflow.models.list_jobs_response import ListJobsResponse
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
    api_instance = queueflow.JobsApi(api_client)
    status = 'status_example' # str | Filter by status (e.g. `pending`, `completed`). (optional)
    queue = 'queue_example' # str | Filter by queue name (jobs only). (optional)
    limit = 56 # int | Page size, 1..=100 (default 50). (optional)
    offset = 56 # int | Number of records to skip (default 0). (optional)
    order_by = 'order_by_example' # str | `created_at ASC` or `created_at DESC` (default DESC). (optional)
    include_total = True # bool | Include the exact `total` count in the response (default false; the count is an extra full scan over the filtered set). (optional)

    try:
        api_response = api_instance.list_jobs(status=status, queue=queue, limit=limit, offset=offset, order_by=order_by, include_total=include_total)
        print("The response of JobsApi->list_jobs:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling JobsApi->list_jobs: %s\n" % e)
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

### Return type

[**ListJobsResponse**](ListJobsResponse.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Page of jobs |  -  |
**401** | Unauthorized |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **stream_job_events**
> str stream_job_events(id)

Stream a job's status transitions as Server-Sent Events until it reaches a terminal state. Lets clients await completion without polling the REST endpoint themselves.

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
    api_instance = queueflow.JobsApi(api_client)
    id = 'id_example' # str | Job id

    try:
        # Stream a job's status transitions as Server-Sent Events until it reaches a terminal state. Lets clients await completion without polling the REST endpoint themselves.
        api_response = api_instance.stream_job_events(id)
        print("The response of JobsApi->stream_job_events:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling JobsApi->stream_job_events: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Job id | 

### Return type

**str**

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/event-stream, application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | SSE stream; each &#x60;status&#x60; event carries the full job JSON. Closes after the job reaches a terminal state. |  -  |
**401** | Unauthorized |  -  |
**403** | Forbidden |  -  |
**404** | Not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

