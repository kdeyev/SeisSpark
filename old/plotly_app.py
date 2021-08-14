"""
    Author: https://github.com/saewoonam
"""

import remi.gui as gui
from remi import start, App

import stackData
import plotly_app_plot


class MyApp(App):
    def __init__(self, *args):
        html_head = '<script src="https://cdn.plot.ly/plotly-latest.min.js">'
        html_head += '</script>'
        super(MyApp, self).__init__(*args, html_head=html_head)

    def main(self):
        wid = gui.HBox()
        wid.style['position'] = 'absolute'
        ctrl = gui.VBox(width=400)
        ctrl.style['justify-content'] = 'space-around'

        plotContainer = gui.Widget()

        self._plotsWidget = plotly_app_plot.PlotsWidget(
            self, width='100%', height='100%')
        
        centralContainer = gui.VBox()
        plotContainer.append(centralContainer)
        centralContainer.append(self._plotsWidget)

        self.plt1 = self._plotsWidget.createPlot('1')
#        centralContainer.append(self.plt1)

#        self.plt2 = PlotlyWidget()
        self.plt2 = self._plotsWidget.createPlot('2')
#        centralContainer.append(self.plt2)
        
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
        self.plt1.setData (stackData.data, None)
        
    def on_button_pressed2(self, widget):        
        self.plt2.setData (stackData.data, None)

if __name__ == "__main__":
    # starts the webserver
    # start(MyApp,address='127.0.0.1', port=8081, multiple_instance=False,
    #        enable_file_cache=True, update_interval=0.1, start_browser=True)
    start(MyApp, debug=False, port=8081, address='0.0.0.0', start_browser=True)
