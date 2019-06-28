import wx
from gui import MyFrame1  #  <--- the wxformbuilder generated python module
import esper
import time
from dataclasses import dataclass

model = {
    "welcome_msg": "Hi",
    "user": {
        "name": "Andy",
        "surname": "",
    }
}

# @dataclass
# class Dirty:
#     pass  # Mark that component needs rendering

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
        for ent, (mw, guist) in self.world.get_components(MW, GUIST):
            guist.ref.SetLabel(mw.model[mw.key])
        for ent, (mw, guitc) in self.world.get_components(MW, GUITC):
            guitc.ref.SetValue(mw.model[mw.key])
        for ent, (mw, mu, guist) in self.world.get_components(MW, MU, GUIST):
            guist.ref.SetLabel(f"{mw.model[mw.key]} {mu.model[mu.key]}")

class MyFrame1A(MyFrame1):
    def onButton1(self, event):
        model["welcome_msg"] = "Hi"
        world.process()

    def onCheck1(self, event):
        model["welcome_msg"] = model["welcome_msg"].upper() if frame.m_checkBox1.IsChecked() else model["welcome_msg"].lower()
        world.process()

    def onEnter(self, event):
        model["welcome_msg"] = frame.m_textCtrl1.GetValue()
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

world.add_component(entity_welcome_left, MW(model=model, key="welcome_msg"))
world.add_component(entity_welcome_left, GUIST(ref=frame.m_staticText1))

world.add_component(entity_welcome_user_right, MW(model=model, key="welcome_msg"))
world.add_component(entity_welcome_user_right, MU(model=model["user"], key="name"))
world.add_component(entity_welcome_user_right, GUIST(ref=frame.m_staticText2))

world.add_component(entity_edit_welcome_msg, MW(model=model, key="welcome_msg"))
world.add_component(entity_edit_welcome_msg, GUITC(ref=frame.m_textCtrl1))

world.process()

app.MainLoop()
