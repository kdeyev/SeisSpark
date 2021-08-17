from typing import Any, List
import pyspark
from su_data.segy_trace_header import SEGYTraceHeaderEntry, SEGYTraceHeaderEntryName, SEGY_TRACE_HEADER_ENTRIES
from su_data.su_gather import SUGather

from su_data.su_pipe import su_process_pipe
from pyspark.sql import SparkSession
from su_data.su_trace import SUTrace
from su_rdd.kv_operations import gather_from_rdd_key_value, rdd_flat_key_value_from_gather, rdd_key_value_from_gather

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

gather_count_to_produce = 10
trace_count_per_gather = 5

def test_rdd_key_value_from_gather():

    buffers = su_process_pipe(["suimp2d", f"nshot={gather_count_to_produce}", f"nrec={trace_count_per_gather}"], [])
    input_gather = gather_from_rdd_key_value((None, buffers))

    header_entries  = input_gather.get_header_entry_values(SEGY_TRACE_HEADER_ENTRIES[SEGYTraceHeaderEntryName.FieldRecord])
    expected = []
    for gather_num in range(1, gather_count_to_produce+1):
        expected += [gather_num]*trace_count_per_gather
    assert header_entries == expected

    # Create an RDD from in memory buffers
    rdd = spark_ctxt.parallelize([rdd_key_value_from_gather(input_gather)])

    # Create an RDD from in-memory gather
    rdd = group_by_trace_header(rdd, SEGY_TRACE_HEADER_ENTRIES[SEGYTraceHeaderEntryName.FieldRecord])
    assert rdd.count() == gather_count_to_produce

    # Get the first gather
    first_gather = gather_from_rdd_key_value(rdd.first())
    assert first_gather.trace_count == trace_count_per_gather

    # 
    header_entries  = first_gather.get_header_entry_values(SEGY_TRACE_HEADER_ENTRIES[SEGYTraceHeaderEntryName.TraceNumber])
    assert header_entries == list(trace_num for trace_num in range(1, trace_count_per_gather+1))

def test_rdd_flat_key_value_from_gather():
    buffers = su_process_pipe(["suimp2d", f"nshot={gather_count_to_produce}", f"nrec={trace_count_per_gather}"], [])
    input_gather = gather_from_rdd_key_value((None, buffers))

    header_entries  = input_gather.get_header_entry_values(SEGY_TRACE_HEADER_ENTRIES[SEGYTraceHeaderEntryName.FieldRecord])
    expected = []
    for gather_num in range(1, gather_count_to_produce+1):
        expected += [gather_num]*trace_count_per_gather
    assert header_entries == expected

    # Create an RDD from in-memory gather
    rdd = spark_ctxt.parallelize(rdd_flat_key_value_from_gather(input_gather))

    # Group traces by ffid
    rdd = group_by_trace_header(rdd, SEGY_TRACE_HEADER_ENTRIES[SEGYTraceHeaderEntryName.FieldRecord])
    assert rdd.count() == gather_count_to_produce

    # Get the first gather
    first_gather = gather_from_rdd_key_value(rdd.first())
    assert first_gather.trace_count == trace_count_per_gather

    # 
    header_entries  = first_gather.get_header_entry_values(SEGY_TRACE_HEADER_ENTRIES[SEGYTraceHeaderEntryName.TraceNumber])
    assert header_entries == list(trace_num for trace_num in range(1, trace_count_per_gather+1))