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

class MyFrame1A(MyFrame1):
    def onButton1(self, event):
        # global world

        print("button pushed")

        i = world.component_for_entity(gui_title, Render)
        i.info = "hi there"

        world.process()


    # def OnHtml2(self, event):
    #     url = "http://www.wxpython.org/docs/api/wx.html.HtmlWindow-class.html"
    #     wx.CallAfter(frame.m_htmlWin1.LoadPage, url)
    #
    # def OnLoadHtml1(self, event):
    #     url = "http://help.websiteos.com/websiteos/example_of_a_simple_html_page.htm"
    #     wx.CallAfter(frame.m_htmlWin1.LoadPage, url)
    # frame.m_htmlWin1.LoadPage(url)

# def setup_esper():
world = esper.World()
world.add_processor(RenderProcessor())

gui_title = world.create_entity()
gui_textentry = world.create_entity()
gui_checkbox = world.create_entity()
gui_button1 = world.create_entity()

world.add_component(gui_title, Render())
world.add_component(gui_title, Dirty())

# setup_esper()

app = wx.App()
frame = MyFrame1A(None)
frame.Show()
frame.SetSize((400, 400))

app.MainLoop()
