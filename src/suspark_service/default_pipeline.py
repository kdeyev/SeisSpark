from su_data.segy_trace_header import SEGY_TRACE_HEADER_ENTRIES, SEGYTraceHeaderEntryName
from suspark.pipeline_repository import PiplineRepository
from suspark_modules.suimp2d import SUimp2dParams
from suspark_modules.susort import SUsortParams


def create_default_pipeline(pipeline_repository: PiplineRepository) -> None:
    id = pipeline_repository.add_pipeline(name="Demo")
    item = pipeline_repository.get_pipeline(id)
    suimp2d = item.pipeline.add_module("SUimp2d")
    suimp2d.set_paramters(SUimp2dParams(nshot=50, nrer=50))
    sucdp = item.pipeline.add_module("SUcdp")
    sort = item.pipeline.add_module("SUsort")
    sort.set_paramters(SUsortParams(key=SEGYTraceHeaderEntryName.cdp))
    sunmo = item.pipeline.add_module("SUnmo")
    sustack = item.pipeline.add_module("SUstack")
    sort = item.pipeline.add_module("SUsort")
    sort.set_paramters(SUsortParams(key=SEGYTraceHeaderEntryName.Crossline3D))
