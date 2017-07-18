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
Created on Wed Nov 16 20:25:15 2016

@author: kdeyev
"""

import remi.gui as gui
from seisspark_config import dprint

class EditorAttributesGroup(gui.Widget):
    """ Contains a title and widgets. When the title is clicked, the contained widgets are hidden.
        Its scope is to provide a foldable group
    """

    def __init__(self, title, **kwargs):
        super(EditorAttributesGroup, self).__init__(**kwargs)
        self.add_class('.RaisedFrame')
        self.style['display'] = 'block'
        self.style['overflow'] = 'visible'
        self.opened = True
        self.title = gui.Label(title)
        self.title.add_class("Title")
        self.title.style['padding-left'] = '32px'
        self.title.style['background-image'] = "url('/res/minus.png')"
        self.title.style['background-repeat'] = 'no-repeat'
        self.title.style['background-position'] = '5px'
        self.title.style['border-bottom'] = '1px solid lightgray'
        self.title.set_on_click_listener(self.openClose)
        self.append(self.title, '0')

    def openClose(self, widget):
        self.opened = not self.opened
        backgroundImage = "url('/res/minus.png')" if self.opened else "url('/res/plus.png')"
        self.title.style['background-image'] = backgroundImage
        display = 'block' if self.opened else 'none'
        for widget in self.children.values():
            if widget != self.title and type(widget) != str:
                widget.style['display'] = display


class ParamsWidget(gui.VBox):
    """ Contains EditorAttributeInput each one of which notify a new value with an event
    """

    def __init__(self, label, appInstance, **kwargs):
        self._appInstance = appInstance

        super(ParamsWidget, self).__init__(**kwargs)
        self.EVENT_ATTRIB_ONCHANGE = 'on_attribute_changed'
        #self.style['overflow-y'] = 'scroll'
        self.style['justify-content'] = 'flex-start'
        self.style['-webkit-justify-content'] = 'flex-start'
        self.titleLabel = gui.Label(label, width='100%')
        self.titleLabel.add_class("DialogTitle")
        self.infoLabel = gui.Label('Selected widget: None')
        self.infoLabel.style['font-weight'] = 'bold'
        self.append(self.titleLabel)
        self.append(self.infoLabel)

        self.titleLabel.style['order'] = '-1'
        self.titleLabel.style['-webkit-order'] = '-1'
        self.infoLabel.style['order'] = '0'
        self.infoLabel.style['-webkit-order'] = '0'

        self.attributesInputs = list()
        # load editable attributes
        self.append(self.titleLabel)
        self.attributeGroups = {}

    def set_on_attribute_change_listener(self, callback, *userdata):
        self.eventManager.register_listener(
            self.EVENT_ATTRIB_ONCHANGE, callback, *userdata)

    # this function is called by an EditorAttributeInput change event and propagates to the listeners
    # adding as first parameter the tag to which it refers
    # widgetAttributeMember can be 'style' or 'attributes'
    def onattribute_changed(self, widget, widgetAttributeMember, attributeName, newValue):
        dprint("setting attribute name: %s    value: %s    attributeMember: %s" % (
            attributeName, newValue, widgetAttributeMember))
        self._params.put(attributeName, newValue)
        return self.eventManager.propagate(self.EVENT_ATTRIB_ONCHANGE, (widgetAttributeMember, attributeName, newValue))

    def setParams(self, params):
        self.empty()
        self._params = params
        self.__generateWidgets()

    def __generateWidgets(self):
        self.attributesInputs = list()
        # load editable attributes
        self.append(self.titleLabel)
        self.attributeGroups = {}

        if self._params == None:
            return

        for p in self._params._par:
            groupName = p._group
            attributeEditor = EditorAttributeInput(p, self._appInstance)
            attributeEditor.set_on_attribute_change_listener(
                self.onattribute_changed)
#            attributeEditor.set_on_attribute_remove_listener(self.onattribute_remove)
            #attributeEditor.style['display'] = 'none'
            if not groupName in self.attributeGroups.keys():
                groupContainer = EditorAttributesGroup(groupName, width='100%')
                self.attributeGroups[groupName] = groupContainer
                self.append(groupContainer)
#                groupContainer.style['order'] = str(html_helper.editorAttributesGroupOrdering[groupName])
#                groupContainer.style['-webkit-order'] = str(html_helper.editorAttributesGroupOrdering[groupName])

            self.attributeGroups[groupName].append(attributeEditor)
            self.attributesInputs.append(attributeEditor)

# class CssSizeInput(gui.Widget):
#    def __init__(self, appInstance, **kwargs):
#        super(CssSizeInput, self).__init__(**kwargs)
#        self.appInstance = appInstance
#        self.set_layout_orientation(gui.Widget.LAYOUT_HORIZONTAL)
#        self.style['display'] = 'block'
#        self.style['overflow'] = 'hidden'
#
#        self.numInput = gui.SpinBox('0',-999999999, 999999999, 1, width='60%', height='100%')
#        self.numInput.set_on_change_listener(self.on_value_changed)
#        self.numInput.style['text-align'] = 'right'
#        self.append(self.numInput)
#
#        self.dropMeasureUnit = gui.DropDown(width='40%', height='100%')
#        self.dropMeasureUnit.append( gui.DropDownItem('px'), 'px' )
#        self.dropMeasureUnit.append( gui.DropDownItem('%'), '%' )
#        self.dropMeasureUnit.select_by_key('px')
#        self.dropMeasureUnit.set_on_change_listener(self.on_value_changed)
#        self.append(self.dropMeasureUnit)
#
#    def on_value_changed(self, widget, new_value):
#        new_size = str(self.numInput.get_value()) + str(self.dropMeasureUnit.get_value())
#        return self.eventManager.propagate(self.EVENT_ONCHANGE, (new_size,))
#
#    def set_on_change_listener(self, callback, *userdata):
#        self.eventManager.register_listener(self.EVENT_ONCHANGE, callback, *userdata)
#
#    def set_value(self, value):
#        """The value have to be in the form '10px' or '10%', so numeric value plus measure unit
#        """
#        v = 0
#        measure_unit = 'px'
#        try:
#            v = int(float(value.replace('px', '')))
#        except ValueError:
#            try:
#                v = int(float(value.replace('%', '')))
#                measure_unit = '%'
#            except ValueError:
#                pass
#        self.numInput.set_value(v)
#        self.dropMeasureUnit.set_value(measure_unit)
#
#
# class UrlPathInput(gui.Widget):
#    def __init__(self, appInstance, **kwargs):
#        super(UrlPathInput, self).__init__(**kwargs)
#        self.appInstance = appInstance
#        self.set_layout_orientation(gui.Widget.LAYOUT_HORIZONTAL)
#        self.style['display'] = 'block'
#        self.style['overflow'] = 'hidden'
#
#        self.txtInput = StringEditor(width='80%', height='100%')
#        self.txtInput.style['float'] = 'left'
#        self.txtInput.set_on_change_listener(self.on_txt_changed)
#        self.append(self.txtInput)
#
#        self.btFileFolderSelection = gui.Widget(width='20%', height='100%')
#        self.btFileFolderSelection.style['background-repeat'] = 'round'
#        self.btFileFolderSelection.style['background-image'] = "url('/res/folder.png')"
#        self.btFileFolderSelection.style['background-color'] = 'transparent'
#        self.append(self.btFileFolderSelection)
#        self.btFileFolderSelection.set_on_click_listener(self.on_file_selection_bt_pressed)
#
#        self.selectionDialog = gui.FileSelectionDialog('Select a file', '', False, './', True, False)
#        self.selectionDialog.set_on_confirm_value_listener(self.file_dialog_confirmed)
#
#    def on_txt_changed(self, widget, value):
#        return self.eventManager.propagate(self.EVENT_ONCHANGE, (value,))
#
#    def on_file_selection_bt_pressed(self, widget):
#        self.selectionDialog.show(self.appInstance)
#
#    def file_dialog_confirmed(self, widget, fileList):
#        if len(fileList)>0:
#            self.txtInput.set_value("url('/res/" + fileList[0].split('/')[-1].split('\\')[-1] + "')")
#            return self.eventManager.propagate(self.EVENT_ONCHANGE, (self.txtInput.get_value(),))
#
#    def set_on_change_listener(self, callback, *userdata):
#        self.eventManager.register_listener(self.EVENT_ONCHANGE, callback, *userdata)
#
#    def set_value(self, value):
#        self.txtInput.set_value(value)


class StringEditor(gui.TextInput):
    """ This class sends the input directly to the listener, but don't applies the changes
        to the widget itself in order to avoid to get updated losting the focus.
        The value will be committed to the widget itself when blurs.
    """

    def __init__(self, *args, **kwargs):
        super(StringEditor, self).__init__(True, *args, **kwargs)
        self.attributes[self.EVENT_ONBLUR] = \
            """var elem=document.getElementById('%(id)s');elem.value = elem.value.split('\\n').join(''); 
            var params={};params['new_value']=elem.value;
            sendCallbackParam('%(id)s','%(evt)s',params);""" % {'id': self.identifier, 'evt': self.EVENT_ONCHANGE}

        self.attributes[self.EVENT_ONKEYUP] = \
            """var elem=document.getElementById('%(id)s');elem.value = elem.value.split('\\n').join(''); 
            var params={};params['new_value']=elem.value;
            sendCallbackParam('%(id)s','%(evt)s',params);""" % {'id': self.identifier, 'evt': self.EVENT_ONKEYUP}

        self.attributes[self.EVENT_ONKEYDOWN] = \
            """if((event.charCode||event.keyCode)==13){event.keyCode = 0;event.charCode = 0; return false;}"""  # % {'id': self.identifier}

    def onkeyup(self, new_value):
        return self.eventManager.propagate(self.EVENT_ONCHANGE, (new_value,))


# widget that allows to edit a specific html and css attributes
# it has a descriptive label, an edit widget (TextInput, SpinBox..) based
# on the 'type' and a title
class EditorAttributeInput(gui.Widget):

    def __init__(self, param, appInstance=None):
        super(EditorAttributeInput, self).__init__()

        self._param = param
        attributeName = self._param._k
        attributeDesc = self._param._description

        self.set_layout_orientation(gui.Widget.LAYOUT_HORIZONTAL)
        self.style['display'] = 'block'
        self.style['overflow'] = 'auto'
        self.style['margin'] = '2px'
        self.attributeName = attributeName
        self.EVENT_ATTRIB_ONCHANGE = 'on_attribute_changed'

        self.EVENT_ATTRIB_ONREMOVE = 'onremove_attribute'
        self.removeAttribute = gui.Image('/res/delete.png', width='5%')
        self.removeAttribute.attributes[
            'title'] = 'Remove attribute from this widget.'
        self.removeAttribute.set_on_click_listener(self.on_attribute_remove)
        self.append(self.removeAttribute)

        self.label = gui.Label(attributeName, width='45%',
                               height=22, margin='0px')
        self.label.style['overflow'] = 'hidden'
        self.label.style['font-size'] = '13px'
        self.append(self.label)
        self.label.attributes['title'] = attributeDesc

        self.__createEditor()

        self.style['display'] = 'block'
        self.set_valid(True)

    def __createEditor(self):
        attributeType = self._param._type
        additionalInfo = self._param._additionalInfo
        attributeValue = self._param._v
        attributeName = self._param._k
        attributeDesc = self._param._description
        if additionalInfo == None:
            additionalInfo = {}

        dprint('name', attributeName, 'type', attributeType,
              'value', attributeValue, 'info', additionalInfo)

        self.inputWidget = None

        #'background-repeat':{'type':str, 'description':'The repeat behaviour of an optional background image', ,'additional_data':{'affected_widget_attribute':'style', 'possible_values':'repeat | repeat-x | repeat-y | no-repeat | inherit'}},
        if attributeType == bool or attributeType == 'bool':
            if attributeValue == 'true':
                attributeValue =True
            if attributeValue == 'false':
                attributeValue =False
            self.inputWidget = gui.CheckBox('checked')
        elif attributeType == int or attributeType == float or attributeType == 'int' or attributeType == 'float':
            min_val = -1000000
            if "min" in additionalInfo:
                min_val = additionalInfo['min']
            max_val = 1000000
            if "max" in additionalInfo:
                max_val = additionalInfo['max']
            step_val = 1
            if "step" in additionalInfo:
                step_val = additionalInfo['step']
            self.inputWidget = gui.SpinBox(
                attributeValue, min_val, max_val, step_val)
        elif attributeType == gui.ColorPicker:
            self.inputWidget = gui.ColorPicker()
        elif attributeType == 'dropdown':
            self.inputWidget = gui.DropDown()
            for value in additionalInfo['possible_values']:
                self.inputWidget.append(gui.DropDownItem(value), value)
#        elif attributeType == 'url_editor':
#            self.inputWidget = UrlPathInput(self._appInstance)
#        elif attributeType == 'css_size':
#            self.inputWidget = CssSizeInput(self._appInstance)
        else:  # default editor is string
            self.inputWidget = StringEditor()

        self.inputWidget.set_on_change_listener(self.on_attribute_changed)
        self.inputWidget.set_size('50%', '22px')
        self.inputWidget.attributes['title'] = attributeDesc
        self.inputWidget.style['float'] = 'right'
        self.inputWidget.set_value(attributeValue)
        dprint ('setValue', attributeValue)
        dprint ('getValue', self.inputWidget.get_value())
        
        self.append(self.inputWidget)

    def set_valid(self, valid=True):
        self.label.style['opacity'] = '1.0'
        if 'display' in self.removeAttribute.style:
            del self.removeAttribute.style['display']
        if not valid:
            self.label.style['opacity'] = '0.5'
            self.removeAttribute.style['display'] = 'none'

    def on_attribute_remove(self, widget):
        self.inputWidget.set_value(self._param._defaultValue)
        self.on_attribute_changed(widget, self._param._defaultValue)

    def set_value(self, value):
        self.set_valid()
        self.inputWidget.set_value(value)

    def on_attribute_changed(self, widget, value):
        self.set_valid()
        
        # stupid patch for bool
        attributeType = self._param._type
        if attributeType == bool or attributeType == 'bool':
            if value == 'true':
                value =True
            if value == 'false':
                value =False
                
        return self.eventManager.propagate(self.EVENT_ATTRIB_ONCHANGE, ("", self.attributeName, value))

    def set_on_attribute_change_listener(self, callback, *userdata):
        self.eventManager.register_listener(
            self.EVENT_ATTRIB_ONCHANGE, callback, *userdata)
