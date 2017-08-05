"""
    Author: https://github.com/saewoonam
"""

import remi.gui as gui
from remi import start, App
import json

import stackData



class PlotlyWidget(gui.Widget):
    def __init__(self, name, 
                 **kwargs):
        super(PlotlyWidget, self).__init__(id=name, **kwargs)
        
        self.name = name
        self.data = stackData.data
 
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
            """% {'id': self.name}
		
        javascript_code.add_child('code',   # Add to Tag
                                  code % {'id': id(self), })
        self.add_child('javascript_code', javascript_code)   # Add to widget

    def get_refresh(self):
        if self.data is None:
            return None, None

        txt = json.dumps(self.data)
        headers = {'Content-type': 'text/plain'}
        return [txt, headers]

class MyApp(App):
    def __init__(self, *args):
        html_head = '<script src="https://cdn.plot.ly/plotly-latest.min.js">'
        html_head += '</script>'
        self.data = stackData.data
        super(MyApp, self).__init__(*args, html_head=html_head)

    def main(self):
        wid = gui.HBox()
        wid.style['position'] = 'absolute'
        ctrl = gui.VBox(width=400)
        ctrl.style['justify-content'] = 'space-around'

        plotContainer = gui.Widget()

        self.plt1 = PlotlyWidget('plot1')
        plotContainer.append(self.plt1)

        self.plt2 = PlotlyWidget('plot2')
        plotContainer.append(self.plt2)
        
        bt1 = gui.Button('Start', width=200, height=30)
        bt1.style['margin'] = 'auto 50px'
        bt1.style['background-color'] = 'green'

        # setting the listener for the onclick event of the button
        bt1.set_on_click_listener(self.on_button_pressed1)
        ctrl.append(bt1)
        
        bt2 = gui.Button('Start', width=200, height=30)
        bt2.style['margin'] = 'auto 50px'
        bt2.style['background-color'] = 'green'

        # setting the listener for the onclick event of the button
        bt2.set_on_click_listener(self.on_button_pressed2)
        ctrl.append(bt2)

        # returning the root widget
        wid.append(ctrl)
        wid.append(plotContainer)

        return wid

    # listener function
    def on_button_pressed1(self, widget):        
        cmd = """
            updateData('%(id)s');
        """%{'id' : self.plt1.name}
        print(cmd)
        self.execute_javascript(cmd)
        
    def on_button_pressed2(self, widget):        
        cmd = """
            updateData('%(id)s');
        """%{'id' : self.plt2.name}
        print(cmd)
        self.execute_javascript(cmd)

if __name__ == "__main__":
    # starts the webserver
    # start(MyApp,address='127.0.0.1', port=8081, multiple_instance=False,
    #        enable_file_cache=True, update_interval=0.1, start_browser=True)
    start(MyApp, debug=False, port=8081, address='0.0.0.0', start_browser=True)
