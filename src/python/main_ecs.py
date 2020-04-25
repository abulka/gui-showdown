import wx
from gui import MyFrame1  #  <--- the wxformbuilder generated python module
import esper
import time
import random
from dataclasses import dataclass
from typing import List, Any
from enum import Enum


engine = world = esper.World()


# Util - Uppercase

def toggleCase(s):
    return s.lower() if s.isupper() else s.upper()

#
# Frame with GUI events
#

class MyFrame1A(MyFrame1):
    def __init__(self, parent):
        MyFrame1.__init__(self, parent)

        # CMD-W to close Frame by attaching the key bind event to accellerator table
        id_close = wx.NewIdRef()
        self.Bind(wx.EVT_MENU, self.OnCloseWindow, id=id_close)
        accel_tbl = wx.AcceleratorTable([(wx.ACCEL_CTRL, ord("W"), id_close)])
        self.SetAcceleratorTable(accel_tbl)

    def OnCloseWindow(self, event):
        self.Destroy()

    # Overridden events

    # Which change the actual model - input fields

    def on_enter_welcome(self, event):
        set_message(event.GetEventObject().GetValue())
        world.process()

    def on_enter_user_firstname(self, event):
        set_firstname(event.GetEventObject().GetValue())
        world.process()

    def on_enter_user_surname(self, event):
        set_surname(event.GetEventObject().GetValue())
        world.process()

    # Which change the actual model - buttons

    def on_button_change_welcome_model_case(self, event):
        # toggle the case of the model's welcome message
        toggle_message()
        world.process()

    def on_button_change_user_model_case(self, event):
        # toggle the case of the model's user message
        toggle_user()
        world.process()
    
    def on_button_reset_welcome(self, event):
        set_message("Hello")
        world.process()

    def on_button_reset_user(self, event):
        set_firstname("Fred")
        set_surname("Flinstone")
        world.process()

    # Which change the way the model is displayed at the top left and top right, but does not change the model

    def on_check_toggle_welcome_outputs_only(self, event):
        # toggle the case of the welcome output messages only - do not affect model
        display_option_toggle_message_case(event.GetEventObject().IsChecked())
        world.process()

    def on_check_toggle_user_outputs_only(self, event):
        # toggle the case of the user output messages only - do not affect model
        display_option_toggle_user_case(event.GetEventObject().IsChecked())
        world.process()

    def on_check_upper_entire_top_right_output(self, event):
        # toggle the case of both the welcome and user output messages only on rhs (top right) display - do not affect model
        display_option_toggle_topright_case(event.GetEventObject().IsChecked())
        world.process()

    # Debug

    def onClickRenderNow(self, event):
        world.process()


# 
# Model - of a sort ;-)
#

# Declare entities - this is like the model, but without data - we attach that later, as 'components'
message = engine.create_entity('model-welcome-message')
firstname = engine.create_entity('model-firstname')
surname = engine.create_entity('model-surname')
topright = engine.create_entity('display-model-topright')

# Map entities (which are just id's) into meaningful names for debugging
entity_name = {
    message: "message",
    firstname: "firstname",
    surname: "surname",
    topright: "topright",
}

# Components - simple, pure data
@dataclass
class Data:
    val: str = ""

@dataclass
class DisplayOptions:
    upper: bool = False

@dataclass
class RenderData:
    welcome: str = ""
    firstname: str = ""
    surname: str = ""

# Associate the model entities to components.
engine.add_component(message, Data(val="Welcome"))
engine.add_component(firstname, Data(val="Sam"))
engine.add_component(surname, Data(val="Smith"))
engine.add_component(topright, RenderData(welcome="", firstname="", surname=""))
engine.add_component(message, DisplayOptions(upper=False))
engine.add_component(firstname, DisplayOptions(upper=False))
engine.add_component(surname, DisplayOptions(upper=False))
engine.add_component(topright, DisplayOptions(upper=False))


# App - Set Model

def set_message(val):
    engine.component_for_entity(message, Data).val = val

def set_firstname(val):
    engine.component_for_entity(firstname, Data).val = val

def set_surname(val):
    engine.component_for_entity(surname, Data).val = val

# App - Toggle Model

def toggle_message():
    data = engine.component_for_entity(message, Data)
    data.val = toggleCase(data.val)

def toggle_user():
    data = engine.component_for_entity(firstname, Data)
    data.val = toggleCase(data.val)
    data = engine.component_for_entity(surname, Data)
    data.val = toggleCase(data.val)


# App - Display Option Checkbox toggles

def display_option_toggle_message_case(flag):
    engine.component_for_entity(message, DisplayOptions).upper = flag

def display_option_toggle_user_case(flag):
    engine.component_for_entity(firstname, DisplayOptions).upper = flag
    engine.component_for_entity(surname, DisplayOptions).upper = flag

def display_option_toggle_topright_case(flag):
    engine.component_for_entity(topright, DisplayOptions).upper = flag


# Init WxPython - do this before defining Systems which need to refer to 'frame'
app = wx.App()
frame = MyFrame1A(None)
frame.SetTitle("Gui wired via ECS")
frame.Show()
frame.SetSize((500, 450))


# Systems


class ControllerModel(esper.Processor):
    """Render model into input fields"""
    def process(self):
        for entity, (data,) in self.world.get_components(Data):
            if entity == message: frame.m_textCtrl1.SetValue(data.val)
            elif entity == firstname: frame.m_textCtrl2.SetValue(data.val)
            elif entity == surname: frame.m_textCtrl3.SetValue(data.val)
            print(f"controller-model: {entity_name[entity]}, {data.val}")

class PreRenderTopRight(esper.Processor):
    """Gather/buffer partial info from individual entities/models into a 
    final 'display model' entity for later render at top right of GUI
    """
    def process(self):
        for entity, (data, displayOptions) in self.world.get_components(Data, DisplayOptions):
            buffer = engine.component_for_entity(topright, RenderData)
            if entity == message:
                buffer.welcome = data.val.upper() if displayOptions.upper else data.val
            elif entity == firstname:
                buffer.firstname = data.val.upper() if displayOptions.upper else data.val
            elif entity == surname:
                buffer.surname = data.val.upper() if displayOptions.upper else data.val
            print(f"pre-render-topright: {entity_name[entity]}, {data.val}, {displayOptions}")

class ControllerTopLeft(esper.Processor):
    """Gather/buffer partial info from individual entities/models into a 
    final 'display model' entity for later render at top right of GUI
    """
    def process(self):
        for entity, (data, displayOptions) in self.world.get_components(Data, DisplayOptions):
            if entity == message:
                s = data.val.upper() if displayOptions.upper else data.val
                frame.m_staticText1.SetLabel(s)
                print(f"controller-topleft: {entity_name[entity]}, {data.val}, {displayOptions}")

class ControllerTopRight(esper.Processor):
    """Gather/buffer partial info from individual entities/models into a 
    final 'display model' entity for later render at top right of GUI
    """
    def process(self):
        for entity, (rdata, displayOptions) in self.world.get_components(RenderData, DisplayOptions):
            s = f"{rdata.welcome} {rdata.firstname} {rdata.surname}"
            if displayOptions.upper:
                s = s.upper()
            frame.m_staticText2.SetLabel(s)
            print(f"controller-topright: {entity_name[entity]}, {rdata}, {displayOptions}")


engine.add_processor(ControllerModel())
engine.add_processor(PreRenderTopRight())
engine.add_processor(ControllerTopLeft())
engine.add_processor(ControllerTopRight())

world.process()

app.MainLoop()
