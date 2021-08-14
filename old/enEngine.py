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
Created on Wed Nov 16 20:45:40 2016

@author: kdeyev
"""

import sys
import seisspark_config
from seisspark_config import dprint

class Engine():

    def __init__(self, stopOnError):
        self._modules = []
        self._stopOnError = stopOnError

    def addModule(self, module, afterMod = None):
        if afterMod != None:
            index = self._modules.index(afterMod)
            self._modules.insert(index  + 1, module)
        else:
            self._modules.append(module)

    def removeModule(self, module):
        if module == None:
            return
        self._modules.remove(module)
        module.remove()

    def upModule(self, module):
        old_index = self._modules.index(module)
        new_index = old_index - 1
        self._modules.insert(new_index, self._modules.pop(old_index))

    def downModule(self, module):
        old_index = self._modules.index(module)
        new_index = old_index + 1
        self._modules.insert(new_index, self._modules.pop(old_index))

    def valid(self):
        error = None
        meta = None
        if seisspark_config.handle_exceptions:
            for m in self._modules:
                dprint("valid", m._name)
                try:
                    meta = m.valid(meta)
                except:
                    error = "Validation of module", m._name, "\nUnexpected error:" + \
                        str(sys.exc_info()[0])
                    print(error)
                    if self._stopOnError:
                        raise
                dprint("valid", m._name, 'key', meta._sort)
        else:
            for m in self._modules:
                dprint("valid", m._name)
                meta = m.valid(meta)
                dprint("valid", m._name, 'key', meta._sort)
        return error
        
    def calcCached(self, m, rdd):
        if rdd is not m._inRddCache: # input was changed
            m._outRddCache = None # drop output
        if m._outRddCache != None:
            dprint ("module", m._name, "used cache")
            return m._outRddCache # return out 
            
        dprint ("module", m._name, "didnt used cache")
        m._inRddCache = rdd
        m._outRddCache = m.calc(rdd)
        return m._outRddCache
        

    def calc(self):
        rdd = None
        error = self.valid()
        if seisspark_config.handle_exceptions:
            for m in self._modules:
                try:
                    rdd = self.calcCached(m, rdd)
                except:
                    error = "Execution of module", m._name, "\nUnexpected error:" + \
                        str(sys.exc_info()[0])
                    print(error)
                    if self._stopOnError:
                        raise
        else:
            for m in self._modules:
                rdd = self.calcCached(m, rdd)

        return error

        
    def save(self):
        save_modules = []
        for m in self._modules:
            save_modules.append(m.save ())
            
        return {'modules' : save_modules}

    def load(self, io, appInstance = None):
        import enModules
        moduleFactory = enModules.ModulesFactory()
        
        save_modules = io['modules']
        for save_module in save_modules:
            name = save_module['uName']
            m = moduleFactory.createModule(name, appInstance)
            m.load(save_module)
            self.addModule(m)
            
    def loadFromFile(self, filename, appInstance = None):        
        import json
        with open(filename, 'r') as f:
            s = f.read()
            io = json.loads(s)
            self.load(io, appInstance)
            
    def saveToFile(self, filename): 
        import json
        with open(filename, 'w') as f:
            f.write(json.dumps(self.save(), indent=4, separators=(',', ': ')))
