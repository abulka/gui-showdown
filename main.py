import wx
from gui import MyFrame1  #  <--- the wxformbuilder generated python module
import esper
import time
import random
from dataclasses import dataclass
from typing import List, Any
from esper_extras import add_or_remove_component
from esper_observer import DirtyObserver, Dirty

#
# Model - The model is pure data.
#

model = {"welcomemsg": "Welcome", "user": {"firstname": "Sam", "surname": "Smith"}}

#
# Mediators - are implemented as Entities with a list of data-only Components
#


@dataclass
class ModelRef:  # Mediator (entity + this component) needs to know about model. Model specific
    model: dict
    key: str
    finalstr: str = ""

@dataclass
class MultiModelRef:  # Refers to multiple model fields, since can only have one component per entity can't have multiple ModelRefs
    refs: List[ModelRef]


@dataclass
class GuiControlRef:  # Mediator (entity + this component) needs to know about a wxPython gui control
    ref: object


class ComponentGuiStaticText(GuiControlRef):
    pass  # Static Text Gui ref


class ComponentGuiTextControl(GuiControlRef):
    pass  # Text Control Gui ref


@dataclass
class Flag:  # Mediator (entity + this component) might have a flag to indicate some behaviour is wanted
    pass


class ComponentUppercaseAll(Flag):
    pass  # flag to make upper right message uppercase or not


class ComponentUppercaseWelcome(Flag):
    pass  # flag to make upper left AND upper right (welcome portion ONLY) message uppercase or not


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
            component.finalstr = component.model[component.key]
            logsimple(component, ent)

        for ent, (component, _) in self.world.get_components(MultiModelRef, Dirty):
            for model_ref in component.refs:
                model_ref.finalstr = model_ref.model[model_ref.key]


class CaseTransformProcessor(esper.Processor):
    def process(self):
        print("--Case transform System---")

        for ent, (component, _, _) in self.world.get_components(ModelRef, ComponentUppercaseWelcome, Dirty):
            if component.key == "welcomemsg":
                component.finalstr = component.finalstr.upper()
                logsimple(component, ent)

        for ent, (component, _, _) in self.world.get_components(MultiModelRef, ComponentUppercaseWelcome, Dirty):
            for model_ref in component.refs:
                if model_ref.key == "welcomemsg":
                    model_ref.finalstr = model_ref.finalstr.upper()
                    logsimple(component, ent)

        for ent, (component, _, _) in self.world.get_components(MultiModelRef, ComponentUppercaseAll, Dirty):
            for model_ref in component.refs:
                model_ref.finalstr = model_ref.finalstr.upper()
            logsimple(component, ent)


class RenderProcessor(esper.Processor):
    def process(self):
        print("--Render System--")

        for ent, (component, gui, _) in self.world.get_components(ModelRef, ComponentGuiStaticText, Dirty):
            if component.key == "welcomemsg":
                print("render static text for", ent)
                gui.ref.SetLabel(component.finalstr)

        msg = {}  # can't target how model ref components get found, so build up what we need here
        for ent, (component, guist, _) in self.world.get_components(MultiModelRef, ComponentGuiStaticText, Dirty):
            for model_ref in component.refs:
                msg[model_ref.key] = model_ref.finalstr
            guist.ref.SetLabel(f"{msg['welcomemsg']} {msg['firstname']} {msg['surname']}")
            print("render staticText for", ent)

        for ent, (component, gui, _) in self.world.get_components(ModelRef, ComponentGuiTextControl, Dirty):
            print("render textctrl for", ent)
            gui.ref.SetValue(component.finalstr)

        do.dirty_all(False, entities=mediators)


class HousekeepingProcessor(esper.Processor):
    def process(self):
        print("--Housekeeping System--")

        if frame.m_checkBox1.IsChecked():
            frame.m_checkBox1A.Disable()
        else:
            frame.m_checkBox1A.Enable()


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


def model_setter_welcome(msg):
    model["welcomemsg"] = msg
    model_welcome_toggle()


def model_welcome_toggle():
    model["welcomemsg"] = model["welcomemsg"].upper() if frame.m_checkBox1.IsChecked() else model["welcomemsg"].lower()


#
# Frame with GUI events
#


class MyFrame1A(MyFrame1):
    def on_button_reset_welcome(self, event):
        model_setter_welcome("Hello")  # so that welcome uppercase toggle is respected
        do.dirty(ModelRef, lambda component : component.key == "welcomemsg", filter_nice_name="welcomemsg")
        do.dirty(MultiModelRef)
        world.process()

    def on_button_reset_user(self, event):
        model["user"]["firstname"] = "Fred"
        model["user"]["surname"] = "Flinstone"
        do.dirty(ModelRef)
        do.dirty(MultiModelRef)
        world.process()

    def on_check_welcome_model(self, event):
        # toggle the case of the model's welcome message
        model_welcome_toggle()
        do.dirty(ModelRef, lambda component : component.key == "welcomemsg", filter_nice_name="welcomemsg")
        do.dirty(MultiModelRef)
        world.process()

    def on_check_toggle_welcome_outputs_only(self, event):
        # toggle the case of the welcome output messages only - do not affect model
        add_or_remove_component(
            world,
            condition=frame.m_checkBox1A.IsChecked(),
            component_Class=ComponentUppercaseWelcome,
            entities=[entity_welcome_left, entity_welcome_user_right],
        )
        do.dirty("welcome display only, not via model")  # doesn't affect welcome text edit field
        world.process()

    def on_check_upper_entire_top_right_output(self, event):
        # don't change the model - only the UI display
        add_or_remove_component(world, 
                                condition=frame.m_checkBox2.IsChecked(), 
                                component_Class=ComponentUppercaseAll, entities=[entity_welcome_user_right])
        do.dirty("just top right")
        world.process()

    def on_enter_welcome(self, event):
        model["welcomemsg"] = frame.m_textCtrl1.GetValue()
        do.dirty(ModelRef, lambda component : component.key == "welcomemsg", filter_nice_name="welcomemsg")
        do.dirty(MultiModelRef)
        world.process()

    def on_enter_user_firstname(self, event):
        model["user"]["firstname"] = frame.m_textCtrl2.GetValue()
        do.dirty(ModelRef, lambda component : component.key == "firstname", filter_nice_name="firstname")
        do.dirty(MultiModelRef)
        world.process()

    def on_enter_user_surname(self, event):
        model["user"]["surname"] = frame.m_textCtrl3.GetValue()
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
frame.Show()
frame.SetSize((500, 400))

#
# Wire up and build everything
#

world = esper.World()
world.add_processor(ModelExtractProcessor())
world.add_processor(CaseTransformProcessor())
world.add_processor(RenderProcessor())
world.add_processor(HousekeepingProcessor())
world.add_processor(FunProcessor())

entity_welcome_left = world.create_entity(
    ModelRef(model=model, key="welcomemsg"), ComponentGuiStaticText(ref=frame.m_staticText1)
)

entity_welcome_user_right = world.create_entity(
    MultiModelRef(refs=[
        ModelRef(model=model, key="welcomemsg"),
        ModelRef(model=model["user"], key="firstname"),
        ModelRef(model=model["user"], key="surname"),
        ]),
    ComponentGuiStaticText(ref=frame.m_staticText2),
)

entity_edit_welcome_msg = world.create_entity(
    ModelRef(model=model, key="welcomemsg"), ComponentGuiTextControl(ref=frame.m_textCtrl1)
)
entity_edit_user_name_msg = world.create_entity(
    ModelRef(model=model["user"], key="firstname"), ComponentGuiTextControl(ref=frame.m_textCtrl2)
)
entity_edit_user_surname_msg = world.create_entity(
    ModelRef(model=model["user"], key="surname"), ComponentGuiTextControl(ref=frame.m_textCtrl3)
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
    appgui: "mediator for app frame etc",
}
mediators: List[int] = list(nice_entity_name.keys())

# Observer Wiring
do = DirtyObserver(world)

do.add_dependency(ModelRef, [entity_welcome_left, entity_edit_welcome_msg, entity_edit_user_name_msg, entity_edit_user_surname_msg])
do.add_dependency(MultiModelRef, [entity_welcome_user_right])
do.add_dependency("welcome display only, not via model", [entity_welcome_left, entity_welcome_user_right])
do.add_dependency("just top right", [entity_welcome_user_right])

do.dirty_all(entities=mediators)  # initialise the gui with initial model values
world.process()

app.MainLoop()
