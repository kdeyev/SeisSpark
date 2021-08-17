import subprocess

from typing import List

from .su_trace_header import SUTraceHeader

from .su_trace import SUTrace

def concatenate_buffers(buffers: List[bytes]) -> bytes:
    out = bytes()
    for buffer in buffers:
        out += buffer
    return out

def su_process_pipe(args: List[str], buffers: List[bytes]) -> List[bytes]:
    # if self._p == None:
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stdin=subprocess.PIPE)

    # simplest communication
    in_data = concatenate_buffers(buffers)
    out, err = p.communicate(input=in_data)
    if err: 
        raise Exception(f"su_process_pipe: {err}")
    out_data_array = bytes(out)
    
    out_trace_header = SUTraceHeader(out_data_array)
    ns = out_trace_header.num_samples
    bps = 4
    trace_len = 240+bps*ns
    trace_count = int (len(out_data_array)/trace_len)
    assert (trace_len*trace_count == len(out_data_array))

    out_buffers: List[bytes] = []
    for i in range(trace_count):
        buffer = out_data_array[i*trace_len:(i+1)*trace_len]
        out_buffers.append(buffer)
    
    return out_buffers