# seisspark_client.ModulesApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_module_schema_api_v1_modules_module_type_get**](ModulesApi.md#get_module_schema_api_v1_modules_module_type_get) | **GET** /api/v1/modules/{module_type} | Get Module Schema
[**get_modules_api_v1_modules_get**](ModulesApi.md#get_modules_api_v1_modules_get) | **GET** /api/v1/modules | Get Modules


# **get_module_schema_api_v1_modules_module_type_get**
> Any get_module_schema_api_v1_modules_module_type_get(module_type)

Get Module Schema

### Example

```python
from __future__ import print_function
import time
import seisspark_client
from seisspark_client.rest import ApiException
from pprint import pprint

# Create an instance of the API class
api_instance = seisspark_client.ModulesApi()
module_type = 'module_type_example' # str |

try:
    # Get Module Schema
    api_response = api_instance.get_module_schema_api_v1_modules_module_type_get(module_type)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ModulesApi->get_module_schema_api_v1_modules_module_type_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **module_type** | **str**|  |

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

# **get_modules_api_v1_modules_get**
> List[str] get_modules_api_v1_modules_get()

Get Modules

### Example

```python
from __future__ import print_function
import time
import seisspark_client
from seisspark_client.rest import ApiException
from pprint import pprint

# Create an instance of the API class
api_instance = seisspark_client.ModulesApi()

try:
    # Get Modules
    api_response = api_instance.get_modules_api_v1_modules_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ModulesApi->get_modules_api_v1_modules_get: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

**List[str]**

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
