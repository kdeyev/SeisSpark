from su_rdd.kv_operations import gather_from_rdd_key_value
from suspark.suspark_context import SusparkContext
from suspark.suspark_modules_factory import ModulesFactory
from suspark.suspark_pipeline import Pipeline


def test_build_and_run_pipeline1(suspark_context: SusparkContext, modules_factory: ModulesFactory):
    pipeline = Pipeline(suspark_context, modules_factory)

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
    first_gather = gather_from_rdd_key_value(sufilter.rdd.first())

    assert len(first_gather.traces) == trace_count_per_gather
    print(first_gather.traces[0].buffer)


def test_build_and_run_pipeline2(suspark_context: SusparkContext, modules_factory: ModulesFactory):
    pipeline = Pipeline(suspark_context, modules_factory)

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
    first_gather = gather_from_rdd_key_value(sufilter.rdd.first())

    assert len(first_gather.traces) == trace_count_per_gather
    print(first_gather.traces[0].buffer)
