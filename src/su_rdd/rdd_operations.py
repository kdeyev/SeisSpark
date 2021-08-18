from typing import List

import pyspark

from su_data.segy_trace_header import SEGYTraceHeaderEntry
from su_rdd.kv_operations import AssignTraceHeaderKey, ConvertToFlatList, SUProcess

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
    rdd = convert_to_flat_map(rdd)
    rdd = rdd.map(AssignTraceHeaderKey(header_entry).operation)
    rdd = rdd.groupByKey().mapValues(list)
    return rdd


def su_process_rdd(rdd: pyspark.RDD, su_xecutable: str, parameters: List[str] = []) -> pyspark.RDD:
    rdd = rdd.map(SUProcess(su_xecutable, parameters).operation)
    return rdd
