import remi.gui as gui
from remi import start, App
import os  # for path handling

import wiParamsWidget
import wiModuleWidget
import wiPlotWidget

import seisspark_config
from seisspark_config import dprint

class EditorFileSelectionDialog(gui.FileSelectionDialog):
    def __init__(self, title='File dialog', message='Select file', 
                multiple_selection=True, selection_folder='.', allow_file_selection=True, 
                allow_folder_selection=True, baseAppInstance = None):
        super(EditorFileSelectionDialog, self).__init__( title,
                 message, multiple_selection, selection_folder, 
                 allow_file_selection, allow_folder_selection)
        
        self.baseAppInstance = baseAppInstance
        
    def show(self, *args):
        dprint ("EditorFileSelectionDialog.show")
        super(EditorFileSelectionDialog, self).show(self.baseAppInstance)


class EditorFileSaveDialog(gui.FileSelectionDialog):
    def __init__(self, title='File dialog', message='Select file', 
                multiple_selection=True, selection_folder='.', 
                 allow_file_selection=True, allow_folder_selection=True, baseAppInstance = None):
        super(EditorFileSaveDialog, self).__init__( title, message, multiple_selection, selection_folder, 
                 allow_file_selection, allow_folder_selection)
        
        self.baseAppInstance = baseAppInstance
        
    def show(self, *args):
        dprint ("EditorFileSelectionDialog.show")
        super(EditorFileSaveDialog, self).show(self.baseAppInstance)
        
    def add_fileinput_field(self, defaultname='untitled'):
        self.txtFilename = gui.TextInput()
        self.txtFilename.set_on_enter_listener(self.on_enter_key_pressed)
        self.txtFilename.set_text(defaultname)
        
        self.add_field_with_label("filename","Filename",self.txtFilename)
        
    def get_fileinput_value(self):
        return self.get_field('filename').get_value()
    
    def on_enter_key_pressed(self, widget, value):
        self.confirm_value(None)
        
    def confirm_value(self, widget):
        """event called pressing on OK button.
           propagates the string content of the input field
        """
        self.hide()
        params = (self.fileFolderNavigator.pathEditor.get_text(),)
        return self.eventManager.propagate(self.EVENT_ONCONFIRMVALUE, params)

        
class ProjectConfigurationDialog(gui.GenericDialog):
#    KEY_PRJ_NAME = 'config_project_name'
#    KEY_ADDRESS = 'config_address'
#    KEY_PORT = 'config_port'
    KEY_MULTIPLE_INSTANCE = 'config_multiple_instance'
    KEY_ENABLE_CACHE = 'config_enable_file_cache'
    KEY_START_BROWSER = 'config_start_browser'
#    KEY_RESOURCEPATH = 'config_resourcepath'

    def __init__(self, title='', message=''):
        super(ProjectConfigurationDialog, self).__init__('Configuration',
                                                         'Here are the configuration options of the project.', width=500)
#        # standard configuration
#        self.configDict = {}
#
#        self.configDict[self.KEY_PRJ_NAME] = 'untitled'
#        self.configDict[self.KEY_ADDRESS] = '0.0.0.0'
#        self.configDict[self.KEY_PORT] = 8081
#        self.configDict[self.KEY_MULTIPLE_INSTANCE] = True
#        self.configDict[self.KEY_ENABLE_CACHE] = True
#        self.configDict[self.KEY_START_BROWSER] = True
#        self.configDict[self.KEY_RESOURCEPATH] = "./res/"
#
#        self.add_field_with_label(
#            '', 'Project Name', gui.TextInput())
        self.add_field_with_label(
            'external_ip', 'IP address', gui.TextInput())
        self.add_field_with_label(
            'websocket_port', 'Listen port', gui.SpinBox(8082, 1025, 65535))
        self.add_field_with_label(
            'plot_w', 'Window w', gui.SpinBox(600, 100, 65535))
        self.add_field_with_label(
            'plot_h', 'Window h', gui.SpinBox(600, 100, 65535))
        self.add_field_with_label(
            'image_w', 'Image w', gui.SpinBox(20, 1, 100))
        self.add_field_with_label(
            'image_h', 'Image h', gui.SpinBox(20, 1, 100))
        self.add_field_with_label(
            'plot_label_size', 'Plot Label Size', gui.SpinBox(10, 1, 100))
        self.add_field_with_label(
            'axis_label', 'Axis Label', gui.CheckBox(True))
        self.add_field_with_label(
            'su_bin', 'SU Path', gui.TextInput())
        self.add_field_with_label(
            self.KEY_MULTIPLE_INSTANCE, 'Use single App instance for multiple users', gui.CheckBox(True))
        self.add_field_with_label(
            self.KEY_ENABLE_CACHE, 'Enable file caching', gui.CheckBox(True))
        self.add_field_with_label(
            self.KEY_START_BROWSER, 'Start browser automatically', gui.CheckBox(True))
#        self.add_field_with_label(
#            self.KEY_RESOURCEPATH, 'Additional resource path', gui.TextInput())
        self.from_dict_to_fields()

    def from_dict_to_fields(self):
        self.get_field('external_ip').set_value(seisspark_config.external_ip)
        self.get_field('websocket_port').set_value(seisspark_config.websocket_port)
        self.get_field('plot_w').set_value(seisspark_config.plot_w)
        self.get_field('plot_h').set_value(seisspark_config.plot_h)
        self.get_field('image_w').set_value(seisspark_config.image_w)
        self.get_field('image_h').set_value(seisspark_config.image_h)
        self.get_field('su_bin').set_value(seisspark_config.su_bin)
        self.get_field('plot_label_size').set_value(seisspark_config.plot_label_size)
        self.get_field('axis_label').set_value(seisspark_config.axis_label)
        #        self.get_field('external_ip').set_value(seisspark_config.external_ip)
#        self.get_field('websocket_port').set_value(seisspark_config.websocket_port)
        return
#        for key in self.inputs.keys():
#            if key in dictionary.keys():
#                self.get_field(key).set_value(str(dictionary[key]))

    def from_fields_to_dict(self):
        seisspark_config.external_ip = self.get_field('external_ip').get_value()
        seisspark_config.websocket_port = self.get_field('websocket_port').get_value()
        seisspark_config.plot_w = self.get_field('plot_w').get_value()
        seisspark_config.plot_h = self.get_field('plot_h').get_value()
        seisspark_config.image_w = int(self.get_field('image_w').get_value())
        seisspark_config.image_h = int(self.get_field('image_h').get_value())
        seisspark_config.su_bin = self.get_field('su_bin').get_value()
        seisspark_config.plot_label_size = self.get_field('plot_label_size').get_value()
        seisspark_config.axis_label = self.get_field('axis_label').get_value()
        return 
#        self.configDict[self.KEY_PRJ_NAME] = self.get_field(
#            self.KEY_PRJ_NAME).get_value()
#        self.configDict[self.KEY_ADDRESS] = self.get_field(
#            self.KEY_ADDRESS).get_value()
#        self.configDict[self.KEY_PORT] = int(
#            self.get_field(self.KEY_PORT).get_value())
#        self.configDict[self.KEY_MULTIPLE_INSTANCE] = self.get_field(
#            self.KEY_MULTIPLE_INSTANCE).get_value()
#        self.configDict[self.KEY_ENABLE_CACHE] = self.get_field(
#            self.KEY_ENABLE_CACHE).get_value()
#        self.configDict[self.KEY_START_BROWSER] = self.get_field(
#            self.KEY_START_BROWSER).get_value()
#        self.configDict[self.KEY_RESOURCEPATH] = self.get_field(
#            self.KEY_RESOURCEPATH).get_value()

    def confirm_dialog(self):
        """event called pressing on OK button.
        """
        #here the user input is transferred to the dict, ready to use
        self.from_fields_to_dict()
        super(ProjectConfigurationDialog,self).confirm_dialog()

    def show(self, baseAppInstance):
        """Allows to show the widget as root window"""
        self.from_dict_to_fields()
        super(ProjectConfigurationDialog, self).show(baseAppInstance)


class SeisSpark(App):

    def __init__(self, *args):
        editor_res_path = os.path.join(os.path.dirname(__file__), 'res')
        
        html_head = '<script src="https://cdn.plot.ly/plotly-latest.js">'
        html_head += '</script>'
        
        self.projectPathFilename = ''
        super(SeisSpark, self).__init__(static_file_path=editor_res_path, html_head=html_head,
            *args)

    def main(self):
        self.projectConfiguration = ProjectConfigurationDialog(
            'Configuration', 'Write here the configuration for your project.')
        
        self.fileOpenDialog = EditorFileSelectionDialog('Open Project', 'Select the job file', False, './jobs', True, False, self)
        self.fileOpenDialog.set_on_confirm_value_listener(self.on_open_dialog_confirm)
        
        self.fileSaveAsDialog = EditorFileSaveDialog('Project Save', 'Select the job file', False, './jobs', True, True, self)
        self.fileSaveAsDialog.add_fileinput_field('untitled.job')
        self.fileSaveAsDialog.set_on_confirm_value_listener(self.on_saveas_dialog_confirm)        
        
        
        self.mainContainer = gui.Widget(
            width='100%', height='100%', layout_orientation=gui.Widget.LAYOUT_VERTICAL)
        self.mainContainer.style['background-color'] = 'white'
        self.mainContainer.style['border'] = 'none'

        self.subContainer = gui.HBox(
            width='100%', height='96%', layout_orientation=gui.Widget.LAYOUT_HORIZONTAL)
        self.subContainer.style['position'] = 'relative'
        self.subContainer.style['overflow'] = 'auto'
        self.subContainer.style['align-items'] = 'stretch'

        # here are contained the widgets
        self.workflowWidget = wiModuleWidget.WorkflowWidget(
            self, width='100%', height='50%')

#        self.project = Project(width='100%', height='100%')
        self._plotsWidget = wiPlotWidget.PlotsWidget(
            self, width='100%', height='100%')
#        self._plotsWidget.style['min-height'] = '400px'

        self.attributeEditor = wiParamsWidget.ParamsWidget(
            'Plot Params', self, width='100%')
#        self.attributeEditor.style['overflow'] = 'hide'
        self.moduleParamsWidget = wiParamsWidget.ParamsWidget(
            'Module Params', self, width='100%', height='50%')

        self.createMenu()
        self.mainContainer.append(self.menubar)
        self.mainContainer.append(self.subContainer)

        self.subContainerLeft = gui.Widget(width='20%', height='100%')
        self.subContainerLeft.style['position'] = 'relative'
        self.subContainerLeft.style['left'] = '0px'
        self.subContainerLeft.append(self.workflowWidget)
        self.subContainerLeft.append(self.moduleParamsWidget)
        self.subContainerLeft.add_class('RaisedFrame')

        self.centralContainer = gui.VBox(width='56%', height='100%')
#        self.centralContainer.append(self.toolbar)
        self.centralContainer.append(self._plotsWidget)

        self.subContainerRight = gui.Widget(width='24%', height='100%')
        self.subContainerRight.style['position'] = 'absolute'
        self.subContainerRight.style['right'] = '0px'
        self.subContainerRight.style['overflow'] = 'scroll'
        self.subContainerRight.add_class('RaisedFrame')

#        self.instancesWidget = editor_widgets.InstancesWidget(width='100%')
#        self.instancesWidget.dropDown.set_on_change_listener(self.on_instances_widget_selection)

#        self.subContainerRight.append(self.instancesWidget)
        self.subContainerRight.append(self.attributeEditor)

        self.subContainer.append(self.subContainerLeft)
        self.subContainer.append(self.centralContainer)
        self.subContainer.append(self.subContainerRight)
        self._plotsWidget.style['position'] = 'relative'

        # TODO: kostya
        self.workflowWidget.setParamWidget(self.moduleParamsWidget)
        self._plotsWidget.setParamWidget(self.attributeEditor)
        self.workflowWidget.open_job('./jobs/default.job')

        # returning the root widget
        return self.mainContainer

    def createPlot(self, name):
        if self._plotsWidget == None:
            return
        return self._plotsWidget.createPlot(name)

    def removePlot(self, mpwl):
        self._plotsWidget.removePlot(mpwl)

    def createMenu(self):
        self.menubar = gui.MenuBar(height='4%')
        menu = gui.Menu(width='100%', height='100%')
        menu.style['z-index'] = '1'
        m1 = gui.MenuItem('File', width=150, height='100%')
        m10 = gui.MenuItem('New', width=150, height=30)
        m11 = gui.MenuItem('Open', width=150, height=30)
        m12 = gui.MenuItem('Save Job...', width=150, height=30)
        #m12.style['visibility'] = 'hidden'
        m121 = gui.MenuItem('Save', width=100, height=30)
        m122 = gui.MenuItem('Save as', width=100, height=30)
        m1.append(m10)
        m1.append(m11)
        m1.append(m12)
        m12.append(m121)
        m12.append(m122)

#        m2 = gui.MenuItem('Edit', width=100, height='100%')
#        m21 = gui.MenuItem('Cut', width=100, height=30)
#        m22 = gui.MenuItem('Paste', width=100, height=30)
#        m2.append(m21)
#        m2.append(m22)

        m3 = gui.MenuItem('Config', width=200, height='100%')
        m4 = gui.MenuItem('Spark', width=200, height='100%')

        menu.append(m1)
#        menu.append(m2)
        menu.append(m3)
        menu.append(m4)
        
        self.menubar.append(menu)


#        self.toolbar = editor_widgets.ToolBar(width='100%', height='30px', margin='0px 0px')
#        self.toolbar.style['border-bottom'] = '1px solid rgba(0,0,0,.12)'
#        self.toolbar.add_command('/res/delete.png', self.toolbar_delete_clicked, 'Delete Widget')
#        self.toolbar.add_command('/res/cut.png', self.menu_cut_selection_clicked, 'Cut Widget')
#        self.toolbar.add_command('/res/paste.png', self.menu_paste_selection_clicked, 'Paste Widget')

        m10.set_on_click_listener(self.menu_new_clicked)
        m11.set_on_click_listener(self.fileOpenDialog.show)
        m121.set_on_click_listener(self.menu_save_clicked)
        m122.set_on_click_listener(self.fileSaveAsDialog.show)
#        m21.set_on_click_listener(self.menu_cut_selection_clicked)
#        m22.set_on_click_listener(self.menu_paste_selection_clicked)

        m3.set_on_click_listener(self.menu_project_config_clicked)
        m4.set_on_click_listener(self.menu_spark_clicked)
        
    def new_job (self):
        self.projectPathFilename = ''
        self.workflowWidget.new_job()
        
    def open_job (self, filename):
        self.projectPathFilename = filename
        self.workflowWidget.open_job(filename)
        
    def save_job (self, filename):
        self.projectPathFilename = filename
        self.workflowWidget.save_job(filename)
        
    def menu_project_config_clicked(self, widget):
        self.projectConfiguration.show(self)

    def menu_new_clicked(self, widget):
        self.new_job()
       
    def on_open_dialog_confirm(self, widget, filelist):
        if len(filelist):
            self.open_job(filelist[0])
        
    def menu_save_clicked(self, widget):
        if self.projectPathFilename == '':
            self.fileSaveAsDialog.show()
        else:
            self.save_job(self.projectPathFilename)
            
    def menu_spark_clicked(self, widget):
        cmd = """
            window.open('%(url)s', '_blank');
            """%{'url' : 'http://' + seisspark_config.external_ip+':8088'}

#        print ('redraw', cmd)
        self.execute_javascript(cmd)
        
        

    def on_saveas_dialog_confirm(self, widget, path):
        dprint ('on_saveas_dialog_confirm', path)
        if len(path):
            filename = path + '/' + self.fileSaveAsDialog.get_fileinput_value()
            dprint ('on_saveas_dialog_confirm', filename)
            self.save_job(filename)  

def main():
   start(SeisSpark, **seisspark_config.remi)

if __name__ == "__main__":
    main()
