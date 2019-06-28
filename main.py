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

@dataclass
class Info:
    model: dict
    colour: str = ""
    font: str = ""

@dataclass
class Dirty:
    pass  # Mark that component needs rendering


class RenderProcessor(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        print("RENDER")
        # for ent, (info, dirty) in self.world.get_components(Info, Dirty):
        #     # print(f"entity {ent} says {render.info}")
        #     frame.m_staticText1.SetLabel(info.model["welcome_msg"])
        #     frame.m_staticText2.SetLabel(info.model["user"]["name"] + " " + info.model["welcome_msg"])
        #     frame.m_textCtrl1.SetValue(info.model["welcome_msg"])            
        #     world.remove_component(ent, Dirty)
        for ent, (info,) in self.world.get_components(Info):
            frame.m_staticText1.SetLabel(info.model["welcome_msg"])
            frame.m_staticText2.SetLabel(info.model["user"]["name"] + " " + info.model["welcome_msg"])
            frame.m_textCtrl1.SetValue(info.model["welcome_msg"])

class MyFrame1A(MyFrame1):
    def onButton1(self, event):
        model["welcome_msg"] = "Hi"
        # w = world.component_for_entity(model_welcome, Info)
        # w.info = "Hi"
        # world.add_component(model_welcome, Dirty())
        world.process()

    def onCheck1( self, event):
        # i = world.component_for_entity(model_welcome, Info)
        # if frame.m_checkBox1.IsChecked():
        #     i.info = i.info.upper()
        # else:
        #     i.info = i.info.lower()
        # world.add_component(model_welcome, Dirty())
        if frame.m_checkBox1.IsChecked():
            model["welcome_msg"] = model["welcome_msg"].upper()
        else:
            model["welcome_msg"] = model["welcome_msg"].lower()
        world.process()


# def setup_esper():
world = esper.World()
world.add_processor(RenderProcessor())

"""
We want to model:
    - a welcome message, default "Hi"
    - a user, default "Andy", cannot change
The GUI displays:
    - the welcome message twice
        - top left: pure message
        - top right: message + user
    - text entry, which allows editing of the welcome message
    - checkbox, which converts top right message to uppercase
    - button, which resets the welcome message to "Hi"
"""


entity_welcome_left = world.create_entity()
entity_welcome_user_right = world.create_entity()
entity_edit_welcome_msg = world.create_entity()
# entity_case_change = world.create_entity()
# entity_reset_welcome_button = world.create_entity()

world.add_component(entity_welcome_left, Info(model=model, colour="red"))
world.add_component(entity_welcome_user_right, Info(model=model))
world.add_component(entity_edit_welcome_msg, Info(model=model))

world.add_component(entity_welcome_left, Dirty())
world.add_component(entity_welcome_user_right, Dirty())
world.add_component(entity_edit_welcome_msg, Dirty())

# setup_esper()

app = wx.App()
frame = MyFrame1A(None)
frame.Show()
frame.SetSize((400, 400))

world.process()

app.MainLoop()
