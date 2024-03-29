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
import struct
from typing import Any, List, Tuple, cast

import numpy as np

from .segy_trace_header import DATA_SAMPLE_FORMAT_HEADER, DATA_SAMPLE_FORMAT_MAPPING, SEGYTraceHeaderEntryType

endian = ">"  # Big Endian  # modified by A Squelch
# endian='<' # Little Endian
# endian='=' # Native

l_int = struct.calcsize("i")
l_uint = struct.calcsize("I")
l_long = 4
# Next line gives wrong result on Linux!! (gives 8 instead of 4)
# l_long = struct.calcsize('l')
l_ulong = struct.calcsize("L")
l_short = struct.calcsize("h")
l_ushort = struct.calcsize("H")
l_char = struct.calcsize("c")
l_uchar = struct.calcsize("B")
l_float = struct.calcsize("f")


# def putValue(value, fileid, index, ctype='l', endian='>', number=1):
#     """
#     putValue(data,index,ctype,endian,number)
#     """
#     if (ctype == 'l') | (ctype == 'long') | (ctype == 'int32'):
#         size = l_long
#         ctype = 'l'
#         value=int(value)
#     elif (ctype == 'L') | (ctype == 'ulong') | (ctype == 'uint32'):
#         size = l_ulong
#         ctype = 'L'
#         value=int(value)
#     elif (ctype == 'h') | (ctype == 'short') | (ctype == 'int16'):
#         size = l_short
#         ctype = 'h'
#         value=int(value)
#     elif (ctype == 'H') | (ctype == 'ushort') | (ctype == 'uint16'):
#         size = l_ushort
#         ctype = 'H'
#         value=int(value)
#     elif (ctype == 'c') | (ctype == 'char'):
#         size = l_char
#         ctype = 'c'
#     elif (ctype == 'B') | (ctype == 'uchar'):
#         size = l_uchar
#         ctype = 'B'
#     elif (ctype == 'f') | (ctype == 'float'):
#         size = l_float
#         ctype = 'f'
#     elif (ctype == 'ibm'):
#         size = l_float
#     else:
#         raise Exception(f"Wrong type: {ctype}")

#     cformat = endian + ctype * number

#     #printverbose('putValue : cformat :  "' + cformat + '" ctype="' + ctype + '"'  + '   value="' + value + '"', -1)
#     # printverbose('cformat="%s", ctype="%s", value=%f' % (cformat,ctype,value), 40 )
#     strVal = struct.pack(cformat, value)
#     fileid.seek(index)
#     fileid.write(strVal)

#     return 1


def get_value(buffer: bytes, index: int, type: SEGYTraceHeaderEntryType, endian: str = ">") -> Any:
    value, index_end = get_values(buffer, index, type, endian, 1)
    return value[0]


def get_ctype_and_size(type: SEGYTraceHeaderEntryType) -> Tuple[str, int]:
    ctype: str
    size: int
    if type == SEGYTraceHeaderEntryType.int32:
        size = l_long
        ctype = "l"
    elif type == SEGYTraceHeaderEntryType.uint32:
        size = l_ulong
        ctype = "L"
    elif type == SEGYTraceHeaderEntryType.int16:
        size = l_short
        ctype = "h"
    elif type == SEGYTraceHeaderEntryType.uint16:
        size = l_ushort
        ctype = "H"
    elif type == SEGYTraceHeaderEntryType.char:
        size = l_char
        ctype = "c"
    elif type == SEGYTraceHeaderEntryType.uchar:
        size = l_uchar
        ctype = "B"
    elif type == SEGYTraceHeaderEntryType.float:
        size = l_float
        ctype = "f"
    elif type == SEGYTraceHeaderEntryType.ibm:
        size = l_float
        ctype = "ibm"
    else:
        raise Exception(f"Wrong type: {type}")

    return ctype, size


def get_values(buffer: bytes, index: int, type: SEGYTraceHeaderEntryType, endian: str = ">", number: int = 1) -> Tuple[List[Any], int]:
    ctype: str
    size: int
    ctype, size = get_ctype_and_size(type)

    index_end = index + size * number

    # printverbose("index=%d, number=%d, size=%d, ctype=%s" % (index, number, size, ctype), 8);
    # printverbose("index, index_end = " + str(index) + "," + str(index_end), 9)

    if ctype == "ibm":
        # ASSUME IBM FLOAT DATA
        value: List[float] = list(range(int(number)))
        for i in np.arange(number):
            index_ibm_start = i * 4 + index
            index_ibm_end = index_ibm_start + 4
            ibm_val = ibm2ieee2(buffer[index_ibm_start:index_ibm_end])
            value[i] = ibm_val
        # this resturn an array as opposed to a tuple
        return value, index_end
    else:
        # ALL OTHER TYPES OF DATA
        cformat = "f" * number
        cformat = endian + ctype * number

        Value: Tuple[Any, ...] = struct.unpack(cformat, buffer[index:index_end])
        return list(Value), index_end


def set_values(value: List[Any], buffer: bytearray, index: int, type: SEGYTraceHeaderEntryType, endian: str = ">", number: int = 1) -> None:
    ctype, size = get_ctype_and_size(type)

    cformat = endian + ctype * number

    struct.pack_into(cformat, buffer, index, *value)


def ibm2ieee2(ibm_float: bytes) -> float:
    """
    ibm2ieee2(ibm_float)
    Used by permission
    (C) Secchi Angelo
    with thanks to Howard Lightstone and Anton Vredegoor.
    """
    dividend = float(16 ** 6)

    # if ibm_float == 0:
    #     return 0.0
    istic, a, b, c = struct.unpack(">BBBB", ibm_float)
    if istic >= 128:
        sign = -1.0
        istic = istic - 128
    else:
        sign = 1.0
    mant = float(a << 16) + float(b << 8) + float(c)
    return cast(float, sign * 16 ** (istic - 64) * (mant / dividend))


def get_data_sample_format(buffer: bytes) -> SEGYTraceHeaderEntryType:
    value = get_value(buffer, index=DATA_SAMPLE_FORMAT_HEADER.position, type=DATA_SAMPLE_FORMAT_HEADER.type)
    if value == 0:
        value = 5
    return DATA_SAMPLE_FORMAT_MAPPING[value]


def get_bytes_per_sample(buffer: bytes) -> int:
    type = get_data_sample_format(buffer)
    ctype, size = get_ctype_and_size(type)
    return size
