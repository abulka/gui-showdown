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

@dataclass
class Dirty:  # Mark that component needs rendering
    pass 

@dataclass
class MW:  # Welcome model ref
    model: dict
    key: str

@dataclass
class MU:  # User model ref
    model: dict
    key: str

@dataclass
class GUIST:  # Static Text Gui ref
    ref: object

@dataclass
class GUITC:  # Text Control Gui ref
    ref: object

# @dataclass
# class CALC:  # some sort of calc between two model refs or a model ref and a str or something
#     ops: list

class RenderProcessor(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        print("RENDER")
        ents = set()

        for ent, (mw, guist, d) in self.world.get_components(MW, GUIST, Dirty):
            # This loop picks up entities who also have MU !! yikes.
            print("mw top left", ent)
            guist.ref.SetLabel(mw.model[mw.key])
            ents.add(ent)

        for ent, (mw, guitc, d) in self.world.get_components(MW, GUITC, Dirty):
            print("mw textctrl")
            guitc.ref.SetValue(mw.model[mw.key])
            ents.add(ent)

        for ent, (mw, mu, guist, d) in self.world.get_components(MW, MU, GUIST, Dirty):
            print("mw mu top right")
            guist.ref.SetLabel(f"{mw.model[mw.key]} {mu.model[mu.key]}")
            ents.add(ent)

        for ent, (mu, guitc, d) in self.world.get_components(MU, GUITC, Dirty):
            print("mu textctrl")
            guitc.ref.SetValue(mu.model[mu.key])
            ents.add(ent)

        for ent in list(ents):
            world.remove_component(ent, Dirty)

class MyFrame1A(MyFrame1):
    def onButton1(self, event):
        model["welcome_msg"] = "Hi"
        dirty_all()
        world.process()

    def onCheck1(self, event):
        model["welcome_msg"] = model["welcome_msg"].upper() if frame.m_checkBox1.IsChecked() else model["welcome_msg"].lower()
        dirty(MW)
        world.process()

    def onEnter(self, event):
        model["welcome_msg"] = frame.m_textCtrl1.GetValue()
        dirty_all()
        world.process()

    def onClickResetUser( self, event ):
        model["user"]["name"] = "Fred"
        model["user"]["surname"] = "Flinstone"
        dirty(MU)
        world.process()

    def onClickRenderNow( self, event ):
        world.process()


world = esper.World()
world.add_processor(RenderProcessor())


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

world.add_component(entity_welcome_left, MW(model=model, key="welcome_msg"))
world.add_component(entity_welcome_left, GUIST(ref=frame.m_staticText1))

world.add_component(entity_welcome_user_right, MW(model=model, key="welcome_msg"))
world.add_component(entity_welcome_user_right, MU(model=model["user"], key="name"))
world.add_component(entity_welcome_user_right, GUIST(ref=frame.m_staticText2))

world.add_component(entity_edit_welcome_msg, MW(model=model, key="welcome_msg"))
world.add_component(entity_edit_welcome_msg, GUITC(ref=frame.m_textCtrl1))

world.add_component(entity_edit_user_name_msg, MU(model=model["user"], key="name"))
world.add_component(entity_edit_user_name_msg, GUITC(ref=frame.m_textCtrl2))


# Tells us which model each mediator entity cares about, like observer pattern mappings.
# Note this uses the model component ref class, rather than anything about the model dict itself
# THOUGHT: we could even have arbitrary keys which are more verbose model descriptions
dirty_model_to_entities = {
    MW: [entity_welcome_left, entity_welcome_user_right],
    MU: [entity_welcome_user_right, entity_edit_user_name_msg],
}

def dirty_all():
    for e in mediators:
        world.add_component(e, Dirty())

def dirty(component_class):
    for mediator in dirty_model_to_entities[component_class]:
        print(f"dirty: {mediator} because {component_class}")
        world.add_component(mediator, Dirty())

dirty_all()    
world.process()

app.MainLoop()
