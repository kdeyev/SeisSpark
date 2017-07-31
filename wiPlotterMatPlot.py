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
import seisspark
import seisspark_config
from seisspark_config import dprint

import io
import time
import threading
import enParam

import remi.gui as gui

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg

import numpy as np

import matplotlib
import mpld3
matplotlib.rcParams.update({'font.size': 10})

palette_names = ['viridis', 'inferno', 'plasma', 'magma',
                 'Blues', 'BuGn', 'BuPu',
                 'GnBu', 'Greens', 'Greys', 'Oranges', 'OrRd',
                 'PuBu', 'PuBuGn', 'PuRd', 'Purples', 'RdPu',
                 'Reds', 'YlGn', 'YlGnBu', 'YlOrBr', 'YlOrRd',
                 'afmhot', 'autumn', 'bone', 'cool',
                 'copper', 'gist_heat', 'gray', 'hot',
                 'pink', 'spring', 'summer', 'winter',
                 'BrBG', 'bwr', 'coolwarm', 'PiYG', 'PRGn', 'PuOr',
                 'RdBu', 'RdGy', 'RdYlBu', 'RdYlGn', 'Spectral',
                 'seismic',
                 'Accent', 'Dark2', 'Paired', 'Pastel1',
                 'Pastel2', 'Set1', 'Set2', 'Set3',
                 'gist_earth', 'terrain', 'ocean', 'gist_stern',
                 'brg', 'CMRmap', 'cubehelix',
                 'gnuplot', 'gnuplot2', 'gist_ncar',
                 'nipy_spectral', 'jet', 'rainbow',
                 'gist_rainbow', 'hsv', 'flag', 'prism']


class MatplotImage(gui.Widget):
    ax = None

    def __init__(self, **kwargs):
        super(MatplotImage, self).__init__( **kwargs)

        self._params = enParam.Params([
                                       enParam.Param(bool, 'density', False),
                                       enParam.Param(bool, 'wiggle', True),
                                       enParam.Param(float, 'percent', 0.9, add = {'min': 0, 'max': 1}),
                                       enParam.Param(float, 'gain', 1),
                                       enParam.Param('dropdown', 'palette', 'Greys', group = 'density', add = {'possible_values': palette_names}),
                                       enParam.Param(int, 'skipt', 1, group = 'wiggle', add = {'min': 1}),
                                       enParam.Param(float, 'lwidth', 0.1, group = 'wiggle'),
                                       ])
        self._buf = None
        self._buflock = threading.Lock()

        self._data = None
        self._header = None

#        self._fig = Figure(figsize=(40, 30))
        self.__createFigure()
        
#        self._fig.gca().invert_yaxis()
        
        self.redraw()
        
    def repr(self, client, changed_widgets={}):
        return mpld3.fig_to_html(self._fig)

#    def redraw(self):
##        fig, ax = plt.subplots()
#
##        x = np.linspace(-2, 2, 20)
##        y = x[:, None]
##        X = np.zeros((20, 20, 4))
##        
##        X[:, :, 0] = np.exp(- (x - 1) ** 2 - (y) ** 2)
##        X[:, :, 1] = np.exp(- (x + 0.71) ** 2 - (y - 0.71) ** 2)
##        X[:, :, 2] = np.exp(- (x + 0.71) ** 2 - (y + 0.71) ** 2)
##        X[:, :, 3] = np.exp(-0.25 * (x ** 2 + y ** 2))
##        
##        im = self._ax.imshow(X, extent=(10, 20, 10, 20),
##                       origin='lower', zorder=1, interpolation='nearest')
##        self._fig.colorbar(im, ax=self._ax)
##        
##        self._ax.set_title('An Image', size=20)
##        
#        from mpld3 import plugins
#        plugins.connect(self._fig, plugins.MousePosition(fontsize=14))
#        pass
    
    def setData(self, data, header):
        self._data = data
        self._header = header
        
        self._ntraces = data.shape[1]
        self._t_start = 0
            
        first_trace = self._header[0]
        self._dt = seisspark.KV_HeaderAccess('dt').getHeaderV(first_trace)
        self._ns = seisspark.KV_HeaderAccess('ns').getHeaderV(first_trace)
        
        self.updateNorm__()

        dprint ("ntraces", self._ntraces)  
        dprint ("t_start", self._t_start)  
        dprint ("dt", self._dt)  
        dprint ("ns", self._ns)  
            
#        dprint ('Data type', type(self._data), 'shape', self._data.shape)
#        dprint ('Header type', type(self._header), 'len', len(self._header))
        self.__redraw()

    def onParamsChanged(self):
        if seisspark_config.debug:
            print ("seisspark_config")  
            self._params.printValues() 

        self.updateNorm__()
        self.__redraw()
        
    def updateNorm__(self):
        array = self._data.reshape (self._ntraces*self._ns)
        array = np.absolute(array)
        array.sort(axis=0)
        percent=float(self._params.get("percent"))
        dprint ('percent', percent)
        
        norm = int((len(array)-1)*percent)
        dprint('len', norm)
        self._norm_amp = array[norm]
        dprint('array', array)
        dprint ('_norm_amp', self._norm_amp)
        
    def __wiggle(self):
            dprint ("__wiggle")  
            
            skipt= int(self._params.get("skipt"))
            maxval=float(self._params.get("gain"))
            maxval = self._norm_amp/maxval
            lwidth=float(self._params.get("lwidth"))
                
            import numpy
            import copy
            data = numpy.transpose(self._data)          
            data = copy.copy(data)
            
            t = [self._t_start + i for i in range(self._ns)]

            for i in range(0,self._ntraces, skipt):
                    trace=data[i]
                    trace[0]=0
                    trace[self._ns-1]=0        

                    for a in range(len(trace)):
                            if (trace[a]>maxval):
                                    trace[a]=maxval
                            if (trace[a]< -maxval):
                                    trace[a]=-maxval

                    self._ax.plot(i+trace/maxval,t,color='black',linewidth=lwidth)
                    for a in range(len(trace)):
                            if (trace[a]<0):
                                    trace[a]=0

                    self._ax.fill(i+trace/maxval,t,'k',linewidth=0)

    def __dense(self):  
        dprint ("__dense")  
            
        maxval = float(self._params.get("gain"))
        maxval = self._norm_amp/maxval
            
        palette = self._params.get("palette")
        self._ax.imshow(self._data, palette, aspect='auto', vmin = -maxval, vmax = maxval)       

    def __createFigure (self):
        self._fig = Figure(figsize=(seisspark_config.image_w, seisspark_config.image_h))
        self._ax = self._fig.add_subplot(111)
        self._fig.gca().invert_yaxis()
        self._ax.tick_params(axis='both', which='major', labelsize=seisspark_config.plot_label_size)
        self._ax.tick_params(axis='both', which='minor', labelsize=seisspark_config.plot_label_size)
        if seisspark_config.axis_label:
            self._ax.set_ylabel('Time')
            self._ax.set_xlabel('Trace')        
        
    def __redraw(self):
        if seisspark_config.debug:
            print ("__redraw")  
            self._params.printValues() 

        del self._fig
        self.__createFigure()
        
        x = np.linspace(-2, 2, 20)
        y = x[:, None]
        X = np.zeros((20, 20, 4))
        
        X[:, :, 0] = np.exp(- (x - 1) ** 2 - (y) ** 2)
        X[:, :, 1] = np.exp(- (x + 0.71) ** 2 - (y - 0.71) ** 2)
        X[:, :, 2] = np.exp(- (x + 0.71) ** 2 - (y + 0.71) ** 2)
        X[:, :, 3] = np.exp(-0.25 * (x ** 2 + y ** 2))
        
        im = self._ax.imshow(X, extent=(10, 20, 10, 20),
                       origin='lower', zorder=1, interpolation='nearest')
        self._fig.colorbar(im, ax=self._ax)
        
        self._ax.set_title('An Image', size=20)

        if self._params.get("density"):
            self.__dense ()
        if self._params.get("wiggle"):
            self.__wiggle ()

        self._ax.axis('tight')

#        self._fig.colorbar()


#        slabel_z = [int(v * 1000) for v in range(self._ns)]
#        for i in range(len(label_z)):
#            if i%2 != 0:
#                label_z[i] = ""
#
#        plt.xticks(range(len(label_x)), label_x)
#        self._fig.yticks(range(len(label_z)), label_z)
        self.redraw()
#        dprint ("End __redraw")

    def get_image_data(self, update_index):
        with self._buflock:
            if self._buf is None:
                return None
            self._buf.seek(0)
            data = self._buf.read()

        return [data, {'Content-type': 'image/png'}]


class wiPlotter(gui.VBox):

    def __init__(self, name, **kwargs):
        super(wiPlotter, self).__init__(**kwargs)

        self.style['align-items'] = "flex-start"
        self.style['justify-content'] = "flex-start"
        self.style['margin'] = "10px"

        self._mpl = MatplotImage(width=seisspark_config.plot_w, height=seisspark_config.plot_h)
#        self._mpl.style['margin'] = '10px'
        self._mpl._ax.set_title(name)

        self.append(self._mpl)
        self._params = self._mpl._params

    def onParamsChanged(self):
        #        dprint ('wiPlotter::onParamsChanged')
        self._mpl.onParamsChanged()

    def setData(self, data, header):
        self._mpl.setData(data, header)
