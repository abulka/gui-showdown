import wx
from gui import MyFrame1  #  <--- the wxformbuilder generated python module
import esper
import time
import random
from dataclasses import dataclass
from typing import List, Any
from esper_extras import add_or_remove_component
from esper_observer import DirtyObserver, Dirty
from nested_dict_accessor import NestedDictAccess
from enum import Enum

#
# Model - The model is pure data.
#

model = {
    "welcomemsg": "Welcome", 
    "user": {
        "firstname": "Sam", 
        "surname": "Smith"
    }
}

#
# Mediators - are implemented as Entities with a list of data-only Components
#


@dataclass
class ModelRef(NestedDictAccess):  
    """
    Dynamically access or set nested dictionary keys in model
    Example: m = NestedDictAccess(model, ["user", "firstname"]); print(m.val); m.val = "fox"
    Params: 'data' ref to dict and list of 'keys' representing nested path
    """
    finalstr: str = ""


@dataclass
class PlainData:  
    finalstr: str = ""


@dataclass
class MultiModelRef:  # Refers to multiple model fields, since can only have one component per entity can't have multiple ModelRefs
    refs: List[ModelRef]


class GuiElType(Enum):  # Tells render system what kind of wxPython control 'set' value method to use to when rendering
    label = 1
    textctrl = 2
    frametitle = 3


@dataclass
class GuiControlRef:  # Mediator (entity + this component) needs to know about a wxPython gui control
    el: object        # reference to wxPython control, but could be implemented with 'id' string or something
    el_type: GuiElType   


@dataclass
class DisplayOptions:
    uppercase_welcome: bool = False
    uppercase_user: bool = False


@dataclass
class ComponentFrameAdornments:
    frame_title: str = ""
    frame_ref: Any = None
    panel_colour: Any = None
    panel_ref: Any = None
    panel_colour_randomise: bool = False


#
# Systems - (ECS behaviour)
#


class ModelExtractProcessor(esper.Processor):
    """
    Extract info from models and stage them in the component in 'finalstr', so that the transform phase
    can alter that info without altering the model.  This makes use of multiple 'system' transformations e.g.
    and decouples transformation from the final output/rendering system stage.
    """

    def process(self):
        print("--Model Extract System---")
        for ent, (component, _) in self.world.get_components(ModelRef, Dirty):
            component.finalstr = component.val
            logsimple(component, ent)

        for ent, (component, _) in self.world.get_components(MultiModelRef, Dirty):
            for model_ref in component.refs:
                model_ref.finalstr = model_ref.val


class CaseTransformProcessor(esper.Processor):
    def process(self):
        print("--Case transform System---")

        for ent, (component, display_options, _) in self.world.get_components(ModelRef, DisplayOptions, Dirty):
            if display_options.uppercase_welcome and "welcomemsg" in component.keys:
                component.finalstr = component.finalstr.upper()
                logsimple(component, ent)

        for ent, (component, display_options, _) in self.world.get_components(MultiModelRef, DisplayOptions, Dirty):
            for model_ref in component.refs:
                c = model_ref
                if (display_options.uppercase_welcome and "welcomemsg" in c.keys) or \
                   (display_options.uppercase_user and ("firstname" in c.keys or "surname" in c.keys)):
                    c.finalstr = c.finalstr.upper()
                    logsimple(component, ent)


class RenderProcessor(esper.Processor):
    def process(self):
        print("--Render System--")

        for ent, (component, gui, _) in self.world.get_components(ModelRef, GuiControlRef, Dirty):
            if "welcomemsg" in component.keys and gui.el_type == GuiElType.label:
                print("render static text for", ent)
                gui.el.SetLabel(component.finalstr)
            elif gui.el_type == GuiElType.textctrl:
                print("render textctrl for", ent)
                gui.el.SetValue(component.finalstr)

        for ent, (component, gui, _) in self.world.get_components(PlainData, GuiControlRef, Dirty):
            print("Plain data being rendered", gui)
            if gui.el_type == GuiElType.label:
                gui.el.SetLabel(component.finalstr)
            elif gui.el_type == GuiElType.textctrl:
                gui.el.SetValue(component.finalstr)
            elif gui.el_type == GuiElType.frametitle:
                gui.el.SetTitle(component.finalstr)

        msg = {}  # can't target how model ref components get found, so build up what we need here
        for ent, (component, gui, _) in self.world.get_components(MultiModelRef, GuiControlRef, Dirty):
            for model_ref in component.refs:
                assert gui.el_type == GuiElType.label
                msg[model_ref.keys[-1]] = model_ref.finalstr
            gui.el.SetLabel(f"{msg['welcomemsg']} {msg['firstname']} {msg['surname']}")
            print("render staticText for", ent)

        do.dirty_all(False, entities=mediators)


# class HousekeepingProcessor(esper.Processor):
#     def process(self):
#         print("--Housekeeping System--")

#         if frame.m_checkBox1.IsChecked():
#             frame.m_checkBox1A.Disable()
#         else:
#             frame.m_checkBox1A.Enable()


class FunProcessor(esper.Processor):
    def process(self):
        print("--Fun System--")

        for _, (f,) in self.world.get_components(ComponentFrameAdornments):
            f.frame_ref.SetTitle(f.frame_title + " " + time.asctime())
            f.panel_ref.SetBackgroundColour(
                wx.Colour(255, random.randint(120, 250), random.randint(120, 250)) if f.panel_colour_randomise else f.panel_colour
            )
            f.panel_ref.Refresh()  # f.panel_ref.Update() doesn't work, need to Refresh()


#
# Util
#


def logsimple(component, entity):  # simple logging
    print(f"have set {component} for {nice_entity_name[entity]}")


#
# Frame with GUI events
#

class MyFrame1A(MyFrame1):
    def on_button_reset_welcome(self, event):
        model["welcomemsg"] = "Hello"
        do.dirty(ModelRef, lambda component : "welcomemsg" in component.keys, filter_nice_name="welcomemsg")
        do.dirty(MultiModelRef)
        world.process()

    def on_button_reset_user(self, event):
        model["user"]["firstname"] = "Fred"
        model["user"]["surname"] = "Flinstone"
        do.dirty(ModelRef)  # could optimise with filters but don't bother, only one will be redundant
        do.dirty(MultiModelRef)
        world.process()

    def on_button_change_welcome_model_case(self, event):
        # toggle the case of the model's welcome message
        model["welcomemsg"] = model["welcomemsg"].upper() if model["welcomemsg"][1].islower() else model["welcomemsg"].lower()
        do.dirty(ModelRef, lambda component : "welcomemsg" in component.keys, filter_nice_name="welcomemsg")
        do.dirty(MultiModelRef)
        world.process()

    def on_button_change_user_model_case(self, event):
        # toggle the case of the model's user message
        model["user"]["firstname"] = model["user"]["firstname"].upper() if model["user"]["firstname"][1].islower() else model["user"]["firstname"].lower()
        model["user"]["surname"] = model["user"]["surname"].upper() if model["user"]["surname"][1].islower() else model["user"]["surname"].lower()
        do.dirty(ModelRef, lambda component : "firstname" in component.keys or "surname" in component.keys, filter_nice_name="firstname or surname")
        do.dirty(MultiModelRef)
        world.process()

    def on_check_toggle_welcome_outputs_only(self, event):
        # toggle the case of the welcome output messages only - do not affect model
        world.component_for_entity(entity_welcome_left, DisplayOptions).uppercase_welcome = event.GetEventObject().IsChecked()
        world.component_for_entity(entity_welcome_user_right, DisplayOptions).uppercase_welcome = event.GetEventObject().IsChecked()
        do.dirty("welcome display only, not via model")  # doesn't affect welcome text edit field
        world.process()

    def on_check_toggle_user_outputs_only(self, event):
        # toggle the case of the user output messages only - do not affect model
        world.component_for_entity(entity_welcome_user_right, DisplayOptions).uppercase_user = event.GetEventObject().IsChecked()
        do.dirty("user display only, not via model")  # doesn't affect welcome text edit field
        world.process()

    def on_check_upper_entire_top_right_output(self, event):
        # toggle the case of both the welcome and user output messages only on rhs (top right) display - do not affect model
        world.component_for_entity(entity_welcome_user_right, DisplayOptions).uppercase_welcome = event.GetEventObject().IsChecked()
        world.component_for_entity(entity_welcome_user_right, DisplayOptions).uppercase_user = event.GetEventObject().IsChecked()
        do.dirty("just top right")
        world.process()

    def on_enter_welcome(self, event):
        model["welcomemsg"] = event.GetEventObject().GetValue()
        do.dirty(ModelRef, lambda component : component.key == "welcomemsg", filter_nice_name="welcomemsg")
        do.dirty(MultiModelRef)
        world.process()

    def on_enter_user_firstname(self, event):
        model["user"]["firstname"] = event.GetEventObject().GetValue()
        do.dirty(ModelRef, lambda component : component.key == "firstname", filter_nice_name="firstname")
        do.dirty(MultiModelRef)
        world.process()

    def on_enter_user_surname(self, event):
        model["user"]["surname"] = event.GetEventObject().GetValue()
        do.dirty(ModelRef, lambda component : component.key == "surname", filter_nice_name="surname")
        do.dirty(MultiModelRef)
        world.process()

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

world = esper.World()
world.add_processor(ModelExtractProcessor())
world.add_processor(CaseTransformProcessor())
world.add_processor(RenderProcessor())
# world.add_processor(HousekeepingProcessor())
# world.add_processor(FunProcessor())

entity_welcome_left = world.create_entity(
    ModelRef(data=model, keys=["welcomemsg"]), 
    GuiControlRef(el=frame.m_staticText1, el_type=GuiElType.label),
    DisplayOptions()
)

entity_welcome_user_right = world.create_entity(
    MultiModelRef(refs=[
        ModelRef(data=model, keys=["welcomemsg"]),
        ModelRef(data=model, keys=["user", "firstname"]),
        ModelRef(data=model, keys=["user", "surname"]),
        ]),
    GuiControlRef(el=frame.m_staticText2, el_type=GuiElType.label),
    DisplayOptions()
)

entity_edit_welcome_msg = world.create_entity(
    ModelRef(data=model, keys=["welcomemsg"]), 
    GuiControlRef(el=frame.m_textCtrl1, el_type=GuiElType.textctrl)
)
entity_edit_user_name_msg = world.create_entity(
    ModelRef(data=model, keys=["user", "firstname"]), 
    GuiControlRef(el=frame.m_textCtrl2, el_type=GuiElType.textctrl)
)
entity_edit_user_surname_msg = world.create_entity(
    ModelRef(data=model, keys=["user", "surname"]), 
    GuiControlRef(el=frame.m_textCtrl3, el_type=GuiElType.textctrl)
)
entity_page_title = world.create_entity(
    PlainData("Gui wired via ECS (Entity Component System)"), 
    GuiControlRef(el=frame, el_type=GuiElType.frametitle)
)
appgui = world.create_entity()  # slightly different style, create entiry then add components
world.add_component(
    appgui,
    ComponentFrameAdornments(
        frame_title="Gui wired via ESC",
        frame_ref=frame,
        panel_colour=wx.Colour(255, 255, 135),
        panel_ref=frame.m_panel1,
        panel_colour_randomise=True,
    ),
)

nice_entity_name = {
    entity_welcome_left: "mediator for welcome_left",
    entity_welcome_user_right: "mediator for welcome_user_right",
    entity_edit_welcome_msg: "mediator for edit_welcome_msg",
    entity_edit_user_name_msg: "mediator for edit_user_name_msg",
    entity_edit_user_surname_msg: "mediator for edit_user_surname_msg",
    entity_page_title: "mediator for entity_page_title",
    appgui: "mediator for app frame etc",
}
mediators: List[int] = list(nice_entity_name.keys())

# Observer Wiring
do = DirtyObserver(world)

do.add_dependency(ModelRef, [entity_welcome_left, entity_edit_welcome_msg, entity_edit_user_name_msg, entity_edit_user_surname_msg])
do.add_dependency(MultiModelRef, [entity_welcome_user_right])
do.add_dependency("welcome display only, not via model", [entity_welcome_left, entity_welcome_user_right])
do.add_dependency("user display only, not via model", [entity_welcome_user_right])
do.add_dependency("just top right", [entity_welcome_user_right])

do.dirty_all(entities=mediators)  # initialise the gui with initial model values
world.process()

app.MainLoop()
