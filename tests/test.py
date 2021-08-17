from typing import Any, List
import pyspark
from su_data.segy_trace_header import SEGYTraceHeaderEntry, SEGYTraceHeaderEntryName, SEGY_TRACE_HEADER_ENTRYS

from su_data.su_pipe import su_process_pipe
from pyspark.sql import SparkSession

from su_rdd.rdd_operations import group_by_trace_header

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
 
spark_sess          = SparkSession.builder.config(conf=spark_conf).getOrCreate()
spark_ctxt          = spark_sess.sparkContext
spark_reader        = spark_sess.read
spark_streamReader  = spark_sess.readStream
spark_ctxt.setLogLevel("WARN")

output_traces = su_process_pipe(["suplane"], [])

rdd = spark_ctxt.parallelize([(None, trace.buffer) for trace in output_traces])
print(rdd.first())

rdd = group_by_trace_header(rdd, SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.cdp])
print(rdd.count())