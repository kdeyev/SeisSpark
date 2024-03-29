# =============================================================================
# Copyright (c) 2021 SeisSpark (https://github.com/kdeyev/SeisSpark).
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =============================================================================
from seisspark.seisspark_context import SeisSparkContext
from su_data.segy_trace_header import SEGY_TRACE_HEADER_ENTRIES, SEGYTraceHeaderEntryName
from su_data.su_pipe import su_process_pipe
from su_rdd.kv_operations import gather_from_rdd_gather_tuple, rdd_flat_gather_tuple_from_gather, rdd_gather_tuple_from_gather
from su_rdd.rdd_operations import group_by_trace_header, import_segy_to_rdd, su_process_rdd

gather_count_to_produce = 10
trace_count_per_gather = 5


def test_rdd_gather_tuple_from_gather(seisspark_context: SeisSparkContext) -> None:

    buffers = su_process_pipe(["suimp2d", f"nshot={gather_count_to_produce}", f"nrec={trace_count_per_gather}"], [])
    input_gather = gather_from_rdd_gather_tuple((0, buffers))

    header_entries = input_gather.get_header_entry_values(SEGY_TRACE_HEADER_ENTRIES[SEGYTraceHeaderEntryName.FieldRecord])
    expected = []
    for gather_num in range(1, gather_count_to_produce + 1):
        expected += [gather_num] * trace_count_per_gather
    assert header_entries == expected

    # Create an RDD from in memory buffers
    rdd = seisspark_context.context.parallelize([rdd_gather_tuple_from_gather(input_gather)])
    # rdd = rdd.mapValues(list)

    # Create an RDD from in-memory gather
    rdd = group_by_trace_header(rdd, SEGY_TRACE_HEADER_ENTRIES[SEGYTraceHeaderEntryName.FieldRecord])
    assert rdd.count() == gather_count_to_produce

    # Get the first gather
    first_gather = gather_from_rdd_gather_tuple(rdd.first())
    assert first_gather.trace_count == trace_count_per_gather

    #
    header_entries = first_gather.get_header_entry_values(SEGY_TRACE_HEADER_ENTRIES[SEGYTraceHeaderEntryName.TraceNumber])
    assert header_entries == list(trace_num for trace_num in range(1, trace_count_per_gather + 1))


def test_rdd_flat_gather_tuple_from_gather(seisspark_context: SeisSparkContext) -> None:
    buffers = su_process_pipe(["suimp2d", f"nshot={gather_count_to_produce}", f"nrec={trace_count_per_gather}"], [])
    input_gather = gather_from_rdd_gather_tuple((0, buffers))

    header_entries = input_gather.get_header_entry_values(SEGY_TRACE_HEADER_ENTRIES[SEGYTraceHeaderEntryName.FieldRecord])
    expected = []
    for gather_num in range(1, gather_count_to_produce + 1):
        expected += [gather_num] * trace_count_per_gather
    assert header_entries == expected

    # Create an RDD from in-memory gather
    rdd = seisspark_context.context.parallelize(rdd_flat_gather_tuple_from_gather(input_gather))
    # rdd = rdd.mapValues(list)

    # Group traces by ffid
    rdd = group_by_trace_header(rdd, SEGY_TRACE_HEADER_ENTRIES[SEGYTraceHeaderEntryName.FieldRecord])
    assert rdd.count() == gather_count_to_produce

    # s = rdd.first()
    # print(type(s))

    # Get the first gather
    first_gather = gather_from_rdd_gather_tuple(rdd.first())
    assert first_gather.trace_count == trace_count_per_gather

    #
    header_entries = first_gather.get_header_entry_values(SEGY_TRACE_HEADER_ENTRIES[SEGYTraceHeaderEntryName.TraceNumber])
    assert header_entries == list(trace_num for trace_num in range(1, trace_count_per_gather + 1))

    rdd = su_process_rdd(rdd, "sufilter", ["f1=10,f2=20,f3=30,f4-40"])

    # Group traces by ffid
    rdd = group_by_trace_header(rdd, SEGY_TRACE_HEADER_ENTRIES[SEGYTraceHeaderEntryName.FieldRecord])
    assert rdd.count() == gather_count_to_produce

    first_gather = gather_from_rdd_gather_tuple(rdd.first())
    print(first_gather.traces[0].buffer)


def test_rdd_import_segy_to_rdd_file(seisspark_context: SeisSparkContext) -> None:
    rdd = import_segy_to_rdd(seisspark_context.context, "/root/SeisSpark/Line_001_ieee.sgy", 1000)

    first_gather = gather_from_rdd_gather_tuple(rdd.first())
    print(first_gather.traces[0].buffer)

    # rdd.saveAsSequenceFile("/root/SeisSpark/Line_001_ieee.seq")
