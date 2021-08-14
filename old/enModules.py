#!/usr/bin/env python2
# -*- coding: utf-8 -*-
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

"""
Created on Mon Nov 14 13:21:12 2016

@author: kdeyev
"""
from enParam import *
import random
import seisspark_config
import seisspark
import segypy

from seisspark_config import dprint

from pyspark import SparkContext, SparkConf

#######
# Spark
#######
s_conf = SparkConf()
s_conf.setAppName("SeisSpark")
if seisspark_config.local_spark:
    s_conf.setMaster("local")
s_sc = SparkContext(conf=s_conf)
s_sc.addPyFile("seisspark_config.py")
s_sc.addPyFile("seisspark.py")
s_sc.addPyFile("segypy.py")
#s_sc = None

###
# Base Module
###

g_traceHeaderList = segypy.STH_def.keys()


class MetaRDD ():

    def __init__(self, sort):
        self._sort = sort


class BaseModule ():

    def __init__(self, appInstance, uName, name, params=Params([])):
        self.init(appInstance, uName, name, params)

    def remove(self):
        pass

    def init(self, appInstance, uName, name, params=Params([])):
        import copy
        self._appInstance = appInstance
        self._uName = uName
        self._name = name
        self._id = random.random()
        self._params = copy.deepcopy(params)
        self._outRddCache = None
        self._inRddCache = None
        dprint('module.init', self._name, 'id', self._id, 'params', self._params)

    def setMeta(self, meta):
        dprint('meta.sort', self._name, meta._sort)
        self._meta = meta
        return self._meta

    # virtual method
    def valid(self, meta):
        return self.setMeta(meta)

    # virtual method
    def calc(self, rdd):
        print('ERROR')
        
    def onParamsChanged(self):
        self._outRddCache = None
        
    def save(self):  
        return {'uName' : self._uName, 'params' : self._params.save()}
                
    def load(self, io):
        assert (io['uName'] == self._uName)        
        self._params.load(io['params'])


class InputModule (BaseModule):

    def __init__(self, appInstance, uName, name="Parallel Read", params=Params([
                 Param(str, 'filename', 'poststack.sgy'),
                 Param('dropdown', 'key', 'cdp', {
                       'possible_values': g_traceHeaderList}),
                 Param(int, 'v1', None),
                 Param(int, 'v2', None)])):

        # TODO init doesnt work
        #        super(InputModule, self).__init__()

        self.init(appInstance, uName, name, params)

    def valid(self, meta):
        key = self._params.get('key')
        return self.setMeta(MetaRDD(key))
        # return super(InputModule, self).valid(meta)

    def calc(self, rdd):
        filename = self._params.get('filename')
        rdd = seisspark.loadData(s_sc, filename)
        #output is flat

        key = self._params.get('key')
        v1 = self._params.get('v1')
        v2 = self._params.get('v2')
        if v1 != None and v2 != None:
            rdd = seisspark.RDD_FilterByHeader(key, int(v1), int(v2)).do(rdd)

#        # TODO optimization: make Filter and Group as one operation - they have
#        # same ke
#        rdd = seisspark.RDD_GroupByHeader(key).do(rdd)
        return rdd


class FilterModule (BaseModule):

    def __init__(self, appInstance, uName,  name="Select Gather",
                 params=Params([
                     Param('dropdown', 'key', 'cdp', {
                           'possible_values': g_traceHeaderList}),
                     Param(int, 'v1', 3000),
                     Param(int, 'v2', 3200)])):
        # TODO init doesnt work
        #        super(InputModule, self).__init__()

        self.init(appInstance, uName, name, params)

    def calc(self, rdd):
        key = self._params.get('key')
        v1 = int(self._params.get('v1'))
        v2 = int(self._params.get('v2'))
        rdd = seisspark.RDD_FilterByHeader(key, v1, v2).do(rdd)
        # output is flat

#        # move back to previous sorting
#        rdd = seisspark.RDD_GroupByHeader(self._meta._sort).do(rdd)
        return rdd


class DisplayModule (BaseModule):

    def __init__(self, appInstance, uName,  name="Display Traces"):
        # TODO init doesnt work
        #        super(InputModule, self).__init__()

        self.init(appInstance, uName, name)
        self._mplw = None
        if self._appInstance != None:
            self._mplw = appInstance.createPlot(self._name + ' Plot')

    def remove(self):
        self._appInstance.removePlot(self._mplw)

    def calc(self, rdd):
		# create gathers
        rdd = seisspark.RDD_GroupByHeader(self._meta._sort).do(rdd)

        data, header = seisspark.prepareRDDtoDraw(rdd, 1000) # no more that 1000 traces
        if self._appInstance != None:
            self._mplw.setData(data, header)
#            self._appInstance.setData(self._mplw, stackData.data, header)
        return rdd


class OutputModule (BaseModule):

    def __init__(self, appInstance, uName,  name="Parallel Write", params=Params([
                 Param(str, 'filename', 'out.sgy')])):
        # TODO init doesnt work
        #        super(InputModule, self).__init__()

        self.init(appInstance, uName, name, params)

    def calc(self, rdd):
        import subprocess

        filename = self._params.get('filename')

        # remove file
        subprocess.call(["hdfs", "dfs", "-rm", "-r", filename])

        # input may be flat or gather
        seisspark.saveData(rdd, filename)
        return rdd


class SortModule (BaseModule):

    def __init__(self, appInstance, uName,  name="Parallel Sort",
                 params=Params([
                     Param('dropdown', 'key', 'cdp', {
                           'possible_values': g_traceHeaderList}),
                 ])):
        # TODO init doesnt work
        #        super(InputModule, self).__init__()

        self.init(appInstance, uName, name, params)

    def valid(self, meta):
        key = self._params.get('key')
        return self.setMeta(MetaRDD(key))
        # return super(InputModule, self).valid(meta)

    def calc(self, rdd):
        key = self._params.get('key')
        rdd = seisspark.RDD_GroupByHeader(key).do(rdd)
        # output is gather
        return rdd


class suBPModule (BaseModule):

    def __init__(self, appInstance, uName,  name="BandPass",
                 params=Params([
                     Param(int, 'f1', 10),
                     Param(int, 'f2', 20),
                     Param(int, 'f3', 40),
                     Param(int, 'f4', 50)
                 ])):
        # TODO init doesnt work
        #        super(InputModule, self).__init__()

        self.init(appInstance, uName, name, params)

    def calc(self, rdd):
		# create gathers
        rdd = seisspark.RDD_GroupByHeader(self._meta._sort).do(rdd)

        command = seisspark_config.su_bin + 'sufilter'
        args = "f=" + self._params.get('f1') + ',' + self._params.get(
            'f2') + ',' + self._params.get('f3') + ',' + self._params.get('f4')
        rdd = seisspark.RDD_Processing([command, args]).do(rdd)
        # output is flat

        # move back to previous sorting
        rdd = seisspark.RDD_GroupByHeader(self._meta._sort).do(rdd)
        return rdd

        
class suModule (BaseModule):
    def suInit (self, appInstance, uName, name, command, params=Params([])):
        self._command = command
        self.init(appInstance, uName, name, params)
        
    def calc(self, rdd):
		# create gathers
        rdd = seisspark.RDD_GroupByHeader(self._meta._sort).do(rdd)

        command = [seisspark_config.su_bin + self._command]
        command += self._params.asString()
        rdd = seisspark.RDD_Processing(command).do(rdd)
        # output is flat

        # move back to previous sorting
        rdd = seisspark.RDD_GroupByHeader(self._meta._sort).do(rdd)
        return rdd
    
class suAGCModule (suModule):

    def __init__(self, appInstance, uName, name="AGC",
                 params=Params([
                     Param(int, 'tpow', 2),
                     Param(bool, 'agc', 1),
                     Param(bool, 'gagc', 0),
                     Param(int, 'wagc', 0.5),
                     Param(int, 'pclip', 0.9)
                 ])):
        # TODO init doesnt work
        #        super(InputModule, self).__init__()

        self.suInit(appInstance, uName, name, 'sugain', params)

class suAttributeModule (suModule):

    def __init__(self, appInstance, uName, name="Attributes",
                 params=Params([
                     Param('dropdown', 'mode', 'amp', add = {'possible_values': ['amp',
                                                                                 'phase',
                                                                                 'freq',
                                                                                 'bandwith',
                                                                                 'normamp', 
                                                                                 'fdenv',
                                                                                 'sdenv',
                                                                                 'q' 
                                                                                 ]}),
                 ])):
        # TODO init doesnt work
        #        super(InputModule, self).__init__()

        self.suInit(appInstance, uName, name, 'suattributes', params)







class ModulesFactory ():

    def __init__(self):
        self.__modules = {
            'Input': InputModule,
            'SelectGather': FilterModule,
            'Display': DisplayModule,
            'sufilter': suBPModule,
            'sugain': suAGCModule,
            'Output': OutputModule,
            'Sort': SortModule,
            'suattribute': suAttributeModule,
        }

    def getModileList(self):
        return self.__modules.keys()

    def getModileNames(self):
        # TODO it's not correct
        out = []
        for k in self.__modules.keys():
            m = self.createModule(k, None)
            out.append(m._name)
        
        return out
        
    def createModule(self, uName, appInstance):
        return self.__modules[uName](appInstance, uName)
