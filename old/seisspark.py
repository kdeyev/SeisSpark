"""
   Copyright 2016 Kostya Deyev

   Licensed under the Apache License, Version 2.0 (the License);
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       httpwww.apache.orglicensesLICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an AS IS BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

import segypy
import seisspark_config
from seisspark_config import dprint

def KV_flatList(kv):
    assert (type(kv) is tuple)
    out = list()
    values = kv[1]
    if type(values) is list:
        for value in values:
            out.append((None, value))
    else:
        if type(values) is not bytearray:
            dprint("KV_flatList error: ", type(values))
        assert (type(values) is bytearray)
        out.append((None, values))
    return out


def KV_concatenateByteArray(kvlist):
    out = bytearray()
    assert (type(kvlist) is list)
    for kv in kvlist:
        value = kv[1]
        assert (type(value) is bytearray)
        out.extend(value)
    return out

def concatenateByteArray(vlist):
    out = bytearray()
    assert (type(vlist) is list)
    for v in vlist:
        assert (type(v) is bytearray)
        out.extend(v)
    return out
    
def RDD_backToFlat(rdd):
    rdd = rdd.flatMap(KV_flatList)
    #rdd = rdd.map (lambda x: (None, x[0]))
    return rdd


def RDD_printKeys(rdd, n=1000):
    # for i in range (1, 10):
    #    print ('KEYS')
    kvlist = rdd.take(n)
    for kv in kvlist:
        assert (type(kv) is tuple)
        print('KEY ' + str(kv[0]))


def RDD_test(st, rdd):
    print(st)
    kv = rdd.take(1)[0]
    ok = True
    if type(kv) is not tuple:
        print('KV type', type(kv))
        ok = False
#    assert (type (kv) is tuple)
    print("KEY", kv[0])
    values = kv[1]
    if type(values) is list:
        print("GATHER len", len(values), "trace len", len(values[0]))
        if type(values[0]) is not bytearray:
            print('Trace type', type(values[0]))
            ok = False
#        assert (type (values[0]) is bytearray)
    else:
        if type(values) is not bytearray:
            print('Trace type', type(values))
            ok = False
#        assert (type (values) is bytearray)
        print("Trace len", len(values))
    if ok == False:
        print(st, 'Failed!')
        exit(0)
    print(st, 'Ok')


def RDD_printValue(rdd):
    kv = rdd.take(1)
    assert (type(kv) is tuple)
    print(kv[0])
    values = kv[1]
    if type(values) is list:
        print(len(values))
        for value in values:
            print(value)
    else:
        assert (type(values) is bytearray)
        print(values)


def KV_printValue(kv):
    assert (type(kv) is tuple)
    print(kv[0])
    values = kv[1]
    if type(values) is list:
        print(len(values))
        for value in values:
            print(value)
    else:
        assert (type(values) is bytearray)
        print(values)


class KV_HeaderAccess:

    def __init__(self, THN):
        self._THN = THN

    def getHeaderKV(self, kv):
        assert (type(kv) is tuple)
        assert (type(kv[1]) is bytearray)

        data = kv[1]

        value = self.getHeaderV(data)

        return (value, data)

    def getHeaderV(self, data):
        assert (type(data) is bytearray)

        THpos = segypy.STH_def[self._THN]["pos"]

        THformat = segypy.STH_def[self._THN]["type"]

        segypy.printverbose('THN ' + str(self._THN))
        segypy.printverbose('THpos ' + str(THpos))
        segypy.printverbose('THformat ' + str(THformat))
        segypy.printverbose('data ' + str(data))

        value, index = segypy.getValue(data, THpos, THformat, segypy.endian, 1)

        return value


class KV_HeaderFilter:

    def __init__(self, THN, first, last):
        self._ha = KV_HeaderAccess(THN)
        self._first = first
        self._last = last

    def filtKV(self, kv):
        assert (type(kv) is tuple)
        assert (type(kv[1]) is bytearray)

        key = kv[0]
        data = kv[1]
        value = self._ha.getHeaderV(data)
        return value >= self._first and value <= self._last

# output is flat


class RDD_SetKeyByHeader:

    def __init__(self, THN):
        self._ha = KV_HeaderAccess(THN)

    def do(self, rdd):
        dprint("SetKeyByHeader")
        rdd = RDD_backToFlat(rdd)
        rdd = rdd.map(self._ha.getHeaderKV)
        if seisspark_config.debug:
            RDD_test("End SetKeyByHeader", rdd)
        return rdd

# output is gather


class RDD_GroupByHeader:

    def __init__(self, THN):
        self._sk = RDD_SetKeyByHeader(THN)

    def do(self, rdd):
        dprint("GroupByHeader")
        rdd = RDD_backToFlat(rdd)
        rdd = self._sk.do(rdd)  # set key
        rdd = rdd.groupByKey().mapValues(list)
        #rdd = rdd.sortByKey()
        if seisspark_config.debug:
            RDD_test("End GroupByHeader", rdd)
        return rdd

# output is flat


class RDD_FilterByHeader:

    def __init__(self, THN, first, last):
        self._hf = KV_HeaderFilter(THN, first, last)

    def do(self, rdd):
        if seisspark_config.debug:
            dprint("FilterByHeader")
        rdd = RDD_backToFlat(rdd)
        rdd = rdd.filter(self._hf.filtKV)
        if seisspark_config.debug:
            RDD_test("End FilterByHeader", rdd)
        return rdd

# input and output are gathers


class RDD_Processing:

    def __init__(self, args):
        self._args = args
        self._p = None
        dprint('RDD_Processing', args)
        return

    def pipe(self, kv):
        import subprocess

        assert (type(kv) is tuple)
        assert (type(kv[1]) is list)  # should be gather
        assert (type(kv[1][0]) is bytearray)  # should be trace

        # if self._p == None:
        p = subprocess.Popen(
            self._args, stdout=subprocess.PIPE, stdin=subprocess.PIPE)

        # simplest communication
        in_data = concatenateByteArray(kv[1])
        out, err = p.communicate(input=in_data)
        out_data_array = bytearray(out)
        dprint('ERROR STREAM', err)
        
        ns = KV_HeaderAccess('ns').getHeaderV(out_data_array)
        bps = 4
        trace_len = 240+bps*ns
        trace_count = int (len(out_data_array)/trace_len)
        assert (trace_len*trace_count == len(out_data_array))

        out_data = []
        for i in range(trace_count):
            trace = out_data_array[i*trace_len:(i+1)*trace_len]
            out_data.append(trace)
        

#        in_data = kv[1]
#        for d in in_data:
#            self._p.stdin.write(d)  # write one by one
#        self._p.stdin.close()
#
#        out_data = []
#        while True:
#            head = bytearray(self._p.stdout.read(240))
#            if not head:
#                break
#
#            head = bytearray(head)
#            ns = KV_HeaderAccess('ns').getHeaderV(head)
#            bps = 4
#
#            body = self._p.stdout.read(ns * bps)
#            if not body:
#                print('cannot read trace body')
#                exit(1)
#            body = bytearray(body)
#
#            data = head
#            head.extend(body)
#
#            out_data.append(data)

        # TODO optimization sometimes i can use kv[0] as new key
        return (None, out_data)

    def do(self, rdd):
        dprint("RDD_Processing")
		##
		## TODO why we do not use spark pipe?!!!!
		##
        rdd = rdd.map(self.pipe)
        if seisspark_config.debug:
            RDD_test("End RDD_Processing", rdd)
        return rdd


def loadData(sc, filename, sort=None):
    rdd = sc.sequenceFile(filename)
    if seisspark_config.debug:
        RDD_test("loadData", rdd)
    if sort != None:
        rdd = RDD_GroupByHeader(sort).do(rdd)
    if seisspark_config.debug:
        RDD_test("End loadData", rdd)
    return rdd


def saveData(rdd, filename):
    dprint("saveData")
    rdd = RDD_backToFlat(rdd)
    rdd.saveAsSequenceFile(filename)


def prepareRDDtoDraw(rdd, count=None):
    dprint("prepareRDDtoDraw")

    from numpy import transpose
    from numpy import reshape
    import struct
    rdd = RDD_backToFlat(rdd)
    if count == None:
        DataFromRDD = rdd.collect()
    else:
        DataFromRDD = rdd.take(count)

    assert (type(DataFromRDD) is list)
    assert (type(DataFromRDD[0]) is tuple)
    assert (type(DataFromRDD[0][1]) is bytearray)

    first_trace = DataFromRDD[0][1]
    ns = KV_HeaderAccess('ns').getHeaderV(first_trace)
    dt = KV_HeaderAccess('dt').getHeaderV(first_trace)
    ntraces = len(DataFromRDD)
    bps = 4
    ndummy_samples = 240 / bps
    number = ntraces * (ns + ndummy_samples)

    # concatenate to single bytearray
    Data = KV_concatenateByteArray(DataFromRDD)

    header = []
    for d in DataFromRDD:
        header.append(d[1][0:240])

    # convert to matrix
    Data = struct.unpack(segypy.endian + 'f' * number, Data)
    Data = reshape(Data, (ntraces, ns + ndummy_samples))
    Data = Data[:, ndummy_samples:(ns + ndummy_samples)]
    Data = transpose(Data)
    dprint("End prepareRDDtoDraw")
    return Data, header


def drawRDD(rdd, label, count=None):
    Data, header = prepareRDDtoDraw(rdd, count)
    segypy.imageSegy(Data, label, 'jet')
