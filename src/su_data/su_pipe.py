import subprocess
from typing import List

from .su_trace_header import SUTraceHeader


def concatenate_buffers(buffers: List[bytes]) -> bytes:
    out = bytes()
    for buffer in buffers:
        out += buffer
    return out


def split_su_buffer(buffer: bytes) -> List[bytes]:
    out_trace_header = SUTraceHeader(buffer)
    ns = out_trace_header.num_samples
    bps = 4
    trace_len = 240 + bps * ns
    trace_count = int(len(buffer) / trace_len)
    assert trace_len * trace_count == len(buffer)

    out_buffers: List[bytes] = []
    for i in range(trace_count):
        b = buffer[i * trace_len : (i + 1) * trace_len]
        out_buffers.append(b)
    return out_buffers


def su_process_pipe(args: List[str], buffers: List[bytes]) -> List[bytes]:
    # if self._p == None:
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stdin=subprocess.PIPE)

    # simplest communication
    in_data = concatenate_buffers(buffers)
    out, err = p.communicate(input=in_data)
    if err:
        raise Exception(f"su_process_pipe: {err}")
    out_data_array = bytes(out)

    return split_su_buffer(out_data_array)
