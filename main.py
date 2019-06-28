import wx
from gui import MyFrame1  #  <--- the wxformbuilder generated python module
import esper
import time
from dataclasses import dataclass


@dataclass
class Render:
    """Class for rendering."""

    info: str = ""


@dataclass
class Dirty:
    """Mark that component needs rendering."""


class RenderProcessor(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        print("RENDER")
        for ent, (render, dirty) in self.world.get_components(Render, Dirty):
            print(f"entity {ent} says {render.info}")
            frame.m_staticText1.SetLabel(render.info)
            frame.m_textCtrl1.SetValue(render.info)
            
            world.remove_component(ent, Dirty)

class MyFrame1A(MyFrame1):
    def onButton1(self, event):
        # global world

        print("button pushed")

        i = world.component_for_entity(gui_title, Render)
        i.info = "hi there"
        world.add_component(gui_title, Dirty())
        world.process()

    def onCheck1( self, event):
        print("checked event")
        i = world.component_for_entity(gui_title, Render)
        if frame.m_checkBox1.IsChecked():
            i.info = i.info.upper()
        else:
            i.info = i.info.lower()
        world.add_component(gui_title, Dirty())
        world.process()


# def setup_esper():
world = esper.World()
world.add_processor(RenderProcessor())

gui_title = world.create_entity()
gui_textentry = world.create_entity()
gui_checkbox = world.create_entity()
gui_button1 = world.create_entity()

world.add_component(gui_title, Render(info="hmm"))
world.add_component(gui_title, Dirty())

# setup_esper()

app = wx.App()
frame = MyFrame1A(None)
frame.Show()
frame.SetSize((400, 400))

world.process()

app.MainLoop()
