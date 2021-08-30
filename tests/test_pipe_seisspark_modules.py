from su_rdd.kv_operations import gather_from_rdd_gather_tuple
from seisspark.seisspark_context import SeisSparkContext
from seisspark_modules.sufilter import SUfilter
from seisspark_modules.suimp2d import SUimp2d, SUimp2dParams
from seisspark_modules.susort import SUsort


def test_build_and_run_modules(seisspark_context: SeisSparkContext) -> None:
    gather_count_to_produce = 10
    trace_count_per_gather = 5

    input_module = SUimp2d(id="1", name="b")
    input_module.set_paramters(SUimp2dParams(nshot=gather_count_to_produce, nrec=trace_count_per_gather))
    sort = SUsort(id="1", name="b")
    filter = SUfilter(id="1", name="b")

    filter_schema = filter.params_schema
    print(filter_schema)

    input_module.init_rdd(seisspark_context, None)
    sort.init_rdd(seisspark_context, input_module.rdd)
    filter.init_rdd(seisspark_context, sort.rdd)

    first_gather = gather_from_rdd_gather_tuple(filter.rdd.first())
    assert len(first_gather.traces) == trace_count_per_gather
    print(first_gather.traces[0].buffer)
