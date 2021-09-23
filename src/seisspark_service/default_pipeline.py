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
from seisspark.pipeline_repository import PiplineRepository
from seisspark.seisspark_pipeline import GraphNodeConnection
from seisspark_modules.suimp2d import SUimp2dParams
from seisspark_modules.susort import SUsortParams
from su_data.segy_trace_header import SEGYTraceHeaderEntryName


def create_default_pipeline(pipeline_repository: PiplineRepository) -> None:
    id = pipeline_repository.add_pipeline(name="Syntetic demo")
    item = pipeline_repository.get_pipeline(id)
    suimp2d = item.pipeline.add_module("SUimp2d")
    suimp2d.set_paramters(SUimp2dParams(nshot=50, nrec=50))
    sucdp = item.pipeline.add_module("SUcdp", producers=[GraphNodeConnection(suimp2d.id, 0)])
    sort = item.pipeline.add_module("SUsort", producers=[GraphNodeConnection(sucdp.id, 0)])
    sort.set_paramters(SUsortParams(key=SEGYTraceHeaderEntryName.cdp))
    sunmo = item.pipeline.add_module("SUnmo", producers=[GraphNodeConnection(sort.id, 0)])
    sustack = item.pipeline.add_module("SUstack", producers=[GraphNodeConnection(sunmo.id, 0)])
    sort = item.pipeline.add_module("SUsort", producers=[GraphNodeConnection(sustack.id, 0)])
    sort.set_paramters(SUsortParams(key=SEGYTraceHeaderEntryName.Crossline3D))
    item.pipeline.add_module("SUfilter", producers=[GraphNodeConnection(sort.id, 0)])

    # id = pipeline_repository.add_pipeline(name="2D Line demo")
    # item = pipeline_repository.get_pipeline(id)
    # item.pipeline.add_module("ImportSegy")
    # item.pipeline.add_module("SelectTraces")
    # sort = item.pipeline.add_module("SUsort")
    # item.pipeline.add_module("SUagc")
