import os

import segypy
from hadoop.io import BytesWritable, IntWritable, SequenceFile

# import pydoop.hdfs as hdfs


def importSGY(sgyFilename, rddFilename):

    # os.remove(rddFilename)
    fp = open(sgyFilename, "rb")
    writer = SequenceFile.createWriter(rddFilename, IntWritable, BytesWritable)

    SH = segypy.getSegyHeader(sgyFilename, 3600, segypy.endian)
    bps = segypy.getBytePerSample(SH)

    filesize = os.path.getsize(sgyFilename)
    samp_count = SH["ns"]
    data_len = samp_count * bps
    trace_size = data_len + 240
    ntraces = (filesize - 3600) / trace_size

    fp.read(3600)
    for trace_num in range(ntraces):
        SegyTraceHeader = fp.read(240)
        SegyTraceData = fp.read(data_len)
        error - segypy.getValue is not correct
        SegyTraceData = segypy.getValue(SegyTraceData, 0, "float", segypy.endian, samp_count)
        writer.append(IntWritable(trace_num), BytesWritable(str(SegyTraceHeader) + str(SegyTraceData)))


def exportSGY(rddFilename, sgyFilename):
    reader = SequenceFile.Reader(rddFilename)

    key_class = reader.getKeyClass()
    value_class = reader.getValueClass()

    key = key_class()
    value = value_class()

    # reader.sync(4042)
    position = reader.getPosition()
    while reader.next(key, value):
        print("*" if reader.syncSeen() else " ", f"[{position:>6}] {key.toString():>6} {value.toString():>6}")
        position = reader.getPosition()

    reader.close()


if __name__ == "__main__":
    print(hdfs.ls("/"))

    # exportSGY ('7o_5m_final_vtap.segy', 'poststack.sgy')
    importSGY("synth.su", "poststack.sgy")
