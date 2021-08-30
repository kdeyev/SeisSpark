# =============================================================================
# Copyright (c) 2021 SeisSpark (https://github.com/kdeyev/SeisSpark).
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =============================================================================
from typing import List

import pydantic
from fastapi.testclient import TestClient

from seisspark.pipeline_repository import PipelineInfo
from seisspark_service.routers.pipelines import CreateModuleRequest, CreatePipelineRequest, ModuleDescription, PipelineDescription


def test_seisspark_service_modules(seisspark_service_client: TestClient) -> None:
    response = seisspark_service_client.get("/api/v1/modules")
    response.raise_for_status()
    module_types: List[str] = pydantic.parse_obj_as(List[str], response.json())
    assert module_types == ["SUfilter", "SUsort", "SUimp2d"]

    response = seisspark_service_client.get("/api/v1/modules/SUfilter")
    response.raise_for_status()
    module_schema = response.json()
    assert module_schema == {
        "title": "SUFilterParams",
        "type": "object",
        "properties": {"filter": {"title": "Filter", "default": [], "type": "array", "items": {"$ref": "#/definitions/SUFilterFA"}}},
        "definitions": {"SUFilterFA": {"title": "SUFilterFA", "type": "object", "properties": {"f": {"title": "F", "type": "number"}, "a": {"title": "A", "type": "number"}}, "required": ["f", "a"]}},
    }


def test_seisspark_service_pipelines(seisspark_service_client: TestClient) -> None:
    response = seisspark_service_client.get("/api/v1/pipelines")
    response.raise_for_status()
    pipelines: List[PipelineInfo] = pydantic.parse_obj_as(List[PipelineInfo], response.json())
    assert pipelines == []

    pipeline_name = "test_pipeline"
    response = seisspark_service_client.post("/api/v1/pipelines", json=CreatePipelineRequest(name=pipeline_name).dict())
    response.raise_for_status()
    pipeline_info: PipelineInfo = pydantic.parse_obj_as(PipelineInfo, response.json())
    assert pipeline_info.name == pipeline_name

    pipeline_id = pipeline_info.id
    response = seisspark_service_client.get(f"/api/v1/pipelines/{pipeline_id}")
    response.raise_for_status()
    pipeline_desc: PipelineDescription = pydantic.parse_obj_as(PipelineDescription, response.json())
    assert pipeline_desc.id == pipeline_id and pipeline_desc.name == pipeline_name and pipeline_desc.modules == []

    response = seisspark_service_client.get("/api/v1/pipelines")
    response.raise_for_status()
    pipelines = pydantic.parse_obj_as(List[PipelineInfo], response.json())
    assert pipelines == [PipelineInfo(id=pipeline_id, name=pipeline_name)]

    response = seisspark_service_client.delete(f"/api/v1/pipelines/{pipeline_id}")
    response.raise_for_status()

    response = seisspark_service_client.get("/api/v1/pipelines")
    response.raise_for_status()
    pipelines = pydantic.parse_obj_as(List[PipelineInfo], response.json())
    assert pipelines == []


def test_seisspark_service_pipeline_module(seisspark_service_client: TestClient) -> None:
    response = seisspark_service_client.get("/api/v1/pipelines")
    response.raise_for_status()
    pipelines: List[PipelineInfo] = pydantic.parse_obj_as(List[PipelineInfo], response.json())
    assert pipelines == []

    pipeline_name = "test_pipeline"
    response = seisspark_service_client.post("/api/v1/pipelines", json=CreatePipelineRequest(name=pipeline_name).dict())
    response.raise_for_status()
    pipeline_info: PipelineInfo = pydantic.parse_obj_as(PipelineInfo, response.json())
    assert pipeline_info.name == pipeline_name
    pipeline_id = pipeline_info.id

    module_type = "SUimp2d"
    module_name = "input"
    response = seisspark_service_client.post(f"/api/v1/pipelines/{pipeline_id}/modules", json=CreateModuleRequest(module_type=module_type, name=module_name).dict())
    response.raise_for_status()
    module_descr: ModuleDescription = pydantic.parse_obj_as(ModuleDescription, response.json())
    assert module_descr.name == module_name
    module_id = module_descr.id

    response = seisspark_service_client.get(f"/api/v1/pipelines/{pipeline_id}/modules/{module_id}/parameters")
    response.raise_for_status()
    json_parameters = response.json()
    assert type(json_parameters) == dict

    response = seisspark_service_client.get(f"/api/v1/pipelines/{pipeline_id}/modules/{module_id}/data")
    response.raise_for_status()
    json_data = response.json()
    assert type(json_data) == list and type(json_data[0]) == list and type(json_data[0][0]) == float

    response = seisspark_service_client.delete(f"/api/v1/pipelines/{pipeline_id}/modules/{module_id}")
    response.raise_for_status()

    response = seisspark_service_client.delete(f"/api/v1/pipelines/{pipeline_id}")
    response.raise_for_status()
