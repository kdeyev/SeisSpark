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
import subprocess
from typing import List

from su_data.encoding import get_values, set_values
from su_data.segy_trace_header import SEGYTraceHeaderEntryType

from .su_trace_header import SUTraceHeader


def concatenate_buffers(buffers: List[bytes]) -> bytes:
    out = bytes()
    for buffer in buffers:
        out += buffer
    return out


def split_su_buffer(buffer: bytes, sample_type: SEGYTraceHeaderEntryType = SEGYTraceHeaderEntryType.float) -> List[bytes]:
    out_trace_header = SUTraceHeader(buffer)
    ns = out_trace_header.num_samples
    if sample_type != SEGYTraceHeaderEntryType.ibm and sample_type != SEGYTraceHeaderEntryType.float:
        raise Exception("Sample format is not supported")

    bps = 4
    trace_len = 240 + bps * ns
    trace_count = int(len(buffer) / trace_len)
    assert trace_len * trace_count == len(buffer)

    out_buffers: List[bytes] = []
    for i in range(trace_count):
        b = buffer[i * trace_len : (i + 1) * trace_len]
        if sample_type == SEGYTraceHeaderEntryType.ibm:
            body = get_values(buffer=b, index=240, type=SEGYTraceHeaderEntryType.ibm, number=ns)[0]
            out_buffer = bytearray(b)
            set_values(value=body, buffer=out_buffer, index=240, type=SEGYTraceHeaderEntryType.float, number=ns)
            b = bytes(out_buffer)
        out_buffers.append(b)
    return out_buffers


def su_process_pipe(args: List[str], buffers: List[bytes]) -> List[bytes]:
    # if self._p == None:
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stdin=subprocess.PIPE)

    # simplest communication
    in_data = concatenate_buffers(buffers)
    out, err = p.communicate(input=in_data)
    if err:
        raise Exception(f"su_process_pipe: {err.decode()}")
    out_data_array = bytes(out)

    return split_su_buffer(out_data_array)
