import wx
from gui import MyFrame1  #  <--- the wxformbuilder generated python module
import esper
import time
from dataclasses import dataclass

model = {
    "welcome_msg": "Hi",
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
class Dirty:  # Mark that component needs rendering
    pass 

@dataclass
class ModelWelcome:  # Welcome model ref
    model: dict
    key: str

@dataclass
class ModelFirstname:  # User model ref
    model: dict
    key: str

@dataclass
class ModelSurname:  # User surname model ref
    model: dict
    key: str

@dataclass
class GuiStaticText:  # Static Text Gui ref
    ref: object

@dataclass
class GuiTextControl:  # Text Control Gui ref
    ref: object

@dataclass
class UP_R_WHOLE:  # flag to make upper right message uppercase or not
    pass

@dataclass
class UP_L_AND_R_WELCOME_ONLY:  # flag to make upper left AND upper right (welcome portion ONLY) message uppercase or not
    pass

@dataclass
class FinalWelcome:
    s: str

@dataclass
class FinalFirstname:
    s: str

@dataclass
class FinalSurname:
    s: str


class ModelExtractProcessor(esper.Processor):
    """
    Extract info from models and stage them in Final* components, so that the transform phase
    can alter them without altering the model.  This will allow for multiple transformations and
    is decoupled from the final output/rendering system stage.
    """
    def process(self):
        print("--Model Extract System---")
        for ent, (mw, d) in self.world.get_components(ModelWelcome, Dirty):
            f = FinalWelcome(s=mw.model[mw.key])
            world.add_component(ent, f)
            dump(f, ent)

        for ent, (mu, d) in self.world.get_components(ModelFirstname, Dirty):
            f = FinalFirstname(s=mu.model[mu.key])
            world.add_component(ent, f)
            dump(f, ent)

        for ent, (mus, d) in self.world.get_components(ModelSurname, Dirty):
            f = FinalSurname(s=mus.model[mus.key])
            world.add_component(ent, f)
            dump(f, ent)


class CaseTransformProcessor(esper.Processor):
    def process(self):
        print("--Case transform System---")
        def up(ent, f):
            f.s = f.s.upper()
            dump(f, ent)
        for ent, (f, uprw, d) in self.world.get_components(FinalWelcome, UP_L_AND_R_WELCOME_ONLY, Dirty):
            up(ent, f)
        for ent, (f, upr, d) in self.world.get_components(FinalWelcome, UP_R_WHOLE, Dirty):
            up(ent, f)
        for ent, (f, upr, d) in self.world.get_components(FinalFirstname, UP_R_WHOLE, Dirty):
            up(ent, f)
        for ent, (f, upr, d) in self.world.get_components(FinalSurname, UP_R_WHOLE, Dirty):
            up(ent, f)


class RenderProcessor(esper.Processor):
    def process(self):
        print("--Render System--")
        ents = set()

        for ent, (finalw, guist, d) in self.world.get_components(FinalWelcome, GuiStaticText, Dirty):
            print("top left", ent)
            guist.ref.SetLabel(finalw.s)
            ents.add(ent)
        for ent, (finalw, finalf, finals, guist, d) in self.world.get_components(FinalWelcome, FinalFirstname, FinalSurname, GuiStaticText, Dirty):
            print("top right")
            guist.ref.SetLabel(f"{finalw.s} {finalf.s} {finals.s}")
            ents.add(ent)
        for ent, (f, guitc, d) in self.world.get_components(FinalWelcome, GuiTextControl, Dirty):
            print("mw textctrl")
            guitc.ref.SetValue(f.s)
            ents.add(ent)
        # wish we didn't have two loops
        for ent, (f, guitc, d) in self.world.get_components(FinalFirstname, GuiTextControl, Dirty):
            print("mu textctrl (name)")
            guitc.ref.SetValue(f.s)
            ents.add(ent)
        for ent, (f, guitc, d) in self.world.get_components(FinalSurname, GuiTextControl, Dirty):
            print("mu textctrl (surname)")
            guitc.ref.SetValue(f.s)
            ents.add(ent)

        for ent in list(ents):
            if world.has_component(ent, UP_R_WHOLE):
                world.remove_component(ent, UP_R_WHOLE)
            if world.has_component(ent, UP_L_AND_R_WELCOME_ONLY):
                world.remove_component(ent, UP_L_AND_R_WELCOME_ONLY)
            world.remove_component(ent, Dirty)

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
        dirty(ModelWelcome)
        world.process()

    def onCheck1(self, event):
        # toggle the case of the model's welcome message
        model_welcome_toggle()
        dirty(ModelWelcome)
        world.process()

    def onCheckToggleWelcomeOutputsOnly(self, event):
        # toggle the case of the welcome output messages only - do not affect model
        if frame.m_checkBox1A.IsChecked():
            world.add_component(entity_welcome_left, UP_L_AND_R_WELCOME_ONLY())
            world.add_component(entity_welcome_user_right, UP_L_AND_R_WELCOME_ONLY())
        else:
            if world.has_component(entity_welcome_left, UP_L_AND_R_WELCOME_ONLY):
                world.remove_component(entity_welcome_left, UP_L_AND_R_WELCOME_ONLY)
            if world.has_component(entity_welcome_user_right, UP_L_AND_R_WELCOME_ONLY):
                world.remove_component(entity_welcome_user_right, UP_L_AND_R_WELCOME_ONLY)
        dirty("welcome outputs only")  # doesn't affect welcome edit field
        world.process()

    def onCheck2(self, event):
        # don't change the model - only the UI display
        # how do we tell the 'system' logic to do this?  need a flag or an extra component
        # looks like its going to be an extra component. Pity - that's inefficient and complex.
        #
        # perhaps we need a two pass render which converts model info to plain info then the uppercase/lowercase
        # can further act on that plain info before rendering.
        e = entity_welcome_user_right
        if frame.m_checkBox2.IsChecked():
            world.add_component(e, UP_R_WHOLE())
        else:
            if world.has_component(e, UP_R_WHOLE):
                world.remove_component(e, UP_R_WHOLE)
        dirty("just top right")
        world.process()

    def onEnter(self, event):
        model["welcome_msg"] = frame.m_textCtrl1.GetValue()
        dirty(ModelWelcome)
        world.process()

    def onClickResetUser( self, event ):
        model["user"]["name"] = "Fred"
        model["user"]["surname"] = "Flinstone"
        dirty(ModelFirstname)
        dirty(ModelSurname)
        world.process()

    def onEnterUserName( self, event ):
        model["user"]["name"] = frame.m_textCtrl2.GetValue()
        dirty(ModelFirstname)
        world.process()

    def onEnterUserSurname( self, event ):
        model["user"]["surname"] = frame.m_textCtrl3.GetValue()
        dirty(ModelSurname)
        world.process()

    def onClickRenderNow( self, event ):
        world.process()


world = esper.World()
world.add_processor(ModelExtractProcessor())
world.add_processor(CaseTransformProcessor())
world.add_processor(RenderProcessor())
world.add_processor(HousekeepingProcessor())


app = wx.App()
frame = MyFrame1A(None)
frame.Show()
frame.SetSize((400, 400))

entity_welcome_left = world.create_entity()
entity_welcome_user_right = world.create_entity()
entity_edit_welcome_msg = world.create_entity()
entity_edit_user_name_msg = world.create_entity()
entity_edit_user_surname_msg = world.create_entity()

mediators = [entity_welcome_left,
            entity_welcome_user_right,
            entity_edit_welcome_msg,
            entity_edit_user_name_msg,
            entity_edit_user_surname_msg,
            ]

nice_entity_name = {  # can't we get esper to give us this info?
    1: "entity_welcome_left",
    2: "entity_welcome_user_right",
    3: "entity_edit_welcome_msg",
    4: "entity_edit_user_name_msg",
    5: "entity_edit_user_surname_msg",
}

def dump(component, entity):
    print(f"added {component} to {nice_entity_name[entity]}")
 
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


# Tells us which model each mediator entity cares about, like observer pattern mappings.
# Note this uses the model component ref class, rather than anything about the model dict itself
# We even have arbitrary keys which are more verbose model descriptions to make it easier
dirty_model_to_entities = {
    ModelWelcome: [entity_welcome_left, entity_welcome_user_right, entity_edit_welcome_msg],
    "welcome outputs only": [entity_welcome_left, entity_welcome_user_right],
    ModelFirstname: [entity_welcome_user_right, entity_edit_user_name_msg],
    ModelSurname: [entity_welcome_user_right, entity_edit_user_surname_msg],
    "just top right": [entity_welcome_user_right],
}

def dirty_all():
    for e in mediators:
        world.add_component(e, Dirty())

def dirty(component_class):
    # dirty_all()
    # return
    for mediator in dirty_model_to_entities[component_class]:
        print(f"dirty: {mediator} because {component_class}")
        world.add_component(mediator, Dirty())

dirty_all()    
world.process()

app.MainLoop()
