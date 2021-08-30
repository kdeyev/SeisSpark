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
from seisspark.pipeline_repository import PipelineInfo, PiplineRepository
from seisspark.seisspark_context import SeisSparkContext
from seisspark.seisspark_modules_factory import ModulesFactory


def test_pipeline_registry(seisspark_context: SeisSparkContext, modules_factory: ModulesFactory) -> None:
    pipeline_repo = PiplineRepository(seisspark_context=seisspark_context, modules_factory=modules_factory)

    name = "my pipe"
    id = pipeline_repo.add_pipeline(name)
    item1 = pipeline_repo.get_pipeline(id)
    assert item1.name == name

    name = "another pipe"
    id = pipeline_repo.add_pipeline(name)
    item2 = pipeline_repo.get_pipeline(id)

    assert item2.name == name

    ids = pipeline_repo.get_pipeline_ids()
    assert len(ids) == 2
    assert PipelineInfo(id=item1.id, name=item1.name) in ids and PipelineInfo(id=item2.id, name=item2.name) in ids
