import pyspark
from pyspark.sql import SparkSession

from su_rdd.kv_operations import gather_from_rdd_key_value
from suspark.suspark_modules_factory import ModulesFactory, register_module_types
from suspark.suspark_pipeline import Pipeline


def test_build_and_run_pipeline1(spark_ctxt: pyspark.SparkContext, modules_factory: ModulesFactory):
    pipeline = Pipeline(spark_ctxt, modules_factory)
    suimp2d_id = pipeline.add_module("SUimp2d")
    pipeline.add_module("SUsort")
    sufilter_id = pipeline.add_module("SUfilter")

    gather_count_to_produce = 10
    trace_count_per_gather = 5

    with pipeline.get_module_w(suimp2d_id) as suimp2d:
        suimp2d.set_json_parameters({"nshot": gather_count_to_produce, "nrec": trace_count_per_gather})

    with pipeline.get_module_r(sufilter_id) as sufilter:
        first_gather = gather_from_rdd_key_value(sufilter.rdd.first())

    assert len(first_gather.traces) == trace_count_per_gather
    print(first_gather.traces[0].buffer)


def test_build_and_run_pipeline2(spark_ctxt: pyspark.SparkContext, modules_factory: ModulesFactory):
    pipeline = Pipeline(spark_ctxt, modules_factory)
    suimp2d_id = pipeline.add_module("SUimp2d")
    sufilter_id = pipeline.add_module("SUfilter")
    pipeline.add_module("SUsort", suimp2d_id)

    gather_count_to_produce = 10
    trace_count_per_gather = 5

    with pipeline.get_module_w(suimp2d_id) as suimp2d:
        suimp2d.set_json_parameters({"nshot": gather_count_to_produce, "nrec": trace_count_per_gather})

    with pipeline.get_module_r(sufilter_id) as sufilter:
        first_gather = gather_from_rdd_key_value(sufilter.rdd.first())

    assert len(first_gather.traces) == trace_count_per_gather
    print(first_gather.traces[0].buffer)
