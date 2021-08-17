

from typing import Any, List, Tuple

from su_data.segy_trace_header import SEGYTraceHeaderEntry
from su_data.su_gather import SUGather
from su_data.su_trace import SUTrace
from su_data.su_trace_header import SUTraceHeader, get_header_value

class ConvertToFlatList:
    def operation(self, key_trace: Tuple[Any, bytes]) -> Tuple[Any, bytes]:
        if type(key_trace) != tuple:
            raise Exception(f"Wrong key_trace type {type(key_trace)}")

        value = key_trace[1]
        if type(value) is list:
            return list([(None, v) for v in value])
        elif type(value) is bytes:
            return list([(None, value)])
        else:
            raise Exception(f"Wrong value type {type(value)}")


class AssignTraceHeaderKey:
    def __init__(self, header_entry: SEGYTraceHeaderEntry):
        self.header_entry = header_entry

    def operation(self, key_trace: Tuple[Any, bytes]) -> Tuple[Any, bytes]:
        if type(key_trace) != tuple and type(key_trace[1]) != bytes:
            raise Exception(f"Wrong key_trace type {type(key_trace)}")

        trace_buffer = key_trace[1]
        header_value = get_header_value(trace_buffer, self.header_entry)

        return (header_value, trace_buffer)

def gather_from_rdd_key_value(key_value: Tuple[Any, List[bytes]]) -> SUGather:
    if type(key_value) != tuple and type(key_value[1]) != list:
        raise Exception(f"Wrong key_trace type {type(key_value)}")

    key, buffers = key_value
    traces = [SUTrace(buffer) for buffer in buffers]
    return SUGather(key, traces)