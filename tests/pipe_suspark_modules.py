import pyspark
from pyspark.sql import SparkSession

from su_data.segy_trace_header import SEGY_TRACE_HEADER_ENTRIES, SEGYTraceHeaderEntryName
from su_data.su_pipe import su_process_pipe
from su_rdd.kv_operations import gather_from_rdd_key_value, rdd_flat_key_value_from_gather, rdd_key_value_from_gather
from su_rdd.rdd_operations import group_by_trace_header, su_process_rdd
from suspark.suspark_module import SUfilter, SUimp2d, SUsort

spark_conf = pyspark.SparkConf()
# spark_conf.setAll([
#     ('spark.master', ),
#     ('spark.app.name', 'myApp'),
#     ('spark.submit.deployMode', 'client'),
#     ('spark.ui.showConsoleProgress', 'true'),
#     ('spark.eventLog.enabled', 'false'),
#     ('spark.logConf', 'false'),
#     ('spark.driver.bindAddress', 'vps00'),
#     ('spark.driver.host', 'vps00'),
# ])

spark_sess = SparkSession.builder.config(conf=spark_conf).getOrCreate()
spark_ctxt = spark_sess.sparkContext
spark_reader = spark_sess.read
spark_streamReader = spark_sess.readStream
spark_ctxt.setLogLevel("WARN")

gather_count_to_produce = 10
trace_count_per_gather = 5

input_module = SUimp2d()
input_module.set_paramters(SUimp2d.SUimp2dParams(nshot=gather_count_to_produce, nrec=trace_count_per_gather))
sort = SUsort()
filter = SUfilter()

input_module.init_rdd(spark_ctxt, None)
sort.init_rdd(spark_ctxt, input_module.rdd)
filter.init_rdd(spark_ctxt, sort.rdd)

first_gather = gather_from_rdd_key_value(filter.rdd.first())
assert len(first_gather.traces) == trace_count_per_gather
print(first_gather.traces[0].buffer)
