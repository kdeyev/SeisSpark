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
from seisspark.seisspark_context import SeisSparkContext
from seisspark.seisspark_modules_factory import ModulesFactory
from seisspark.seisspark_pipeline import Pipeline
from su_rdd.kv_operations import gather_from_rdd_gather_tuple


def test_build_and_run_pipeline1(seisspark_context: SeisSparkContext, modules_factory: ModulesFactory) -> None:
    pipeline = Pipeline(seisspark_context, modules_factory)

    suimp2d = pipeline.add_module(module_type="SUimp2d")
    pipeline.add_module(module_type="SUsort", name="SUsort1")
    sufilter = pipeline.add_module(module_type="SUfilter")

    gather_count_to_produce = 10
    trace_count_per_gather = 5

    suimp2d = pipeline.get_module(suimp2d.id)
    suimp2d.set_json_parameters({"nshot": gather_count_to_produce, "nrec": trace_count_per_gather})

    # FIXME: make it automatically after parameters change
    pipeline._init_rdd()

    sufilter = pipeline.get_module(sufilter.id)
    first_gather = gather_from_rdd_gather_tuple(sufilter.rdd.first())

    assert len(first_gather.traces) == trace_count_per_gather
    print(first_gather.traces[0].buffer)


def test_build_and_run_pipeline2(seisspark_context: SeisSparkContext, modules_factory: ModulesFactory) -> None:
    pipeline = Pipeline(seisspark_context, modules_factory)

    suimp2d = pipeline.add_module(module_type="SUimp2d")
    sufilter = pipeline.add_module(module_type="SUfilter")
    pipeline.add_module(module_type="SUsort", prev_module_id=suimp2d.id)

    gather_count_to_produce = 10
    trace_count_per_gather = 5

    suimp2d = pipeline.get_module(suimp2d.id)
    suimp2d.set_json_parameters({"nshot": gather_count_to_produce, "nrec": trace_count_per_gather})

    # FIXME: make it automatically after parameters change
    pipeline._init_rdd()

    sufilter = pipeline.get_module(sufilter.id)
    first_gather = gather_from_rdd_gather_tuple(sufilter.rdd.first())

    assert len(first_gather.traces) == trace_count_per_gather
    print(first_gather.traces[0].buffer)
