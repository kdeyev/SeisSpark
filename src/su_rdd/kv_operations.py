import os
from typing import List, Tuple

from su_data.encoding import get_data_sample_format
from su_data.segy_trace_header import SEGYTraceHeaderEntry, SEGYTraceHeaderEntryType
from su_data.su_gather import SUGather
from su_data.su_pipe import split_su_buffer, su_process_pipe
from su_data.su_trace import SUTrace
from su_data.su_trace_header import SUTraceHeader, get_header_value

# GatherTuple = namedtuple("GatherTuple", "key buffers")

GatherTuple = Tuple[int, List[bytes]]


def type_check(gather_tuple: GatherTuple) -> GatherTuple:
    # if type(gather_tuple) == tuple:
    #     gather_tuple = (gather_tuple[0], gather_tuple[1])
    # if type(gather_tuple) != GatherTuple:
    #     raise Exception(f"Wrong type(gather_tuple) {type(gather_tuple)}")

    if type(gather_tuple[0]) != int:
        raise Exception(f"Wrong type(gather_tuple[0]) {type(gather_tuple[0])}")

    if type(gather_tuple[1]) != list:
        raise Exception(f"Wrong type(gather_tuple[1]) {type(gather_tuple[1])}")

    if type(gather_tuple[1][0]) != bytes:
        raise Exception(f"Wrong type(gather_tuple[1]) {type(gather_tuple[1][0])}")

    return gather_tuple


class ConvertToFlatList:
    def operation(self, gather_tuple: GatherTuple) -> List[GatherTuple]:
        gather_tuple = type_check(gather_tuple)

        return [(gather_tuple[0], [buffer]) for buffer in gather_tuple[1]]


class SegyRead:
    def __init__(self, file_path: str, chunk_size: int) -> None:
        self._file_path = file_path
        self._chunk_size = chunk_size
        with open(self._file_path, "rb") as file:
            binary_header = file.read(3600)

            out = file.read(240)
            out_trace_header = SUTraceHeader(out)

        type = get_data_sample_format(binary_header)
        if type != SEGYTraceHeaderEntryType.ibm:
            raise Exception("Sample format is not supported")
        self._bps = 4

        filesize = os.path.getsize(self._file_path)
        samp_count = out_trace_header.num_samples
        data_len = samp_count * self._bps
        self._trace_size = data_len + 240
        self._ntraces = int((filesize - 3600) / self._trace_size)

    @property
    def chunk_count(self) -> int:
        return int(self._ntraces / self._chunk_size)

    def get_kv_chunks(self) -> List[Tuple[int, int]]:
        chunk_count = self.chunk_count
        kv = [(chunk, chunk * self._chunk_size) for chunk in range(chunk_count)]
        return kv

    def operation(self, kv: Tuple[int, int]) -> GatherTuple:
        chunk_num: int = kv[0]
        start_trace: int = kv[1]
        to_read = min(self._chunk_size, self._ntraces - start_trace)
        with open(self._file_path, "rb") as file:
            file.seek(3600 + start_trace * self._trace_size)
            data = file.read(to_read * self._trace_size)

        buffers = split_su_buffer(data)
        return (chunk_num, buffers)


class AssignTraceHeaderKey:
    def __init__(self, header_entry: SEGYTraceHeaderEntry):
        self.header_entry = header_entry

    def operation(self, gather_tuple: GatherTuple) -> List[GatherTuple]:
        gather_tuple = type_check(gather_tuple)

        return [(get_header_value(buffer, self.header_entry), [buffer]) for buffer in gather_tuple[1]]


class SelectTraceHeaderKey:
    def __init__(self, header_entry: SEGYTraceHeaderEntry, value: int):
        self._header_entry = header_entry
        self._value = value

    def operation(self, gather_tuple: GatherTuple) -> bool:
        gather_tuple = type_check(gather_tuple)
        if len(gather_tuple[1]) > 1:
            raise Exception("Need to flat")

        ret_val: bool = get_header_value(gather_tuple[1][0], self._header_entry) == self._value
        return ret_val


class SUProcess:
    def __init__(self, su_xecutable: str, parameters: List[str] = []):
        self.su_xecutable = su_xecutable
        self.parameters = parameters

    def operation(self, gather_tuple: GatherTuple) -> GatherTuple:
        gather_tuple = type_check(gather_tuple)
        output_buffers = su_process_pipe([self.su_xecutable, *self.parameters], gather_tuple[1])

        return (gather_tuple[0], output_buffers)


def gather_from_rdd_gather_tuple(gather_tuple: GatherTuple) -> SUGather:
    gather_tuple = type_check(gather_tuple)

    traces = [SUTrace(buffer) for buffer in gather_tuple[1]]
    return SUGather(gather_tuple[0], traces)


def rdd_gather_tuple_from_gather(gather: SUGather) -> GatherTuple:
    return (gather.key, [trace.buffer for trace in gather.traces])


def rdd_flat_gather_tuple_from_gather(gather: SUGather) -> List[GatherTuple]:
    return [(gather.key, [trace.buffer]) for trace in gather.traces]
