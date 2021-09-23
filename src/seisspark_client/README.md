# seisspark-client
No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)

The `seisspark_client` package is automatically generated by the [OpenAPI Generator](https://openapi-generator.tech) project:

- API version: 0.1.0
- Package version: 1.0.0
- Build package: org.openapitools.codegen.languages.PythonClientCodegen

## Requirements.

Python 2.7 and 3.4+

## Installation & Usage

This python library package is generated without supporting files like setup.py or requirements files

To be able to use it, you will need these dependencies in your own package that uses this library:

* urllib3 >= 1.15
* six >= 1.10
* certifi
* python-dateutil

## Getting Started

In your own code, to use this library to connect and interact with seisspark-client,
you can run the following:

```python
from __future__ import print_function
import time
import seisspark_client
from seisspark_client.rest import ApiException
from pprint import pprint


# Defining host is optional and default to http://localhost
configuration.host = "http://localhost"
# Create an instance of the API class
api_instance = seisspark_client.ModulesApi(seisspark_client.ApiClient(configuration))
module_type = 'module_type_example' # str |

try:
    # Get Module Schema
    api_response = api_instance.get_module_schema(module_type)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ModulesApi->get_module_schema: %s\n" % e)

```

## Documentation for API Endpoints

All URIs are relative to *http://localhost*

Class | Method | HTTP request | Description
------------ | ------------- | ------------- | -------------
*ModulesApi* | [**get_module_schema**](docs/ModulesApi.md#get_module_schema) | **GET** /api/v1/modules/{module_type} | Get Module Schema
*ModulesApi* | [**get_modules**](docs/ModulesApi.md#get_modules) | **GET** /api/v1/modules | Get Modules
*PipelinesApi* | [**create_pipeline_module**](docs/PipelinesApi.md#create_pipeline_module) | **POST** /api/v1/pipelines/{pipeline_id}/modules | Create Pipeline Module
*PipelinesApi* | [**create_pipeline**](docs/PipelinesApi.md#create_pipeline) | **POST** /api/v1/pipelines | Create Pipelines
*PipelinesApi* | [**delete_pipeline**](docs/PipelinesApi.md#delete_pipeline) | **DELETE** /api/v1/pipelines/{pipeline_id} | Delete Pipeline
*PipelinesApi* | [**delete_pipeline_module**](docs/PipelinesApi.md#delete_pipeline_module) | **DELETE** /api/v1/pipelines/{pipeline_id}/modules/{module_id} | Delete Pipeline Module
*PipelinesApi* | [**get_pipeline**](docs/PipelinesApi.md#get_pipeline) | **GET** /api/v1/pipelines/{pipeline_id} | Get Pipeline
*PipelinesApi* | [**get_pipeline_module_data**](docs/PipelinesApi.md#get_pipeline_module_data) | **GET** /api/v1/pipelines/{pipeline_id}/modules/{module_id}/data/{key} | Get Pipeline Module Data
*PipelinesApi* | [**get_pipeline_module_data_info**](docs/PipelinesApi.md#get_pipeline_module_data_info) | **GET** /api/v1/pipelines/{pipeline_id}/modules/{module_id}/keys | Get Pipeline Module Data Info
*PipelinesApi* | [**get_pipeline_module_parameters**](docs/PipelinesApi.md#get_pipeline_module_parameters) | **GET** /api/v1/pipelines/{pipeline_id}/modules/{module_id}/parameters | Get Pipeline Module Parameters
*PipelinesApi* | [**get_pipeline_module_schema**](docs/PipelinesApi.md#get_pipeline_module_schema) | **GET** /api/v1/pipelines/{pipeline_id}/modules/{module_id}/schema | Get Pipeline Module Schema
*PipelinesApi* | [**get_pipeline_modules**](docs/PipelinesApi.md#get_pipeline_modules) | **GET** /api/v1/pipelines/{pipeline_id}/modules | Get Pipeline Modules
*PipelinesApi* | [**get_pipelines**](docs/PipelinesApi.md#get_pipelines) | **GET** /api/v1/pipelines | Get Pipelines
*PipelinesApi* | [**move_pipeline_module**](docs/PipelinesApi.md#move_pipeline_module) | **PUT** /api/v1/pipelines/{pipeline_id}/modules | Move Pipeline Module
*PipelinesApi* | [**set_pipeline_module_parameters**](docs/PipelinesApi.md#set_pipeline_module_parameters) | **PUT** /api/v1/pipelines/{pipeline_id}/modules/{module_id}/parameters | Set Pipeline Module Parameters


## Documentation For Models

 - [CreateModuleRequest](docs/CreateModuleRequest.md)
 - [CreatePipelineRequest](docs/CreatePipelineRequest.md)
 - [HTTPValidationError](docs/HTTPValidationError.md)
 - [ModuleDescription](docs/ModuleDescription.md)
 - [ModuleInfo](docs/ModuleInfo.md)
 - [MoveModuleRequest](docs/MoveModuleRequest.md)
 - [PipelineInfo](docs/PipelineInfo.md)
 - [ValidationError](docs/ValidationError.md)


## Documentation For Authorization

 All endpoints do not require authorization.

## Author