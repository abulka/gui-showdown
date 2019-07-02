import wx
from gui import MyFrame1  #  <--- the wxformbuilder generated python module
import esper
import time
import random
from dataclasses import dataclass
from typing import List, Any
from esper_extras import add_or_remove_component
from esper_observer import DirtyObserver, Dirty

# The only reason we have a deep model like this, is because it is shared and manipulated by
# many things.  Other 'model' data bits can be put into components directly as a sole place.
model = {"welcome_msg": "Welcome", "user": {"name": "Sam", "surname": "Smith"}}


@dataclass
class ModelRef:  # Mediator (entity + this component) needs to know about model. Model specific
    model: dict
    key: str
    finalstr: str = ""


class ModelWelcome(ModelRef):
    pass


class ModelFirstname(ModelRef):
    pass


class ModelSurname(ModelRef):
    pass


@dataclass
class GuiControlRef:  # Mediator (entity + this component) needs to know about a wxPython gui control
    ref: object


class GuiStaticText(GuiControlRef):
    pass  # Static Text Gui ref


class GuiTextControl(GuiControlRef):
    pass  # Text Control Gui ref


@dataclass
class Flag:  # Mediator (entity + this component) might have a flag to indicate some behaviour is wanted
    pass


class UP_R_WHOLE(Flag):
    pass  # flag to make upper right message uppercase or not


class UP_L_AND_R_WELCOME_ONLY(Flag):
    pass  # flag to make upper left AND upper right (welcome portion ONLY) message uppercase or not


@dataclass
class FrameAdornments:
    frame_title: str = ""
    frame_ref: Any = None
    panel_colour: Any = None
    panel_ref: Any = None
    panel_colour_randomise: bool = False


class ModelExtractProcessor(esper.Processor):
    """
    Extract info from models and stage them in the component in 'finalstr', so that the transform phase
    can alter that info without altering the model.  This makes use of multiple 'system' transformations e.g.
    and decouples transformation from the final output/rendering system stage.
    """

    def process(self):
        print("--Model Extract System---")
        for Component in (ModelWelcome, ModelFirstname, ModelSurname):
            for ent, (component, _) in self.world.get_components(Component, Dirty):
                component.finalstr = component.model[component.key]
                dump(component, ent)


class CaseTransformProcessor(esper.Processor):
    def process(self):
        print("--Case transform System---")

        for Component in (ModelWelcome,):
            for ent, (component, _, _) in self.world.get_components(Component, UP_L_AND_R_WELCOME_ONLY, Dirty):
                component.finalstr = component.finalstr.upper()
                dump(component, ent)
        for Component in (ModelWelcome, ModelFirstname, ModelSurname):
            for ent, (component, _, _) in self.world.get_components(Component, UP_R_WHOLE, Dirty):
                component.finalstr = component.finalstr.upper()
                dump(component, ent)


class RenderProcessor(esper.Processor):
    def process(self):
        print("--Render System--")

        def render_text_control(Component):
            for ent, (component, gui, _) in self.world.get_components(Component, GuiTextControl, Dirty):
                print("render textctrl for", component, ent)
                gui.ref.SetValue(component.finalstr)

        def render_static_text(Component):
            for ent, (component, gui, _) in self.world.get_components(Component, GuiStaticText, Dirty):
                print("render static text for", component, ent)
                gui.ref.SetLabel(component.finalstr)

        render_static_text(ModelWelcome)

        for ent, (mw, mf, ms, guist, _) in self.world.get_components(ModelWelcome, ModelFirstname, ModelSurname, GuiStaticText, Dirty):
            print("top right", ent)
            guist.ref.SetLabel(f"{mw.finalstr} {mf.finalstr} {ms.finalstr}")

        for Component in (ModelWelcome, ModelFirstname, ModelSurname):
            render_text_control(Component)

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

        for _, (f,) in self.world.get_components(FrameAdornments):
            f.frame_ref.SetTitle(f.frame_title + " " + time.asctime())
            f.panel_ref.SetBackgroundColour(
                wx.Colour(255, random.randint(120, 250), random.randint(120, 250)) if f.panel_colour_randomise else f.panel_colour
            )
            f.panel_ref.Refresh()  # f.panel_ref.Update() doesn't work, need to Refresh()


# Not used - but would be nice to integrate something like this into the ECS
# but then again, the data components attached to a mediator entity is like a view model, so
# why replicate that information uncessessarily.
view_model = {"uppercase welcome model": False, "uppercase welcome outputs": False, "uppercase top right": False}


def dump(component, entity):  # simple logging
    print(f"have set {component} for {nice_entity_name[entity]}")


def model_setter_welcome(msg):
    model["welcome_msg"] = msg
    model_welcome_toggle()


def model_welcome_toggle():
    model["welcome_msg"] = model["welcome_msg"].upper() if frame.m_checkBox1.IsChecked() else model["welcome_msg"].lower()


# Frame
class MyFrame1A(MyFrame1):
    def on_button_reset_welcome(self, event):
        model_setter_welcome("Hello")  # so that welcome uppercase toggle is respected
        do.dirty(ModelWelcome)
        world.process()

    def on_button_reset_user(self, event):
        model["user"]["name"] = "Fred"
        model["user"]["surname"] = "Flinstone"
        do.dirty(ModelFirstname)
        do.dirty(ModelSurname)
        world.process()

    def on_check_welcome_model(self, event):
        # toggle the case of the model's welcome message
        model_welcome_toggle()
        do.dirty(ModelWelcome)
        world.process()

    def on_check_toggle_welcome_outputs_only(self, event):
        # toggle the case of the welcome output messages only - do not affect model
        add_or_remove_component(
            world,
            condition=frame.m_checkBox1A.IsChecked(),
            component_Class=UP_L_AND_R_WELCOME_ONLY,
            entities=[entity_welcome_left, entity_welcome_user_right],
        )
        do.dirty("welcome display only, not via model")  # doesn't affect welcome text edit field
        world.process()

    def on_check_upper_entire_top_right_output(self, event):
        # don't change the model - only the UI display
        add_or_remove_component(
            world, condition=frame.m_checkBox2.IsChecked(), component_Class=UP_R_WHOLE, entities=[entity_welcome_user_right]
        )
        do.dirty("just top right")
        world.process()

    def on_enter_welcome(self, event):
        model["welcome_msg"] = frame.m_textCtrl1.GetValue()
        do.dirty(ModelWelcome)
        world.process()

    def on_enter_user_firstname(self, event):
        model["user"]["name"] = frame.m_textCtrl2.GetValue()
        do.dirty(ModelFirstname)
        world.process()

    def on_enter_user_surname(self, event):
        model["user"]["surname"] = frame.m_textCtrl3.GetValue()
        do.dirty(ModelSurname)
        world.process()

    def onClickRenderNow(self, event):
        world.process()


app = wx.App()
frame = MyFrame1A(None)
frame.Show()
frame.SetSize((500, 400))

world = esper.World()
world.add_processor(ModelExtractProcessor())
world.add_processor(CaseTransformProcessor())
world.add_processor(RenderProcessor())
world.add_processor(HousekeepingProcessor())
world.add_processor(FunProcessor())

entity_welcome_left = world.create_entity(ModelWelcome(model=model, key="welcome_msg"), GuiStaticText(ref=frame.m_staticText1))
entity_welcome_user_right = world.create_entity(
    ModelWelcome(model=model, key="welcome_msg"),
    ModelFirstname(model=model["user"], key="name"),
    ModelSurname(model=model["user"], key="surname"),
    GuiStaticText(ref=frame.m_staticText2),
)
entity_edit_welcome_msg = world.create_entity(ModelWelcome(model=model, key="welcome_msg"), GuiTextControl(ref=frame.m_textCtrl1))
entity_edit_user_name_msg = world.create_entity(ModelFirstname(model=model["user"], key="name"), GuiTextControl(ref=frame.m_textCtrl2))
entity_edit_user_surname_msg = world.create_entity(ModelSurname(model=model["user"], key="surname"), GuiTextControl(ref=frame.m_textCtrl3))
appgui = world.create_entity()  # slightly different style, create entiry then add components
world.add_component(
    appgui,
    FrameAdornments(
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
do.add_dependency(ModelWelcome, [entity_welcome_left, entity_welcome_user_right, entity_edit_welcome_msg])
do.add_dependency(ModelFirstname, [entity_welcome_user_right, entity_edit_user_name_msg])
do.add_dependency(ModelSurname, [entity_welcome_user_right, entity_edit_user_surname_msg])
do.add_dependency("welcome display only, not via model", [entity_welcome_left, entity_welcome_user_right])
do.add_dependency("just top right", [entity_welcome_user_right])

do.dirty_all(entities=mediators)  # initialise the gui with initial model values
world.process()

app.MainLoop()
