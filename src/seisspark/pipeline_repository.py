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
import uuid
from typing import Dict, List

import pydantic

from seisspark.seisspark_context import SeisSparkContext
from seisspark.seisspark_modules_factory import ModulesFactory
from seisspark.seisspark_pipeline import Pipeline


class PipelineInfo(pydantic.BaseModel):
    id: str
    name: str


class PiplineRepositoryItem:
    def __init__(self, id: str, name: str, pipeline: Pipeline) -> None:
        self._id = id
        self._name = name
        self._pipeline = pipeline

    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def pipeline(self) -> Pipeline:
        return self._pipeline


class PiplineRepository:
    def __init__(self, seisspark_context: SeisSparkContext, modules_factory: ModulesFactory) -> None:
        self._seisspark_context = seisspark_context
        self._modules_factory = modules_factory
        self._items: Dict[str, PiplineRepositoryItem] = {}

    def add_pipeline(self, name: str) -> str:
        id = str(uuid.uuid4())

        pipeline = Pipeline(seisspark_context=self._seisspark_context, modules_factory=self._modules_factory)
        item = PiplineRepositoryItem(id=id, name=name, pipeline=pipeline)
        self._items[id] = item

        return id

    def get_pipeline(self, id: str) -> PiplineRepositoryItem:
        return self._items[id]

    def get_pipeline_ids(self) -> List[PipelineInfo]:
        return [PipelineInfo(id=item.id, name=item.name) for item in self._items.values()]

    def delete_pipeline(self, id: str) -> None:
        del self._items[id]
