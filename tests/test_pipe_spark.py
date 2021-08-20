from su_data.segy_trace_header import SEGY_TRACE_HEADER_ENTRIES, SEGYTraceHeaderEntryName
from su_data.su_pipe import su_process_pipe
from su_rdd.kv_operations import gather_from_rdd_key_value, rdd_flat_key_value_from_gather, rdd_key_value_from_gather
from su_rdd.rdd_operations import group_by_trace_header, su_process_rdd
from suspark.suspark_context import SusparkContext

gather_count_to_produce = 10
trace_count_per_gather = 5


def test_rdd_key_value_from_gather(suspark_context: SusparkContext):

    buffers = su_process_pipe(["suimp2d", f"nshot={gather_count_to_produce}", f"nrec={trace_count_per_gather}"], [])
    input_gather = gather_from_rdd_key_value((None, buffers))

    header_entries = input_gather.get_header_entry_values(SEGY_TRACE_HEADER_ENTRIES[SEGYTraceHeaderEntryName.FieldRecord])
    expected = []
    for gather_num in range(1, gather_count_to_produce + 1):
        expected += [gather_num] * trace_count_per_gather
    assert header_entries == expected

    # Create an RDD from in memory buffers
    rdd = suspark_context.context.parallelize([rdd_key_value_from_gather(input_gather)])

    # Create an RDD from in-memory gather
    rdd = group_by_trace_header(rdd, SEGY_TRACE_HEADER_ENTRIES[SEGYTraceHeaderEntryName.FieldRecord])
    assert rdd.count() == gather_count_to_produce

    # Get the first gather
    first_gather = gather_from_rdd_key_value(rdd.first())
    assert first_gather.trace_count == trace_count_per_gather

    #
    header_entries = first_gather.get_header_entry_values(SEGY_TRACE_HEADER_ENTRIES[SEGYTraceHeaderEntryName.TraceNumber])
    assert header_entries == list(trace_num for trace_num in range(1, trace_count_per_gather + 1))


def test_rdd_flat_key_value_from_gather(suspark_context: SusparkContext):
    buffers = su_process_pipe(["suimp2d", f"nshot={gather_count_to_produce}", f"nrec={trace_count_per_gather}"], [])
    input_gather = gather_from_rdd_key_value((None, buffers))

    header_entries = input_gather.get_header_entry_values(SEGY_TRACE_HEADER_ENTRIES[SEGYTraceHeaderEntryName.FieldRecord])
    expected = []
    for gather_num in range(1, gather_count_to_produce + 1):
        expected += [gather_num] * trace_count_per_gather
    assert header_entries == expected

    # Create an RDD from in-memory gather
    rdd = suspark_context.context.parallelize(rdd_flat_key_value_from_gather(input_gather))

    # Group traces by ffid
    rdd = group_by_trace_header(rdd, SEGY_TRACE_HEADER_ENTRIES[SEGYTraceHeaderEntryName.FieldRecord])
    assert rdd.count() == gather_count_to_produce

    # Get the first gather
    first_gather = gather_from_rdd_key_value(rdd.first())
    assert first_gather.trace_count == trace_count_per_gather

    #
    header_entries = first_gather.get_header_entry_values(SEGY_TRACE_HEADER_ENTRIES[SEGYTraceHeaderEntryName.TraceNumber])
    assert header_entries == list(trace_num for trace_num in range(1, trace_count_per_gather + 1))

    rdd = su_process_rdd(rdd, "sufilter", ["f1=10,f2=20,f3=30,f4-40"])

    # Group traces by ffid
    rdd = group_by_trace_header(rdd, SEGY_TRACE_HEADER_ENTRIES[SEGYTraceHeaderEntryName.FieldRecord])
    assert rdd.count() == gather_count_to_produce

    first_gather = gather_from_rdd_key_value(rdd.first())
    print(first_gather.traces[0].buffer)
