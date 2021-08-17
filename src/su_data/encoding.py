import struct

import numpy as np

from .segy_trace_header import SEGYTraceHeaderEntryType

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


def get_value(data: bytes, index: int, type: SEGYTraceHeaderEntryType, endian: str = ">"):
    value, index_end = get_values(data, index, type, endian, 1)
    return value[0]


def get_values(data, index, type: SEGYTraceHeaderEntryType, endian: str = ">", number: int = 1):
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

    index_end = index + size * number

    # printverbose("index=%d, number=%d, size=%d, ctype=%s" % (index, number, size, ctype), 8);
    # printverbose("index, index_end = " + str(index) + "," + str(index_end), 9)

    if ctype == "ibm":
        # ASSUME IBM FLOAT DATA
        Value = list(range(int(number)))
        for i in np.arange(number):
            index_ibm_start = i * 4 + index
            index_ibm_end = index_ibm_start + 4
            ibm_val = ibm2ieee2(data[index_ibm_start:index_ibm_end])
            Value[i] = ibm_val
        # this resturn an array as opposed to a tuple
    else:
        # ALL OTHER TYPES OF DATA
        cformat = "f" * number
        cformat = endian + ctype * number

        # printverbose("getValue : cformat : '" + cformat + "'", 11)

        Value = struct.unpack(cformat, data[index:index_end])

    # if (ctype == 'B'):
    #     # printverbose('getValue : Ineficient use of 1byte Integer...', -1)

    #     vtxt = 'getValue : ' + 'start=' + str(index) + ' size=' + str(size) + ' number=' + str(
    #         number) + ' Value=' + str(Value) + ' cformat=' + str(cformat)
    #     # printverbose(vtxt, 20)

    # if number == 1:
    #     return Value[0], index_end
    # else:
    return Value, index_end


def ibm2ieee2(ibm_float):
    """
    ibm2ieee2(ibm_float)
    Used by permission
    (C) Secchi Angelo
    with thanks to Howard Lightstone and Anton Vredegoor.
    """
    dividend = float(16 ** 6)

    if ibm_float == 0:
        return 0.0
    istic, a, b, c = struct.unpack(">BBBB", ibm_float)
    if istic >= 128:
        sign = -1.0
        istic = istic - 128
    else:
        sign = 1.0
    mant = float(a << 16) + float(b << 8) + float(c)
    return sign * 16 ** (istic - 64) * (mant / dividend)
