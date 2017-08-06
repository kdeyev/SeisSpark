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
Created on Mon Nov 14 13:35:29 2016

@author: kdeyev
"""
import remi.gui as gui

#import seisspark
from seisspark_config import dprint

#import wiPlotterMatPlot
import wiPlotterPlotly

class PlotsWidget (gui.HBox):

    def __init__(self, appInstance, **kwargs):
        super(PlotsWidget, self).__init__(**kwargs)

        self.paramsWidget = None
        self._selectedPlot = None
        self.style['position'] = 'relative'
        self.style['overflow'] = 'auto'
        self.style['background-color'] = 'rgb(250,248,240)'
        self.style['background-image'] = "url('/res/background.png')"
        self.style['justify-content'] = 'space-between'

        self._appInstance = appInstance
        

    def createPlot(self, name):
#        mplw = wiPlotterMatPlot.wiPlotter(name)
        mplw = wiPlotterPlotly.wiPlotter(self._appInstance, name)
#        mplw.attributes['editor_constructor'] = constructor
#        mplw.attributes['editor_varname'] = variableName
#        mplw.attributes['editor_tag_type'] = 'widget'
#        mplw.attributes['editor_newclass'] = 'False'# if self.dialog.get_field("editor_newclass").get_value() else 'False'
#        mplw.attributes['editor_baseclass'] = mplw.__class__.__name__ #__class__.__bases__[0].__name__
#        "this.style.cursor='default';this.style['left']=(event.screenX) + 'px'; this.style['top']=(event.screenY) + 'px'; event.preventDefault();return true;"
# if not 'position' in mplw.style:
##            mplw.style['position'] = 'absolute'
#        if not 'display' in mplw.style:
#            mplw.style['display'] = 'block'

        self.append(mplw)
        mplw.set_on_mousedown_listener(self.onPlotMouseDown)
        return mplw

    def removePlot(self, mpwl):
        if mpwl == self._selectedPlot:
            self.deselectPlot()
        self.remove_child(mpwl)

    def setParamWidget(self, paramsWidget):
        self.paramsWidget = paramsWidget

    def onPlotMouseDown(self, widget, x, y):
        self.selectPlot(widget)

    def deselectPlot(self):
        self.__remove_box_shadow_selected_widget(self._selectedPlot)
        self.paramsWidget.setParams(None)
        self._selectedPlot = None

    def selectPlot(self, plot):
        self.deselectPlot()

        self._selectedPlot = plot
        if self._selectedPlot != None:
            self.paramsWidget.setParams(self._selectedPlot._params)
            self.paramsWidget.set_on_attribute_change_listener(
                self.onattribute_changed)

            self.__set_box_shadow_selected_widget(self._selectedPlot)

    def onattribute_changed(self, widget, widgetAttributeMember, attributeName, newValue):
        self._selectedPlot.onParamsChanged()

    @staticmethod
    def __remove_box_shadow_selected_widget(plot):
        if plot == None:
            return
#        if 'box-shadow' in plot.style.keys():
#            del plot.style['box-shadow']

    @staticmethod
    def __set_box_shadow_selected_widget(plot):
        if plot == None:
            return
#        plot.style['box-shadow'] = '0 0 10px rgb(33,150,243)'
