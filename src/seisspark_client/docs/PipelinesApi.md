# seisspark_client.PipelinesApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_pipeline_module**](PipelinesApi.md#create_pipeline_module) | **POST** /api/v1/pipelines/{pipeline_id}/modules | Create Pipeline Module
[**create_pipeline**](PipelinesApi.md#create_pipeline) | **POST** /api/v1/pipelines | Create Pipelines
[**delete_pipeline**](PipelinesApi.md#delete_pipeline) | **DELETE** /api/v1/pipelines/{pipeline_id} | Delete Pipeline
[**delete_pipeline_module**](PipelinesApi.md#delete_pipeline_module) | **DELETE** /api/v1/pipelines/{pipeline_id}/modules/{module_id} | Delete Pipeline Module
[**get_pipeline**](PipelinesApi.md#get_pipeline) | **GET** /api/v1/pipelines/{pipeline_id} | Get Pipeline
[**get_pipeline_module_data**](PipelinesApi.md#get_pipeline_module_data) | **GET** /api/v1/pipelines/{pipeline_id}/modules/{module_id}/data/{key} | Get Pipeline Module Data
[**get_pipeline_module_data_info**](PipelinesApi.md#get_pipeline_module_data_info) | **GET** /api/v1/pipelines/{pipeline_id}/modules/{module_id}/keys | Get Pipeline Module Data Info
[**get_pipeline_module_parameters**](PipelinesApi.md#get_pipeline_module_parameters) | **GET** /api/v1/pipelines/{pipeline_id}/modules/{module_id}/parameters | Get Pipeline Module Parameters
[**get_pipeline_module_schema**](PipelinesApi.md#get_pipeline_module_schema) | **GET** /api/v1/pipelines/{pipeline_id}/modules/{module_id}/schema | Get Pipeline Module Schema
[**get_pipeline_modules**](PipelinesApi.md#get_pipeline_modules) | **GET** /api/v1/pipelines/{pipeline_id}/modules | Get Pipeline Modules
[**get_pipelines**](PipelinesApi.md#get_pipelines) | **GET** /api/v1/pipelines | Get Pipelines
[**move_pipeline_module**](PipelinesApi.md#move_pipeline_module) | **PUT** /api/v1/pipelines/{pipeline_id}/modules | Move Pipeline Module
[**set_pipeline_module_parameters**](PipelinesApi.md#set_pipeline_module_parameters) | **PUT** /api/v1/pipelines/{pipeline_id}/modules/{module_id}/parameters | Set Pipeline Module Parameters


# **create_pipeline_module**
> ModuleDescription create_pipeline_module(pipeline_id, create_module_request)

Create Pipeline Module

### Example

```python
from __future__ import print_function
import time
import seisspark_client
from seisspark_client.rest import ApiException
from pprint import pprint

# Create an instance of the API class
api_instance = seisspark_client.PipelinesApi()
pipeline_id = 'pipeline_id_example' # str |
create_module_request = seisspark_client.CreateModuleRequest() # CreateModuleRequest |

try:
    # Create Pipeline Module
    api_response = api_instance.create_pipeline_module(pipeline_id, create_module_request)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PipelinesApi->create_pipeline_module: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **pipeline_id** | **str**|  |
 **create_module_request** | [**CreateModuleRequest**](CreateModuleRequest.md)|  |

### Return type

[**ModuleDescription**](ModuleDescription.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_pipeline**
> PipelineInfo create_pipeline(create_pipeline_request)

Create Pipelines

### Example

```python
from __future__ import print_function
import time
import seisspark_client
from seisspark_client.rest import ApiException
from pprint import pprint

# Create an instance of the API class
api_instance = seisspark_client.PipelinesApi()
create_pipeline_request = seisspark_client.CreatePipelineRequest() # CreatePipelineRequest |

try:
    # Create Pipelines
    api_response = api_instance.create_pipeline(create_pipeline_request)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PipelinesApi->create_pipeline: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **create_pipeline_request** | [**CreatePipelineRequest**](CreatePipelineRequest.md)|  |

### Return type

[**PipelineInfo**](PipelineInfo.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_pipeline**
> Any delete_pipeline(pipeline_id)

Delete Pipeline

### Example

```python
from __future__ import print_function
import time
import seisspark_client
from seisspark_client.rest import ApiException
from pprint import pprint

# Create an instance of the API class
api_instance = seisspark_client.PipelinesApi()
pipeline_id = 'pipeline_id_example' # str |

try:
    # Delete Pipeline
    api_response = api_instance.delete_pipeline(pipeline_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PipelinesApi->delete_pipeline: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **pipeline_id** | **str**|  |

### Return type

[**Any**](Any.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_pipeline_module**
> Any delete_pipeline_module(pipeline_id, module_id)

Delete Pipeline Module

### Example

```python
from __future__ import print_function
import time
import seisspark_client
from seisspark_client.rest import ApiException
from pprint import pprint

# Create an instance of the API class
api_instance = seisspark_client.PipelinesApi()
pipeline_id = 'pipeline_id_example' # str |
module_id = 'module_id_example' # str |

try:
    # Delete Pipeline Module
    api_response = api_instance.delete_pipeline_module(pipeline_id, module_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PipelinesApi->delete_pipeline_module: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **pipeline_id** | **str**|  |
 **module_id** | **str**|  |

### Return type

[**Any**](Any.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_pipeline**
> PipelineInfo get_pipeline(pipeline_id)

Get Pipeline

### Example

```python
from __future__ import print_function
import time
import seisspark_client
from seisspark_client.rest import ApiException
from pprint import pprint

# Create an instance of the API class
api_instance = seisspark_client.PipelinesApi()
pipeline_id = 'pipeline_id_example' # str |

try:
    # Get Pipeline
    api_response = api_instance.get_pipeline(pipeline_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PipelinesApi->get_pipeline: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **pipeline_id** | **str**|  |

### Return type

[**PipelineInfo**](PipelineInfo.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_pipeline_module_data**
> Any get_pipeline_module_data(pipeline_id, module_id, key)

Get Pipeline Module Data

### Example

```python
from __future__ import print_function
import time
import seisspark_client
from seisspark_client.rest import ApiException
from pprint import pprint

# Create an instance of the API class
api_instance = seisspark_client.PipelinesApi()
pipeline_id = 'pipeline_id_example' # str |
module_id = 'module_id_example' # str |
key = 56 # int |

try:
    # Get Pipeline Module Data
    api_response = api_instance.get_pipeline_module_data(pipeline_id, module_id, key)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PipelinesApi->get_pipeline_module_data: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **pipeline_id** | **str**|  |
 **module_id** | **str**|  |
 **key** | **int**|  |

### Return type

[**Any**](Any.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_pipeline_module_data_info**
> Any get_pipeline_module_data_info(pipeline_id, module_id)

Get Pipeline Module Data Info

### Example

```python
from __future__ import print_function
import time
import seisspark_client
from seisspark_client.rest import ApiException
from pprint import pprint

# Create an instance of the API class
api_instance = seisspark_client.PipelinesApi()
pipeline_id = 'pipeline_id_example' # str |
module_id = 'module_id_example' # str |

try:
    # Get Pipeline Module Data Info
    api_response = api_instance.get_pipeline_module_data_info(pipeline_id, module_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PipelinesApi->get_pipeline_module_data_info: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **pipeline_id** | **str**|  |
 **module_id** | **str**|  |

### Return type

[**Any**](Any.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_pipeline_module_parameters**
> Any get_pipeline_module_parameters(pipeline_id, module_id)

Get Pipeline Module Parameters

### Example

```python
from __future__ import print_function
import time
import seisspark_client
from seisspark_client.rest import ApiException
from pprint import pprint

# Create an instance of the API class
api_instance = seisspark_client.PipelinesApi()
pipeline_id = 'pipeline_id_example' # str |
module_id = 'module_id_example' # str |

try:
    # Get Pipeline Module Parameters
    api_response = api_instance.get_pipeline_module_parameters(pipeline_id, module_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PipelinesApi->get_pipeline_module_parameters: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **pipeline_id** | **str**|  |
 **module_id** | **str**|  |

### Return type

[**Any**](Any.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_pipeline_module_schema**
> Any get_pipeline_module_schema(pipeline_id, module_id)

Get Pipeline Module Schema

### Example

```python
from __future__ import print_function
import time
import seisspark_client
from seisspark_client.rest import ApiException
from pprint import pprint

# Create an instance of the API class
api_instance = seisspark_client.PipelinesApi()
pipeline_id = 'pipeline_id_example' # str |
module_id = 'module_id_example' # str |

try:
    # Get Pipeline Module Schema
    api_response = api_instance.get_pipeline_module_schema(pipeline_id, module_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PipelinesApi->get_pipeline_module_schema: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **pipeline_id** | **str**|  |
 **module_id** | **str**|  |

### Return type

[**Any**](Any.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_pipeline_modules**
> List[ModuleInfo] get_pipeline_modules(pipeline_id)

Get Pipeline Modules

### Example

```python
from __future__ import print_function
import time
import seisspark_client
from seisspark_client.rest import ApiException
from pprint import pprint

# Create an instance of the API class
api_instance = seisspark_client.PipelinesApi()
pipeline_id = 'pipeline_id_example' # str |

try:
    # Get Pipeline Modules
    api_response = api_instance.get_pipeline_modules(pipeline_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PipelinesApi->get_pipeline_modules: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **pipeline_id** | **str**|  |

### Return type

[**List[ModuleInfo]**](ModuleInfo.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_pipelines**
> List[PipelineInfo] get_pipelines()

Get Pipelines

### Example

```python
from __future__ import print_function
import time
import seisspark_client
from seisspark_client.rest import ApiException
from pprint import pprint

# Create an instance of the API class
api_instance = seisspark_client.PipelinesApi()

try:
    # Get Pipelines
    api_response = api_instance.get_pipelines()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PipelinesApi->get_pipelines: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**List[PipelineInfo]**](PipelineInfo.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **move_pipeline_module**
> Any move_pipeline_module(pipeline_id, move_module_request)

Move Pipeline Module

### Example

```python
from __future__ import print_function
import time
import seisspark_client
from seisspark_client.rest import ApiException
from pprint import pprint

# Create an instance of the API class
api_instance = seisspark_client.PipelinesApi()
pipeline_id = 'pipeline_id_example' # str |
move_module_request = seisspark_client.MoveModuleRequest() # MoveModuleRequest |

try:
    # Move Pipeline Module
    api_response = api_instance.move_pipeline_module(pipeline_id, move_module_request)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PipelinesApi->move_pipeline_module: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **pipeline_id** | **str**|  |
 **move_module_request** | [**MoveModuleRequest**](MoveModuleRequest.md)|  |

### Return type

[**Any**](Any.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **set_pipeline_module_parameters**
> Any set_pipeline_module_parameters(pipeline_id, module_id, body)

Set Pipeline Module Parameters

### Example

```python
from __future__ import print_function
import time
import seisspark_client
from seisspark_client.rest import ApiException
from pprint import pprint

# Create an instance of the API class
api_instance = seisspark_client.PipelinesApi()
pipeline_id = 'pipeline_id_example' # str |
module_id = 'module_id_example' # str |
body = seisspark_client.Any() # Any |

try:
    # Set Pipeline Module Parameters
    api_response = api_instance.set_pipeline_module_parameters(pipeline_id, module_id, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PipelinesApi->set_pipeline_module_parameters: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **pipeline_id** | **str**|  |
 **module_id** | **str**|  |
 **body** | **Any**|  |

### Return type

[**Any**](Any.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)
