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
from typing import List, Tuple

import pyspark

from su_data.segy_trace_header import SEGYTraceHeaderEntry
from su_rdd.kv_operations import AssignTraceHeaderKey, ConvertToFlatList, GatherTuple, SegyRead, SelectTraceHeaderKey, SUProcess

# class RDD_SetKeyByHeader:

#     def __init__(self, THN):
#         self._ha = KV_HeaderAccess(THN)

# def set_key_by_trace_header(self, rdd):
#     rdd = RDD_backToFlat(rdd)
#     rdd = rdd.map(self._ha.getHeaderKV)
#     return rdd

# class RDD_GroupByHeader:

#     def __init__(self, THN):
#         self._sk = RDD_SetKeyByHeader(THN)


def convert_to_flat_map(rdd: "pyspark.RDD[GatherTuple]") -> "pyspark.RDD[GatherTuple]":
    return rdd.flatMap(ConvertToFlatList().operation)


def group_by_trace_header(rdd: "pyspark.RDD[GatherTuple]", header_entry: SEGYTraceHeaderEntry) -> "pyspark.RDD[GatherTuple]":
    # rdd = convert_to_flat_map(rdd)
    rdd = rdd.flatMap(AssignTraceHeaderKey(header_entry).operation).mapValues(list)
    rdd = rdd.reduceByKey(lambda a, b: a + b).mapValues(list)
    return rdd


def select_by_trace_header(rdd: "pyspark.RDD[GatherTuple]", header_entry: SEGYTraceHeaderEntry, value: int) -> "pyspark.RDD[GatherTuple]":
    # TODO: we can optimize this operation by skipping convert_to_flat_map
    rdd = convert_to_flat_map(rdd)
    rdd = rdd.filter(SelectTraceHeaderKey(header_entry, value).operation)
    return rdd


def su_process_rdd(rdd: "pyspark.RDD[GatherTuple]", su_xecutable: str, parameters: List[str] = []) -> "pyspark.RDD[GatherTuple]":
    rdd = rdd.map(SUProcess(su_xecutable, parameters).operation)
    return rdd


def get_gather_keys(rdd: "pyspark.RDD[GatherTuple]") -> List[int]:
    keys = rdd.keys().collect()
    keys.sort()
    return keys


def get_gather_by_key(rdd: "pyspark.RDD[GatherTuple]", key: int) -> List[bytes]:
    value = rdd.lookup(key)[0]
    return value


def import_segy_to_rdd(context: pyspark.SparkContext, file_path: str, chunk_size: int) -> "pyspark.RDD[GatherTuple]":
    segy_reader = SegyRead(file_path=file_path, chunk_size=chunk_size)
    kv = segy_reader.get_kv_chunks()
    rdd_kv: "pyspark.RDD[Tuple[int, int]]" = context.parallelize(kv)
    rdd: "pyspark.RDD[GatherTuple]" = rdd_kv.map(segy_reader.operation)
    return rdd
