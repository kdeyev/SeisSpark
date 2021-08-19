import pyspark
from pyspark.sql import SparkSession

from su_rdd.kv_operations import gather_from_rdd_key_value
from suspark.suspark_module import SUfilter, SUimp2d, SUsort


def test_build_and_run_modules(spark_ctxt: pyspark.SparkContext):
    gather_count_to_produce = 10
    trace_count_per_gather = 5

    input_module = SUimp2d()
    input_module.set_paramters(SUimp2d.SUimp2dParams(nshot=gather_count_to_produce, nrec=trace_count_per_gather))
    sort = SUsort()
    filter = SUfilter()

    filter_schema = filter.json_schema
    print(filter_schema)

    input_module.init_rdd(spark_ctxt, None)
    sort.init_rdd(spark_ctxt, input_module.rdd)
    filter.init_rdd(spark_ctxt, sort.rdd)

    first_gather = gather_from_rdd_key_value(filter.rdd.first())
    assert len(first_gather.traces) == trace_count_per_gather
    print(first_gather.traces[0].buffer)
