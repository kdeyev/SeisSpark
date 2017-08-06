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
Created on Fri Dec  2 07:04:11 2016

@author: kdeyev
"""
import os


debug = False
handle_exceptions = not debug
local_spark = debug
local_remi = debug

def dprint (*kwargs):
    if debug:
        print (kwargs)
        
if debug:
	su_bin = '/home/cloudera/cwp/bin/'
else:
	su_bin = '/usr/local/bin/'

plot_w = 600
plot_h = 600
image_w = 20
image_h = 20
plot_label_size = 10
axis_label = True

external_ip = '35.195.79.128'
websocket_port=8082
if local_remi:
    remi = dict(debug=False, address='0.0.0.0', port=8081)
else:
    remi = dict(debug=False, address='0.0.0.0', port=8081, websocket_port=websocket_port,
                host_name=external_ip, username='1', password='1')
