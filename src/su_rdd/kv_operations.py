from collections import namedtuple
from typing import Any, List, Tuple

from su_data.segy_trace_header import SEGYTraceHeaderEntry
from su_data.su_gather import SUGather
from su_data.su_pipe import su_process_pipe
from su_data.su_trace import SUTrace
from su_data.su_trace_header import get_header_value

GatherTuple = namedtuple("GatherTuple", "key buffers")


def type_check(gather_tuple: GatherTuple) -> GatherTuple:
    if type(gather_tuple) == tuple:
        gather_tuple = GatherTuple(gather_tuple[0], gather_tuple[1])
    # if type(gather_tuple) != GatherTuple:
    #     raise Exception(f"Wrong type(gather_tuple) {type(gather_tuple)}")

    if type(gather_tuple.key) != int:
        raise Exception(f"Wrong type(gather_tuple.key) {type(gather_tuple.key)}")

    if type(gather_tuple.buffers) != list:
        raise Exception(f"Wrong type(gather_tuple.buffers) {type(gather_tuple.buffers)}")

    if type(gather_tuple.buffers[0]) != bytes:
        raise Exception(f"Wrong type(gather_tuple.buffers) {type(gather_tuple.buffers[0])}")

    return gather_tuple


# class ConvertToFlatList:
#     def operation(self, gather_tuple: GatherTuple) -> List[GatherTuple]:
#         gather_tuple = type_check(gather_tuple)

#         return [GatherTuple(gather_tuple.key, [buffer]) for buffer in gather_tuple.buffers]


class AssignTraceHeaderKey:
    def __init__(self, header_entry: SEGYTraceHeaderEntry):
        self.header_entry = header_entry

    def operation(self, gather_tuple: GatherTuple) -> List[GatherTuple]:
        gather_tuple = type_check(gather_tuple)

        return [GatherTuple(get_header_value(buffer, self.header_entry), [buffer]) for buffer in gather_tuple.buffers]


class SUProcess:
    def __init__(self, su_xecutable: str, parameters: List[str] = []):
        self.su_xecutable = su_xecutable
        self.parameters = parameters

    def operation(self, gather_tuple: GatherTuple) -> GatherTuple:
        gather_tuple = type_check(gather_tuple)
        output_buffers = su_process_pipe([self.su_xecutable, *self.parameters], gather_tuple.buffers)

        return GatherTuple(gather_tuple.key, output_buffers)


def gather_from_rdd_gather_tuple(gather_tuple: GatherTuple) -> SUGather:
    gather_tuple = type_check(gather_tuple)

    traces = [SUTrace(buffer) for buffer in gather_tuple.buffers]
    return SUGather(gather_tuple.key, traces)


def rdd_gather_tuple_from_gather(gather: SUGather) -> GatherTuple:
    return GatherTuple(gather.key, [trace.buffer for trace in gather.traces])


def rdd_flat_gather_tuple_from_gather(gather: SUGather) -> List[GatherTuple]:
    return [GatherTuple(gather.key, [trace.buffer]) for trace in gather.traces]
