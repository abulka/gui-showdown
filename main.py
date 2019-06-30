import wx
from gui import MyFrame1  #  <--- the wxformbuilder generated python module
import esper
import time
from dataclasses import dataclass
from typing import List
from esper_extras import add_or_remove_component
from esper_observer import DirtyObserver, Dirty

model = {
    "welcome_msg": "Welcome",
    "user": {
        "name": "Sam",
        "surname": "Smith",
    }
}

# Not used - but would be nice to integrate something like this into the ECS
view_model = {
    "uppercase welcome model": False,
    "uppercase welcome outputs": False,
    "uppercase top right": False,
}

@dataclass
class ModelRef:  # Mediator (entity + this component) needs to know about model. Model specific
    model: dict
    key: str
    finalstr: str = ""
class ModelWelcome(ModelRef): pass
class ModelFirstname(ModelRef): pass
class ModelSurname(ModelRef): pass

@dataclass
class GuiControlRef:  # Mediator (entity + this component) needs to know about a wxPython gui control
    ref: object
class GuiStaticText(GuiControlRef): pass  # Static Text Gui ref
class GuiTextControl(GuiControlRef): pass  # Text Control Gui ref

@dataclass
class Flag:  # Mediator (entity + this component) might have a flag to indicate some behaviour is wanted
    pass
class UP_R_WHOLE(Flag): pass  # flag to make upper right message uppercase or not
class UP_L_AND_R_WELCOME_ONLY(Flag): pass  # flag to make upper left AND upper right (welcome portion ONLY) message uppercase or not


def dump(component, entity):  # simple logging
    print(f"added {component} to {nice_entity_name[entity]}")


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


def model_welcome_toggle():
        model["welcome_msg"] = model["welcome_msg"].upper() if frame.m_checkBox1.IsChecked() else model["welcome_msg"].lower()

def model_setter_welcome(msg):
        model["welcome_msg"] = msg
        model_welcome_toggle()

class MyFrame1A(MyFrame1):
    def onResetWelcome(self, event):
        model_setter_welcome("Hello")  # so that welcome uppercase toggle is respected
        do.dirty(ModelWelcome)
        world.process()

    def onCheck1(self, event):
        # toggle the case of the model's welcome message
        model_welcome_toggle()
        do.dirty(ModelWelcome)
        world.process()

    def onCheckToggleWelcomeOutputsOnly(self, event):
        # toggle the case of the welcome output messages only - do not affect model
        add_or_remove_component(
            world, 
            condition=frame.m_checkBox1A.IsChecked(), 
            component_Class=UP_L_AND_R_WELCOME_ONLY, 
            entities=[entity_welcome_left, entity_welcome_user_right])
        do.dirty("welcome display only, not via model")  # doesn't affect welcome text edit field
        world.process()

    def onCheck2(self, event):
        # don't change the model - only the UI display
        add_or_remove_component(
            world, 
            condition=frame.m_checkBox2.IsChecked(), 
            component_Class=UP_R_WHOLE, 
            entities=[entity_welcome_user_right])
        do.dirty("just top right")
        world.process()

    def onEnter(self, event):
        model["welcome_msg"] = frame.m_textCtrl1.GetValue()
        do.dirty(ModelWelcome)
        world.process()

    def onClickResetUser( self, event ):
        model["user"]["name"] = "Fred"
        model["user"]["surname"] = "Flinstone"
        do.dirty(ModelFirstname)
        do.dirty(ModelSurname)
        world.process()

    def onEnterUserName( self, event ):
        model["user"]["name"] = frame.m_textCtrl2.GetValue()
        do.dirty(ModelFirstname)
        world.process()

    def onEnterUserSurname( self, event ):
        model["user"]["surname"] = frame.m_textCtrl3.GetValue()
        do.dirty(ModelSurname)
        world.process()

    def onClickRenderNow( self, event ):
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

entity_welcome_left = world.create_entity()
entity_welcome_user_right = world.create_entity()
entity_edit_welcome_msg = world.create_entity()
entity_edit_user_name_msg = world.create_entity()
entity_edit_user_surname_msg = world.create_entity()

nice_entity_name = {
    entity_welcome_left: "mediator for welcome_left",
    entity_welcome_user_right: "mediator for welcome_user_right",
    entity_edit_welcome_msg: "mediator for edit_welcome_msg",
    entity_edit_user_name_msg: "mediator for edit_user_name_msg",
    entity_edit_user_surname_msg: "mediator for edit_user_surname_msg",
}
mediators: List[int] = list(nice_entity_name.keys())

world.add_component(entity_welcome_left, ModelWelcome(model=model, key="welcome_msg"))
world.add_component(entity_welcome_left, GuiStaticText(ref=frame.m_staticText1))

world.add_component(entity_welcome_user_right, ModelWelcome(model=model, key="welcome_msg"))
world.add_component(entity_welcome_user_right, ModelFirstname(model=model["user"], key="name"))
world.add_component(entity_welcome_user_right, ModelSurname(model=model["user"], key="surname"))
world.add_component(entity_welcome_user_right, GuiStaticText(ref=frame.m_staticText2))

world.add_component(entity_edit_welcome_msg, ModelWelcome(model=model, key="welcome_msg"))
world.add_component(entity_edit_welcome_msg, GuiTextControl(ref=frame.m_textCtrl1))

world.add_component(entity_edit_user_name_msg, ModelFirstname(model=model["user"], key="name"))
world.add_component(entity_edit_user_name_msg, GuiTextControl(ref=frame.m_textCtrl2))

world.add_component(entity_edit_user_surname_msg, ModelSurname(model=model["user"], key="surname"))
world.add_component(entity_edit_user_surname_msg, GuiTextControl(ref=frame.m_textCtrl3))

do = DirtyObserver(world)
do.add_dependency(ModelWelcome, [entity_welcome_left, entity_welcome_user_right, entity_edit_welcome_msg])
do.add_dependency(ModelFirstname, [entity_welcome_user_right, entity_edit_user_name_msg])
do.add_dependency(ModelSurname, [entity_welcome_user_right, entity_edit_user_surname_msg])
do.add_dependency("welcome display only, not via model", [entity_welcome_left, entity_welcome_user_right])
do.add_dependency("just top right", [entity_welcome_user_right])

do.dirty_all(entities=mediators)    
world.process()

app.MainLoop()
