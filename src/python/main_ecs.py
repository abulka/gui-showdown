import wx
from gui import MyFrame1  #  <--- the wxformbuilder generated python module
import esper
import time
import random
from dataclasses import dataclass
from typing import List, Any
from enum import Enum

engine = world = esper.World()

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



# OLD



# message = world.create_entity(
#     ModelRef(data=model, keys=["welcomemsg"]), 
#     GuiControlRef(el=frame.m_staticText1, el_type=GuiElType.label),
#     DisplayOptions()
# )

# #
# # Model - The model is pure data.
# #

# model = {
#     "welcomemsg": "Welcome", 
#     "user": {
#         "firstname": "Sam", 
#         "surname": "Smith"
#     }
# }

# #
# # Mediators - are implemented as Entities with a list of data-only Components
# #


# @dataclass
# class ModelRef(NestedDictAccess):  
#     """
#     Dynamically access or set nested dictionary keys in model
#     Example: m = NestedDictAccess(model, ["user", "firstname"]); print(m.val); m.val = "fox"
#     Params: 'data' ref to dict and list of 'keys' representing nested path
#     """
#     finalstr: str = ""


# @dataclass
# class PlainData:  
#     finalstr: str = ""


# @dataclass
# class MultiModelRef:  # Refers to multiple model fields, since can only have one component per entity can't have multiple ModelRefs
#     refs: List[ModelRef]


# class GuiElType(Enum):  # Tells render system what kind of wxPython control 'set' value method to use to when rendering
#     label = 1
#     textctrl = 2
#     frametitle = 3


# @dataclass
# class GuiControlRef:  # Mediator (entity + this component) needs to know about a wxPython gui control
#     el: object        # reference to wxPython control, but could be implemented with 'id' string or something
#     el_type: GuiElType   


# @dataclass
# class DisplayOptions:
#     uppercase_welcome: bool = False
#     uppercase_user: bool = False


# @dataclass
# class ComponentFrameAdornments:
#     frame_title: str = ""
#     frame_ref: Any = None
#     panel_colour: Any = None
#     panel_ref: Any = None
#     panel_colour_randomise: bool = False


# #
# # Systems - (ECS behaviour)
# #


# class ModelExtractProcessor(esper.Processor):
#     """
#     Extract info from models and stage them in the component in 'finalstr', so that the transform phase
#     can alter that info without altering the model.  This makes use of multiple 'system' transformations e.g.
#     and decouples transformation from the final output/rendering system stage.
#     """

#     def process(self):
#         print("--Model Extract System---")
#         for ent, (component, _) in self.world.get_components(ModelRef, Dirty):
#             component.finalstr = component.val
#             logsimple(component, ent)

#         for ent, (component, _) in self.world.get_components(MultiModelRef, Dirty):
#             for model_ref in component.refs:
#                 model_ref.finalstr = model_ref.val


# class CaseTransformProcessor(esper.Processor):
#     def process(self):
#         print("--Case transform System---")

#         for ent, (component, display_options, _) in self.world.get_components(ModelRef, DisplayOptions, Dirty):
#             if display_options.uppercase_welcome and "welcomemsg" in component.keys:
#                 component.finalstr = component.finalstr.upper()
#                 logsimple(component, ent)

#         for ent, (component, display_options, _) in self.world.get_components(MultiModelRef, DisplayOptions, Dirty):
#             for model_ref in component.refs:
#                 c = model_ref
#                 if (display_options.uppercase_welcome and "welcomemsg" in c.keys) or \
#                    (display_options.uppercase_user and ("firstname" in c.keys or "surname" in c.keys)):
#                     c.finalstr = c.finalstr.upper()
#                     logsimple(component, ent)


# class RenderProcessor(esper.Processor):

#     def render(self, s, gui):  # Helper
#         if gui.el_type == GuiElType.label:
#             gui.el.SetLabel(s)
#         elif gui.el_type == GuiElType.textctrl:
#             gui.el.SetValue(s)
#         elif gui.el_type == GuiElType.frametitle:
#             gui.el.SetTitle(s)

#     def gather_model_refs_into_single_dict(self, c_multi_model_ref):  # Helper
#         data = {}  # can't target how model ref components get found, so build up multi model output string here, via dict
#         for ent, (component, gui, _) in self.world.get_components(MultiModelRef, GuiControlRef, Dirty):
#             for model_ref in component.refs:
#                 data[model_ref.keys[-1]] = model_ref.finalstr
#         return data

#     def process(self):
#         print("--Render System--")

#         for ent, (component, gui, _) in self.world.get_components(ModelRef, GuiControlRef, Dirty):
#             self.render(component.finalstr, gui)

#         for ent, (component, gui, _) in self.world.get_components(PlainData, GuiControlRef, Dirty):
#             self.render(component.finalstr, gui)

#         for ent, (component_multi_model_ref, gui, _) in self.world.get_components(MultiModelRef, GuiControlRef, Dirty):
#             data = self.gather_model_refs_into_single_dict(component_multi_model_ref)
#             self.render(f"{data['welcomemsg']} {data['firstname']} {data['surname']}", gui)

#         do.dirty_all(False, entities=mediators)


# class HousekeepingProcessor(esper.Processor):
#     def process(self):
#         print("--Housekeeping System--")

#         if frame.m_checkBox1.IsChecked():
#             frame.m_checkBox1A.Disable()
#         else:
#             frame.m_checkBox1A.Enable()


# class FunProcessor(esper.Processor):
#     def process(self):
#         print("--Fun System--")

#         for _, (f,) in self.world.get_components(ComponentFrameAdornments):
#             f.frame_ref.SetTitle(f.frame_title + " " + time.asctime())
#             f.panel_ref.SetBackgroundColour(
#                 wx.Colour(255, random.randint(120, 250), random.randint(120, 250)) if f.panel_colour_randomise else f.panel_colour
#             )
#             f.panel_ref.Refresh()  # f.panel_ref.Update() doesn't work, need to Refresh()


#
# Util
#


def logsimple(component, entity):  # simple logging
    print(f"have set {component} for {nice_entity_name[entity]}")


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
# Init WxPython
#

app = wx.App()
frame = MyFrame1A(None)
frame.SetTitle("Gui wired via ECS")
frame.Show()
frame.SetSize((500, 450))

#
# Wire up and build everything
#



 # Systems

#   engine.system('controller-model', ['data'], (entity, { data }) => {
#     if (entity.name == 'model-welcome-message') $('input[name=welcome]').val(data.val)
#     else if (entity.name == 'model-firstname') $('input[name=firstname]').val(data.val)
#     else if (entity.name == 'model-surname') $('input[name=surname]').val(data.val)
#     log(`controller-model: ${entity.name}, ${data.val}`);
#   });

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











# OLD


# world = esper.World()
# world.add_processor(ModelExtractProcessor())
# world.add_processor(CaseTransformProcessor())
# world.add_processor(RenderProcessor())
# world.add_processor(HousekeepingProcessor())
# world.add_processor(FunProcessor())

# entity_welcome_left = world.create_entity(
#     ModelRef(data=model, keys=["welcomemsg"]), 
#     GuiControlRef(el=frame.m_staticText1, el_type=GuiElType.label),
#     DisplayOptions()
# )

# entity_welcome_user_right = world.create_entity(
#     MultiModelRef(refs=[
#         ModelRef(data=model, keys=["welcomemsg"]),
#         ModelRef(data=model, keys=["user", "firstname"]),
#         ModelRef(data=model, keys=["user", "surname"]),
#         ]),
#     GuiControlRef(el=frame.m_staticText2, el_type=GuiElType.label),
#     DisplayOptions()
# )

# entity_edit_welcome_msg = world.create_entity(
#     ModelRef(data=model, keys=["welcomemsg"]), 
#     GuiControlRef(el=frame.m_textCtrl1, el_type=GuiElType.textctrl)
# )
# entity_edit_user_name_msg = world.create_entity(
#     ModelRef(data=model, keys=["user", "firstname"]), 
#     GuiControlRef(el=frame.m_textCtrl2, el_type=GuiElType.textctrl)
# )
# entity_edit_user_surname_msg = world.create_entity(
#     ModelRef(data=model, keys=["user", "surname"]), 
#     GuiControlRef(el=frame.m_textCtrl3, el_type=GuiElType.textctrl)
# )
# entity_page_title = world.create_entity(
#     PlainData("Gui wired via ECS (Entity Component System)"), 
#     GuiControlRef(el=frame, el_type=GuiElType.frametitle)
# )
# appgui = world.create_entity()  # slightly different style, create entiry then add components
# world.add_component(
#     appgui,
#     ComponentFrameAdornments(
#         frame_title="Gui wired via ESC",
#         frame_ref=frame,
#         panel_colour=wx.Colour(255, 255, 135),
#         panel_ref=frame.m_panel1,
#         panel_colour_randomise=True,
#     ),
# )

# nice_entity_name = {
#     entity_welcome_left: "mediator for welcome_left",
#     entity_welcome_user_right: "mediator for welcome_user_right",
#     entity_edit_welcome_msg: "mediator for edit_welcome_msg",
#     entity_edit_user_name_msg: "mediator for edit_user_name_msg",
#     entity_edit_user_surname_msg: "mediator for edit_user_surname_msg",
#     entity_page_title: "mediator for entity_page_title",
#     appgui: "mediator for app frame etc",
# }
# mediators: List[int] = list(nice_entity_name.keys())

# # Observer Wiring
# do = DirtyObserver(world)

# do.add_dependency(ModelRef, [entity_welcome_left, entity_edit_welcome_msg, entity_edit_user_name_msg, entity_edit_user_surname_msg])
# do.add_dependency(MultiModelRef, [entity_welcome_user_right])
# do.add_dependency("welcome display only, not via model", [entity_welcome_left, entity_welcome_user_right])
# do.add_dependency("user display only, not via model", [entity_welcome_user_right])
# do.add_dependency("just top right", [entity_welcome_user_right])

# do.dirty_all(entities=mediators)  # initialise the gui with initial model values


# Util - Uppercase

def toggleCase(s):
    return s.lower() if s.isupper() else s.upper()

world.process()

app.MainLoop()
