from typing import List, Optional

import pyspark

from su_data.segy_trace_header import SEGYTraceHeaderEntry
from su_rdd.kv_operations import AssignTraceHeaderKey, ConvertToFlatList, SegyRead, SelectTraceHeaderKey, SUProcess

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


def convert_to_flat_map(rdd: pyspark.RDD) -> pyspark.RDD:
    return rdd.flatMap(ConvertToFlatList().operation)


def group_by_trace_header(rdd: pyspark.RDD, header_entry: SEGYTraceHeaderEntry) -> pyspark.RDD:
    # rdd = convert_to_flat_map(rdd)
    rdd = rdd.flatMap(AssignTraceHeaderKey(header_entry).operation).mapValues(list)
    rdd = rdd.reduceByKey(lambda a, b: a + b).mapValues(list)
    return rdd


def select_by_trace_header(rdd: pyspark.RDD, header_entry: SEGYTraceHeaderEntry, value: int) -> pyspark.RDD:
    rdd = convert_to_flat_map(rdd)
    rdd = rdd.filter(SelectTraceHeaderKey(header_entry, value).operation)
    return rdd


def su_process_rdd(rdd: pyspark.RDD, su_xecutable: str, parameters: List[str] = []) -> pyspark.RDD:
    rdd = rdd.map(SUProcess(su_xecutable, parameters).operation)
    return rdd


def get_gather_keys(rdd: pyspark.RDD) -> List[int]:
    keys = rdd.keys().collect()
    keys.sort()
    return keys


def get_gather_by_key(rdd: pyspark.RDD, key: int) -> List[bytes]:
    value = rdd.lookup(key)[0]
    return value


def import_segy_to_rdd(context: pyspark.SparkContext, file_path: str, chunk_size: int) -> pyspark.RDD:
    segy_reader = SegyRead(file_path=file_path, chunk_size=chunk_size)
    kv = segy_reader.get_kv_chunks()
    rdd = context.parallelize(kv)
    rdd = rdd.map(segy_reader.operation)
    return rdd
