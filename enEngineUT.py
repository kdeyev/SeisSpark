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

import enEngine

def runTest(filename):
    engine = enEngine.Engine(True)
    engine.loadFromFile (filename)
    engine.calc()

if __name__ == "__main__":
    runTest ("jobs/UT.job")
   
