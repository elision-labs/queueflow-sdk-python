# queueflow.WorkflowsApi

All URIs are relative to *http://localhost:8000*

Method | HTTP request | Description
------------- | ------------- | -------------
[**cancel_workflow**](WorkflowsApi.md#cancel_workflow) | **POST** /api/v1/workflows/{id}/cancel | 
[**create_workflow**](WorkflowsApi.md#create_workflow) | **POST** /api/v1/workflows | 
[**get_workflow**](WorkflowsApi.md#get_workflow) | **GET** /api/v1/workflows/{id} | 
[**get_workflow_diagram**](WorkflowsApi.md#get_workflow_diagram) | **GET** /api/v1/workflows/{id}/diagram | 
[**get_workflow_step_states**](WorkflowsApi.md#get_workflow_step_states) | **GET** /api/v1/workflows/{id}/steps | 
[**list_workflows**](WorkflowsApi.md#list_workflows) | **GET** /api/v1/workflows | 


# **cancel_workflow**
> cancel_workflow(id)



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
    api_instance = queueflow.WorkflowsApi(api_client)
    id = 'id_example' # str | Workflow id

    try:
        api_instance.cancel_workflow(id)
    except Exception as e:
        print("Exception when calling WorkflowsApi->cancel_workflow: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Workflow id | 

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

# **create_workflow**
> CreateWorkflowResponse create_workflow(create_workflow_request)



### Example

* Bearer (API Key) Authentication (bearerAuth):

```python
import queueflow
from queueflow.models.create_workflow_request import CreateWorkflowRequest
from queueflow.models.create_workflow_response import CreateWorkflowResponse
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
    api_instance = queueflow.WorkflowsApi(api_client)
    create_workflow_request = queueflow.CreateWorkflowRequest() # CreateWorkflowRequest | 

    try:
        api_response = api_instance.create_workflow(create_workflow_request)
        print("The response of WorkflowsApi->create_workflow:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkflowsApi->create_workflow: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **create_workflow_request** | [**CreateWorkflowRequest**](CreateWorkflowRequest.md)|  | 

### Return type

[**CreateWorkflowResponse**](CreateWorkflowResponse.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Workflow created |  -  |
**400** | Invalid workflow (e.g. dependency cycle) |  -  |
**401** | Unauthorized |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_workflow**
> Workflow get_workflow(id)



### Example

* Bearer (API Key) Authentication (bearerAuth):

```python
import queueflow
from queueflow.models.workflow import Workflow
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
    api_instance = queueflow.WorkflowsApi(api_client)
    id = 'id_example' # str | Workflow id

    try:
        api_response = api_instance.get_workflow(id)
        print("The response of WorkflowsApi->get_workflow:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkflowsApi->get_workflow: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Workflow id | 

### Return type

[**Workflow**](Workflow.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Workflow |  -  |
**403** | Forbidden |  -  |
**404** | Not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_workflow_diagram**
> WorkflowDiagramResponse get_workflow_diagram(id)



### Example

* Bearer (API Key) Authentication (bearerAuth):

```python
import queueflow
from queueflow.models.workflow_diagram_response import WorkflowDiagramResponse
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
    api_instance = queueflow.WorkflowsApi(api_client)
    id = 'id_example' # str | Workflow id

    try:
        api_response = api_instance.get_workflow_diagram(id)
        print("The response of WorkflowsApi->get_workflow_diagram:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkflowsApi->get_workflow_diagram: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Workflow id | 

### Return type

[**WorkflowDiagramResponse**](WorkflowDiagramResponse.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Mermaid diagram of the workflow DAG |  -  |
**401** | Unauthorized |  -  |
**403** | Forbidden |  -  |
**404** | Not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_workflow_step_states**
> WorkflowStepStatesResponse get_workflow_step_states(id)



### Example

* Bearer (API Key) Authentication (bearerAuth):

```python
import queueflow
from queueflow.models.workflow_step_states_response import WorkflowStepStatesResponse
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
    api_instance = queueflow.WorkflowsApi(api_client)
    id = 'id_example' # str | Workflow id

    try:
        api_response = api_instance.get_workflow_step_states(id)
        print("The response of WorkflowsApi->get_workflow_step_states:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkflowsApi->get_workflow_step_states: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Workflow id | 

### Return type

[**WorkflowStepStatesResponse**](WorkflowStepStatesResponse.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Runtime status of every step, in declaration order. The workflow record carries only step definitions; this is the live progress view. |  -  |
**401** | Unauthorized |  -  |
**403** | Forbidden |  -  |
**404** | Not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_workflows**
> ListWorkflowsResponse list_workflows(status=status, queue=queue, limit=limit, offset=offset, order_by=order_by, include_total=include_total, cursor=cursor, created_after=created_after, created_before=created_before)



### Example

* Bearer (API Key) Authentication (bearerAuth):

```python
import queueflow
from queueflow.models.list_workflows_response import ListWorkflowsResponse
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
    api_instance = queueflow.WorkflowsApi(api_client)
    status = 'status_example' # str | Filter by status (e.g. `pending`, `completed`). (optional)
    queue = 'queue_example' # str | Filter by queue name (jobs only). (optional)
    limit = 56 # int | Page size, 1..=100 (default 50). (optional)
    offset = 56 # int | Number of records to skip (default 0). (optional)
    order_by = 'order_by_example' # str | `created_at ASC` or `created_at DESC` (default DESC). (optional)
    include_total = True # bool | Include the exact `total` count in the response (default false; the count is an extra full scan over the filtered set). (optional)
    cursor = 'cursor_example' # str | Opaque keyset cursor from a previous page's `next_cursor`. When set, `offset` is ignored and listing continues where that page ended. (optional)
    created_after = '2013-10-20T19:20:30+01:00' # datetime | Only rows created at or after this instant (RFC 3339, inclusive). With `created_before` this forms the half-open range `[after, before)` — the natural shape for walking history period by period. (optional)
    created_before = '2013-10-20T19:20:30+01:00' # datetime | Only rows created strictly before this instant (RFC 3339, exclusive). (optional)

    try:
        api_response = api_instance.list_workflows(status=status, queue=queue, limit=limit, offset=offset, order_by=order_by, include_total=include_total, cursor=cursor, created_after=created_after, created_before=created_before)
        print("The response of WorkflowsApi->list_workflows:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkflowsApi->list_workflows: %s\n" % e)
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
 **created_after** | **datetime**| Only rows created at or after this instant (RFC 3339, inclusive). With &#x60;created_before&#x60; this forms the half-open range &#x60;[after, before)&#x60; — the natural shape for walking history period by period. | [optional] 
 **created_before** | **datetime**| Only rows created strictly before this instant (RFC 3339, exclusive). | [optional] 

### Return type

[**ListWorkflowsResponse**](ListWorkflowsResponse.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Page of workflows |  -  |
**401** | Unauthorized |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

