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
Created on Wed Nov 16 20:49:12 2016

@author: kdeyev
"""

import remi.gui as gui


class ToolBar(gui.Widget):

    def __init__(self, **kwargs):
        super(ToolBar, self).__init__(**kwargs)
        self.set_layout_orientation(gui.Widget.LAYOUT_HORIZONTAL)
        self.style['background-color'] = 'white'

    def add_command(self, imagePath, callback, title):
        icon = gui.Image(imagePath, height='90%', margin='0px 1px')
        icon.style['outline'] = '1px solid lightgray'
        icon.set_on_click_listener(callback)
        icon.attributes['title'] = title
        self.append(icon)
