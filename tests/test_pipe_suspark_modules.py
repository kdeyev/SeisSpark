from su_rdd.kv_operations import gather_from_rdd_key_value
from suspark.suspark_context import SusparkContext
from suspark.suspark_module import SUfilter, SUimp2d, SUsort


def test_build_and_run_modules(suspark_context: SusparkContext):
    gather_count_to_produce = 10
    trace_count_per_gather = 5

    input_module = SUimp2d()
    input_module.set_paramters(SUimp2d.SUimp2dParams(nshot=gather_count_to_produce, nrec=trace_count_per_gather))
    sort = SUsort()
    filter = SUfilter()

    filter_schema = filter.json_schema
    print(filter_schema)

    input_module.init_rdd(suspark_context, None)
    sort.init_rdd(suspark_context, input_module.rdd)
    filter.init_rdd(suspark_context, sort.rdd)

    first_gather = gather_from_rdd_key_value(filter.rdd.first())
    assert len(first_gather.traces) == trace_count_per_gather
    print(first_gather.traces[0].buffer)
