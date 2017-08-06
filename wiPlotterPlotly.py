# -*- coding: utf-8 -*-
"""
Created on Sun Aug  6 08:54:35 2017

@author: kostyad
"""

import remi.gui as gui
import json
import numpy
import enParam

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

                 
class wiPlotter(gui.Widget):
    def __init__(self, appInstance, name, **kwargs):
        
        self._params = enParam.Params([
                                       enParam.Param(bool, 'density', True),
                                       enParam.Param(bool, 'wiggle', False),
                                       enParam.Param(float, 'percent', 0.9, add = {'min': 0, 'max': 1}),
                                       enParam.Param(float, 'gain', 1),
                                       enParam.Param('dropdown', 'palette', 'Greys', group = 'density', add = {'possible_values': palette_names}),
                                       enParam.Param(int, 'skipt', 1, group = 'wiggle', add = {'min': 1}),
                                       enParam.Param(float, 'lwidth', 0.1, group = 'wiggle'),
                                       ])
                
        self._name = name
        self._appInstance = appInstance
        self._id = str(id (self))
        super(wiPlotter, self).__init__(id=self._id, **kwargs)
        
        self._data = numpy.zeros ((1,1))
 
        javascript_code = gui.Tag()
        javascript_code.type = 'script'
        javascript_code.attributes['type'] = 'text/javascript'
		
        code = """
            var PLOT = document.getElementById('%(id)s');
            var config = {
    			modeBarButtonsToRemove : ["sendDataToCloud", ],
    			displaylogo: false,
    			displayModeBar: true,
    			//scrollZoom: true,
    			//editable: true,
    		};

          var layout = {
    				title: 'run calculation',
				xaxis: {title: 'CMP'},
    			  yaxis: {title: 'Time', autorange: 'reversed',},
    			  showlegend: false,
    			};
      
              var drawWiggle = function (PLOT, name, twoDArray, max_val) {
                    var data = [];
    			
    			var step = 1;
    			var gain = 1;
    			for (var trace=0;trace<twoDArray.length;trace+=step) {
    				var x = new Array (twoDArray[trace].length);
    				var y = new Array (twoDArray[trace].length);
    				var ampl = new Array (twoDArray[trace].length);
    				var fill_ampl = new Array (twoDArray[trace].length);
    				
    				
    				for (var i=0;i<twoDArray[trace].length;i++) {
    					x[i] = trace;
    					y[i] = i;
    					ampl[i] = trace + twoDArray[trace][i]/max_val*step*gain;
    					if (twoDArray[trace][i] > 0) {
    						fill_ampl[i] = ampl[i]
    					} else {
    						fill_ampl[i] = trace;
    					}
    					
    				}
    				
    				var zero_line = {
    				  x: x,
    				  y: y,
    				  type: 'scatter',
    				  line: {color: 'black',
    						width: 0,
    						},
    				};
    
    				var fill = {
    				  x: fill_ampl,
    				  y: y,
    				  type: 'scatter',
    				  fill: 'tonextx',
    				  line: {color: 'black',
    						width: 0,
    						//shape: 'spline',
    						},
    				};
    
    				var wiggle = {
    				  x: ampl,
    				  y: y,
    				  type: 'scatter',
    				  line: {color: 'black',
    						width: 1,
    						//shape: 'spline',
    						},
    				};
    
    				data.push(zero_line);
    				data.push(fill);
    				data.push(wiggle);
    			}
    			var layout = {
    				title: name,
    				xaxis: {title: 'CMP'},
    			  yaxis: {title: 'Time', autorange: 'reversed',},
    			  showlegend: false,
    			};
    
    			Plotly.newPlot(PLOT, data, layout, config);
               };
               
               var drawMatrix = function (PLOT, name, twoDArray, max_val) {
                   	var stack = 
			  {
				z: twoDArray,
				type: 'heatmap',
				transpose : true,
				zsmooth : 'best',
				zauto : false,
				zmin : -max_val,
				zmax : max_val,
				colorscale : [[0, 'rgb(0,0,255)'], [0.5, 'rgb(255,255,255)'], [1, 'rgb(255,0,0)']],
				//colorbar : {symmetric: true,}
			};
   
    			var layout = {
    				title: name,
    				xaxis: {title: 'CMP'},
    			  yaxis: {title: 'Time', autorange: 'reversed',},
    			  showlegend: false,
    			};
    
    			Plotly.newPlot(PLOT, [stack], layout, config);
               };
               
               
      
          var updateData = function (id) {  
    		var PLOT = document.getElementById(id);
    		var url = id + "/get_refresh";
    		Plotly.d3.json(url,
    		function(error, data) {
                 d = data.d
                 name = data.n
                 max_val = data.m
    			drawMatrix (PLOT, name, d, max_val);
    		});
            };
            
            updateData ('%(id)s');
            """% {'id': self._id}
		
        javascript_code.add_child('code',   # Add to Tag
                                  code % {'id': id(self), })
        self.add_child('javascript_code', javascript_code)   # Add to widget

    def get_refresh(self):
        if self._data is None:
            return None, None

        max_val = 0
        for x in numpy.nditer(self._data):
            max_val = max (max_val, abs (x))
            
        max_val= max_val/10.
#        print ('redraw', max_val)
        tosend = {'d': self._data.transpose().tolist(),
                  'n': self._name,
                  'm': max_val}

        txt = json.dumps(tosend)
        headers = {'Content-type': 'text/plain'}
        return [txt, headers]


    def redraw (self):
        
        cmd = """
            updateData('%(id)s');
        """%{'id' : self._id}

#        print ('redraw', cmd)
        self._appInstance.execute_javascript(cmd)
        
    def onParamsChanged(self):
        pass

    def setData(self, data, header):
        self._data = data
        self.redraw ()
