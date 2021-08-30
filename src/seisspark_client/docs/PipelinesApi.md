# seisspark_client.PipelinesApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_pipeline_module_api_v1_pipelines_pipeline_id_modules_post**](PipelinesApi.md#create_pipeline_module_api_v1_pipelines_pipeline_id_modules_post) | **POST** /api/v1/pipelines/{pipeline_id}/modules | Create Pipeline Module
[**create_pipelines_api_v1_pipelines_post**](PipelinesApi.md#create_pipelines_api_v1_pipelines_post) | **POST** /api/v1/pipelines | Create Pipelines
[**delete_pipeline_api_v1_pipelines_pipeline_id_delete**](PipelinesApi.md#delete_pipeline_api_v1_pipelines_pipeline_id_delete) | **DELETE** /api/v1/pipelines/{pipeline_id} | Delete Pipeline
[**delete_pipeline_module_api_v1_pipelines_pipeline_id_modules_module_id_delete**](PipelinesApi.md#delete_pipeline_module_api_v1_pipelines_pipeline_id_modules_module_id_delete) | **DELETE** /api/v1/pipelines/{pipeline_id}/modules/{module_id} | Delete Pipeline Module
[**get_pipeline_api_v1_pipelines_pipeline_id_get**](PipelinesApi.md#get_pipeline_api_v1_pipelines_pipeline_id_get) | **GET** /api/v1/pipelines/{pipeline_id} | Get Pipeline
[**get_pipeline_module_data_api_v1_pipelines_pipeline_id_modules_module_id_data_key_get**](PipelinesApi.md#get_pipeline_module_data_api_v1_pipelines_pipeline_id_modules_module_id_data_key_get) | **GET** /api/v1/pipelines/{pipeline_id}/modules/{module_id}/data/{key} | Get Pipeline Module Data
[**get_pipeline_module_data_info_api_v1_pipelines_pipeline_id_modules_module_id_keys_get**](PipelinesApi.md#get_pipeline_module_data_info_api_v1_pipelines_pipeline_id_modules_module_id_keys_get) | **GET** /api/v1/pipelines/{pipeline_id}/modules/{module_id}/keys | Get Pipeline Module Data Info
[**get_pipeline_module_parameters_api_v1_pipelines_pipeline_id_modules_module_id_parameters_get**](PipelinesApi.md#get_pipeline_module_parameters_api_v1_pipelines_pipeline_id_modules_module_id_parameters_get) | **GET** /api/v1/pipelines/{pipeline_id}/modules/{module_id}/parameters | Get Pipeline Module Parameters
[**get_pipeline_module_schema_api_v1_pipelines_pipeline_id_modules_module_id_schema_get**](PipelinesApi.md#get_pipeline_module_schema_api_v1_pipelines_pipeline_id_modules_module_id_schema_get) | **GET** /api/v1/pipelines/{pipeline_id}/modules/{module_id}/schema | Get Pipeline Module Schema
[**get_pipeline_modules_api_v1_pipelines_pipeline_id_modules_get**](PipelinesApi.md#get_pipeline_modules_api_v1_pipelines_pipeline_id_modules_get) | **GET** /api/v1/pipelines/{pipeline_id}/modules | Get Pipeline Modules
[**get_pipelines_api_v1_pipelines_get**](PipelinesApi.md#get_pipelines_api_v1_pipelines_get) | **GET** /api/v1/pipelines | Get Pipelines
[**move_pipeline_module_api_v1_pipelines_pipeline_id_modules_put**](PipelinesApi.md#move_pipeline_module_api_v1_pipelines_pipeline_id_modules_put) | **PUT** /api/v1/pipelines/{pipeline_id}/modules | Move Pipeline Module
[**set_pipeline_module_parameters_api_v1_pipelines_pipeline_id_modules_module_id_parameters_put**](PipelinesApi.md#set_pipeline_module_parameters_api_v1_pipelines_pipeline_id_modules_module_id_parameters_put) | **PUT** /api/v1/pipelines/{pipeline_id}/modules/{module_id}/parameters | Set Pipeline Module Parameters


# **create_pipeline_module_api_v1_pipelines_pipeline_id_modules_post**
> ModuleDescription create_pipeline_module_api_v1_pipelines_pipeline_id_modules_post(pipeline_id, create_module_request)

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
    api_response = api_instance.create_pipeline_module_api_v1_pipelines_pipeline_id_modules_post(pipeline_id, create_module_request)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PipelinesApi->create_pipeline_module_api_v1_pipelines_pipeline_id_modules_post: %s\n" % e)
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

# **create_pipelines_api_v1_pipelines_post**
> PipelineInfo create_pipelines_api_v1_pipelines_post(create_pipeline_request)

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
    api_response = api_instance.create_pipelines_api_v1_pipelines_post(create_pipeline_request)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PipelinesApi->create_pipelines_api_v1_pipelines_post: %s\n" % e)
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

# **delete_pipeline_api_v1_pipelines_pipeline_id_delete**
> Any delete_pipeline_api_v1_pipelines_pipeline_id_delete(pipeline_id)

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
    api_response = api_instance.delete_pipeline_api_v1_pipelines_pipeline_id_delete(pipeline_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PipelinesApi->delete_pipeline_api_v1_pipelines_pipeline_id_delete: %s\n" % e)
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

# **delete_pipeline_module_api_v1_pipelines_pipeline_id_modules_module_id_delete**
> Any delete_pipeline_module_api_v1_pipelines_pipeline_id_modules_module_id_delete(pipeline_id, module_id)

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
    api_response = api_instance.delete_pipeline_module_api_v1_pipelines_pipeline_id_modules_module_id_delete(pipeline_id, module_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PipelinesApi->delete_pipeline_module_api_v1_pipelines_pipeline_id_modules_module_id_delete: %s\n" % e)
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

# **get_pipeline_api_v1_pipelines_pipeline_id_get**
> PipelineInfo get_pipeline_api_v1_pipelines_pipeline_id_get(pipeline_id)

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
    api_response = api_instance.get_pipeline_api_v1_pipelines_pipeline_id_get(pipeline_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PipelinesApi->get_pipeline_api_v1_pipelines_pipeline_id_get: %s\n" % e)
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

# **get_pipeline_module_data_api_v1_pipelines_pipeline_id_modules_module_id_data_key_get**
> Any get_pipeline_module_data_api_v1_pipelines_pipeline_id_modules_module_id_data_key_get(pipeline_id, module_id, key)

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
    api_response = api_instance.get_pipeline_module_data_api_v1_pipelines_pipeline_id_modules_module_id_data_key_get(pipeline_id, module_id, key)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PipelinesApi->get_pipeline_module_data_api_v1_pipelines_pipeline_id_modules_module_id_data_key_get: %s\n" % e)
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

# **get_pipeline_module_data_info_api_v1_pipelines_pipeline_id_modules_module_id_keys_get**
> Any get_pipeline_module_data_info_api_v1_pipelines_pipeline_id_modules_module_id_keys_get(pipeline_id, module_id)

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
    api_response = api_instance.get_pipeline_module_data_info_api_v1_pipelines_pipeline_id_modules_module_id_keys_get(pipeline_id, module_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PipelinesApi->get_pipeline_module_data_info_api_v1_pipelines_pipeline_id_modules_module_id_keys_get: %s\n" % e)
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

# **get_pipeline_module_parameters_api_v1_pipelines_pipeline_id_modules_module_id_parameters_get**
> Any get_pipeline_module_parameters_api_v1_pipelines_pipeline_id_modules_module_id_parameters_get(pipeline_id, module_id)

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
    api_response = api_instance.get_pipeline_module_parameters_api_v1_pipelines_pipeline_id_modules_module_id_parameters_get(pipeline_id, module_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PipelinesApi->get_pipeline_module_parameters_api_v1_pipelines_pipeline_id_modules_module_id_parameters_get: %s\n" % e)
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

# **get_pipeline_module_schema_api_v1_pipelines_pipeline_id_modules_module_id_schema_get**
> Any get_pipeline_module_schema_api_v1_pipelines_pipeline_id_modules_module_id_schema_get(pipeline_id, module_id)

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
    api_response = api_instance.get_pipeline_module_schema_api_v1_pipelines_pipeline_id_modules_module_id_schema_get(pipeline_id, module_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PipelinesApi->get_pipeline_module_schema_api_v1_pipelines_pipeline_id_modules_module_id_schema_get: %s\n" % e)
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

# **get_pipeline_modules_api_v1_pipelines_pipeline_id_modules_get**
> List[ModuleInfo] get_pipeline_modules_api_v1_pipelines_pipeline_id_modules_get(pipeline_id)

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
    api_response = api_instance.get_pipeline_modules_api_v1_pipelines_pipeline_id_modules_get(pipeline_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PipelinesApi->get_pipeline_modules_api_v1_pipelines_pipeline_id_modules_get: %s\n" % e)
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

# **get_pipelines_api_v1_pipelines_get**
> List[PipelineInfo] get_pipelines_api_v1_pipelines_get()

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
    api_response = api_instance.get_pipelines_api_v1_pipelines_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PipelinesApi->get_pipelines_api_v1_pipelines_get: %s\n" % e)
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

# **move_pipeline_module_api_v1_pipelines_pipeline_id_modules_put**
> Any move_pipeline_module_api_v1_pipelines_pipeline_id_modules_put(pipeline_id, move_module_request)

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
    api_response = api_instance.move_pipeline_module_api_v1_pipelines_pipeline_id_modules_put(pipeline_id, move_module_request)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PipelinesApi->move_pipeline_module_api_v1_pipelines_pipeline_id_modules_put: %s\n" % e)
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

# **set_pipeline_module_parameters_api_v1_pipelines_pipeline_id_modules_module_id_parameters_put**
> Any set_pipeline_module_parameters_api_v1_pipelines_pipeline_id_modules_module_id_parameters_put(pipeline_id, module_id, body)

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
    api_response = api_instance.set_pipeline_module_parameters_api_v1_pipelines_pipeline_id_modules_module_id_parameters_put(pipeline_id, module_id, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PipelinesApi->set_pipeline_module_parameters_api_v1_pipelines_pipeline_id_modules_module_id_parameters_put: %s\n" % e)
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
