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
Created on Wed Nov 16 20:32:47 2016

@author: kdeyev
"""

# possible types:
# bool or 'bool':
# int or float or 'int' or 'float': additionalInfo['min'], additionalInfo['max'], additionalInfo['step']
# gui.ColorPicker:
# 'dropdown': additionalInfo['possible_values']:
# 'url_editor':
# 'css_size':
# default is string

from seisspark_config import dprint

class Param ():

    def __init__(self, t, k, v, add=None, group = "General"):
        self._k = k
        self._v = v
        self._defaultValue = v
        self._description = "None"
        self._group = group
        self._type = t
        self._additionalInfo = add
        
    def save(self):
        return {'name' : self._k, 'value' : self._v}

    def load(self, io):      
        assert (io['name'] == self._k)  
        self._v = io['value']

    def asString(self):
        return self._k + '=' + str(self._v)

class Params ():

    def __init__(self, par=[]):
        self._par = par

    def add(self, k, v):
        self._par.append(Param(k, v))

    def get(self, k):
        for p in self._par:
            if p._k == k:
                return p._v
        return None

    def put(self, k, v):
        for p in self._par:
            if p._k == k:
                dprint('Params::put', p._k, v)
                p._v = v

    def printValues(self):
        for p in self._par:
            print(p._k, p._v)
            
    def save(self):
        save_params = []
        for p in self._par:
            save_param = p.save()
            save_params.append(save_param)
    
        return save_params

    def load(self, io):      
        for save_param in io:
            name = save_param['name']
            self.__find(name).load(save_param)

    def __find(self, k):
        for p in self._par:
            if p._k == k:
                return p
        return None        
        
    def asString(self):
        ret_str = []
        for p in self._par:
            ret_str.append(p.asString())
        
        return ret_str