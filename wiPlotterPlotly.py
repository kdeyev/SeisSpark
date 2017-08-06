# -*- coding: utf-8 -*-
"""
Created on Sun Aug  6 08:54:35 2017

@author: kostyad
"""

import remi.gui as gui
import json

class wiPlotter(gui.Widget):
    def __init__(self, appInstance, name, **kwargs):
        
        self._name = name
        self._appInstance = appInstance
        self._id = str(id (self))
        super(wiPlotter, self).__init__(id=self._id, **kwargs)
        
        self._data = []
 
        javascript_code = gui.Tag()
        javascript_code.type = 'script'
        javascript_code.attributes['type'] = 'text/javascript'
		
        code = """
            var PLOT = document.getElementById('%(id)s');
            var zmax = 20000;
            var config = {
    			modeBarButtonsToRemove : ["sendDataToCloud", ],
    			displaylogo: false,
    			displayModeBar: true,
    			//scrollZoom: true,
    			//editable: true,
    		};

          var layout = {
    				title: 'very first version of Wiggle',
				xaxis: {title: 'CMP'},
    			  yaxis: {title: 'Time', autorange: 'reversed',},
    			  showlegend: false,
    			};
    
    		Plotly.newPlot(PLOT, [], layout, config);
      
              var drawWiggle = function (PLOT, twoDArray) {
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
    					ampl[i] = trace + twoDArray[trace][i]/zmax*step*gain;
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
    				title: 'very first version of Wiggle',
    				xaxis: {title: 'CMP'},
    			  yaxis: {title: 'Time', autorange: 'reversed',},
    			  showlegend: false,
    			};
    
    			Plotly.newPlot(PLOT, data, layout, config);
               };
               
               var drawMatrix = function (PLOT, twoDArray) {
                   	var stack = 
			  {
				z: twoDArray,
				type: 'heatmap',
				transpose : true,
				zsmooth : 'best',
				zauto : false,
				zmin : -zmax,
				zmax : zmax,
				colorscale : [[0, 'rgb(0,0,255)'], [0.5, 'rgb(255,255,255)'], [1, 'rgb(255,0,0)']],
				//colorbar : {symmetric: true,}
			};
   
    			var layout = {
    				title: 'very first version of Wiggle',
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
    		function(error, twoDArray) {
    			drawMatrix (PLOT, twoDArray );
    		});
            };
            """% {'id': self._id}
		
        javascript_code.add_child('code',   # Add to Tag
                                  code % {'id': id(self), })
        self.add_child('javascript_code', javascript_code)   # Add to widget

    def get_refresh(self):
        if self._data is None:
            return None, None

        txt = json.dumps(self._data)
        headers = {'Content-type': 'text/plain'}
        return [txt, headers]


    def redraw (self):
        cmd = """
            updateData('%(id)s');
        """%{'id' : self._id}
        self._appInstance.execute_javascript(cmd)
        
    def onParamsChanged(self):
        pass

    def setData(self, data, header):
        self._data = data
        self.redraw ()

        
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
        mplw = wiPlotter(self._appInstance, name)
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
#        self.paramsWidget.setParams(None)
        self._selectedPlot = None

    def selectPlot(self, plot):
        self.deselectPlot()

        self._selectedPlot = plot
        if self._selectedPlot != None:
#            self.paramsWidget.setParams(self._selectedPlot._params)
#            self.paramsWidget.set_on_attribute_change_listener(self.onattribute_changed)

            self.__set_box_shadow_selected_widget(self._selectedPlot)

    def onattribute_changed(self, widget, widgetAttributeMember, attributeName, newValue):
        self._selectedPlot.onParamsChanged()

    @staticmethod
    def __remove_box_shadow_selected_widget(plot):
        if plot == None:
            return
        if 'box-shadow' in plot.style.keys():
            del plot.style['box-shadow']

    @staticmethod
    def __set_box_shadow_selected_widget(plot):
        if plot == None:
            return
#        plot.style['box-shadow'] = '0 0 10px rgb(33,150,243)'
