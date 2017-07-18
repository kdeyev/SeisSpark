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
Created on Mon Nov 14 13:32:04 2016

@author: kdeyev
"""

import remi.gui as gui

import wiToolBar
import enEngine
import enModules
#import editor_widgets
from seisspark_config import dprint

g_moduleFactory = enModules.ModulesFactory()
g_moduleList = g_moduleFactory.getModileList()
g_moduleNames = g_moduleFactory.getModileNames()


class ModuleList(gui.ListView):

    def __init__(self, listView, appInstance):
        self._appInstance = appInstance
        self.listView = listView
        self._engine = enEngine.Engine(False)

    def addModule(self, module, afterMod = None):
        self._engine.addModule(module, afterMod)
        self.__rebuildGUI()

    def removeModule(self, module):
        self._engine.removeModule(module)
        self.__rebuildGUI()

    def upModule(self, module):
        self._engine.upModule(module)
        self.__rebuildGUI()

    def downModule(self, module):
        self._engine.downModule(module)
        self.__rebuildGUI()

    def __rebuildGUI(self):
        key = self.listView.get_key()
        self.listView.empty()
        for m in self._engine._modules:
            item = gui.ListItem(m._name)
            item._module = m
            self.listView.append(item, str(m._id))
        if key != None:
            self.listView.select_by_key(key)

    def calc(self):
        return self._engine.calc()
        
    def new_job (self):
        while len(self._engine._modules) != 0:
            self.removeModule(self._engine._modules[0]) # remove first
        self.__rebuildGUI()
        
    def open_job (self, filename):
        self.new_job()
        self._engine.loadFromFile(filename, self._appInstance)
        self.__rebuildGUI()
        
    def save_job (self, filename):
        self._engine.saveToFile(filename)

class WorkflowWidget(gui.Widget):

    def __init__(self, appInstance, **kwargs):
        super(WorkflowWidget, self).__init__(**kwargs)

        self._appInstance = appInstance
        self.paramsWidget = None

        self.lblTitle = gui.Label("Workflow editor")
        self.lblTitle.add_class("DialogTitle")

        self.createMainMenu()
        self.listView = gui.ListView(width='100%', height='85%')
        self.listView.style['left'] = '0%'
        self.listView.style['overflow-y'] = 'scroll'
        self.listView.style['overflow-x'] = 'hidden'
        self.listView.style['flex-wrap'] = 'wrap'
        self.listView.style['background-color'] = 'white'

        self._moduleList = ModuleList(self.listView, appInstance)

#        self.style['margin'] = '0px'

        self.append(self.lblTitle)
        self.append(self.listView)

        self.listView.set_on_selection_listener(self.moduleSelected)
#        self.paramsWidget.set_on_click_listener(self.paramsClicked)

    def setParamWidget(self, paramsWidget):
        self.paramsWidget = paramsWidget
        self.paramsWidget.set_on_attribute_change_listener(
                self.onattribute_changed)

#    def createModules(self):
#        import enEngineUT
#        for module in enEngineUT.defaultWorkFlow:
#            self._moduleList.addModule(
#                g_moduleFactory.createModule(module, self._appInstance))

    def createMainMenu(self):
        self._toolbar = wiToolBar.ToolBar(
            width='100%', height='30px', margin='0px 0px')
        self._toolbar.style['border-bottom'] = '1px solid rgba(0,0,0,.12)'
        self._toolbar.add_command(
            '/res/arrow-right.png', self.runClicked, 'Run workflow')
        self._toolbar.add_command(
            '/res/list-add.png', self.addClicked, 'Add module')
        self._toolbar.add_command(
            '/res/list-remove.png', self.deleteClicked, 'Delete module')
        self._toolbar.add_command(
            '/res/go-up.png', self.upClicked, 'Up module')
        self._toolbar.add_command(
            '/res/go-down.png', self.downClicked, 'Down module')

        self.append(self._toolbar)

    # listener function
    def runClicked(self, widget):
        import time
        t = time.time()
        error = self._moduleList.calc()
        elapsed = time.time()-t
        if error == None:
            self._appInstance.notification_message(
                "Calculation finished", "Calculation finished in " + str(elapsed) +"s. Thank you for choosing SeisSpark!")
        else:
            self._appInstance.notification_message("Calculation error", error)

#    def paramsClicked(self, widget):
#        selected_item_key = self._moduleList.get_key ()
#
#        module = None
#        if selected_item_key != None:
#            module_item = self._moduleList.children[selected_item_key]
#            module = module_item._module
#
#        d = ParamsDialog(self._appInstance, module)
#
##        self.moduleSelected(None, selected_item_key)
#        self.paramsWidget.setModule (module)

    def addClicked(self, widget):
        #        selected_item_key = self._moduleList.get_key ()
        #        module_item = self._moduleList.children[selected_item_key]

        addModuleDialog = gui.GenericDialog('Add new module', 'Choose module',
                                            width=500, height=160)
        
        # TODO new from list is not suitable
        drop = gui.DropDown()
        for i in range(len(g_moduleList)):
            drop.append(g_moduleNames[i], g_moduleList[i])
        addModuleDialog.add_field(
            "ModuleName", drop)
        addModuleDialog.set_on_confirm_dialog_listener(
            self.addClickedConfirmed)
        
        addModuleDialog.show(self._appInstance)

    def addClickedConfirmed(self, widget):
        module_guid = widget.get_field('ModuleName').get_key()

        sel_module = self.getSelectedModule()

        self._moduleList.addModule(
            g_moduleFactory.createModule(module_guid, self._appInstance), sel_module)

    def getSelectedModule(self):
        selected_item_key = self.listView.get_key()
        dprint('getSelectedModule', selected_item_key)
        module = None
        if selected_item_key != None:
            module_item = self.listView.children[selected_item_key]
            module = module_item._module
        return module
        
    def deleteClicked(self, widget):
        module = self.getSelectedModule()
        self._moduleList.removeModule(module)

    def upClicked(self, widget):
        module = self.getSelectedModule()

        if module != None:
            self._moduleList.upModule(module)

    def downClicked(self, widget):
        module = self.getSelectedModule()

        if module != None:
            self._moduleList.downModule(module)

    def moduleSelected(self, widget, selected_item_key):
        module_item = self.listView.children[selected_item_key]
        dprint('moduleSelected', selected_item_key)
        module = module_item._module
        if self.paramsWidget != None:
            self.paramsWidget.setParams(module._params)
            
    def onattribute_changed(self, widget, widgetAttributeMember, attributeName, newValue):
        module = self.getSelectedModule()
        dprint('module onattribute_changed', module._name)
        module.onParamsChanged()

    def new_job (self):
        self._moduleList.new_job()
        
    def open_job (self, filename):
        self._moduleList.open_job(filename)
        
    def save_job (self, filename):
        self._moduleList.save_job(filename)