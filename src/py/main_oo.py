import wx
from gui import MyFrame1  #  <--- the wxformbuilder generated python module
import time
import random
from dataclasses import dataclass, astuple
from typing import List, Any
from observer_oo import Observable, Observer

#
# Model - The Welcome model and User model are Observable.
#


@dataclass
class BaseModel(Observable):
    def __post_init__(self):
        super().__init__()


@dataclass
class Welcome(BaseModel):
    _msg: str = "Welcome"

    @property
    def message(self) -> str:
        return self._msg

    @message.setter
    def message(self, v: str) -> None:
        self._msg = v
        self.NotifyAll(data=v)


@dataclass
class User(BaseModel):
    _firstname: str = "Sam"
    _surname: str = "Smith"

    @property
    def firstname(self) -> str:
        return self._firstname

    @firstname.setter
    def firstname(self, v: str) -> None:
        self._firstname = v
        self.NotifyAll(data=v)

    @property
    def surname(self) -> str:
        return self._surname

    @surname.setter
    def surname(self, v: str) -> None:
        self._surname = v
        self.NotifyAll(data=v)


@dataclass
class Model:
    """Main model, contains both the welcome model and the user model"""

    welcome: Welcome
    user: User

    def dirty_all(self):
        self.welcome.NotifyAll("dirty_all")
        self.user.NotifyAll("dirty_all")


#
# Mediators - are implemented as Observer classes, contain the behaviour
#


@dataclass
class Mediator(Observer):
    def __post_init__(self):
        super().__init__()

    def __hash__(self):
        return hash(tuple(self))


@dataclass
class MediatorWelcomeLeft(Mediator):
    welcome: Welcome
    gui_ref: wx.StaticText
    _uppercase_welcome: bool = False

    @property
    def uppercase_welcome(self) -> str:
        return self._uppercase_welcome

    @uppercase_welcome.setter
    def uppercase_welcome(self, v: str) -> None:
        self._uppercase_welcome = v
        self.Notify(self, 'display option change')

    def Notify(self, target, data):
        super().Notify(target, data)
        msg = self.welcome.message.upper() if self.uppercase_welcome else self.welcome.message
        self.gui_ref.SetLabel(msg)


@dataclass
class MediatorWelcomeUserRight(Mediator):
    welcome: Welcome
    user: User
    gui_ref: wx.StaticText
    _uppercase_welcome: bool = False
    _uppercase_user: bool = False

    @property
    def uppercase_welcome(self) -> str:
        return self._uppercase_welcome

    @uppercase_welcome.setter
    def uppercase_welcome(self, v: str) -> None:
        self._uppercase_welcome = v
        self.Notify(self, 'display option change')

    @property
    def uppercase_user(self) -> str:
        return self._uppercase_user

    @uppercase_user.setter
    def uppercase_user(self, v: str) -> None:
        self._uppercase_user = v
        self.Notify(self, 'display option change')

    def Notify(self, target, data):
        super().Notify(target, data)
        welcome = self.welcome.message.upper() if self.uppercase_welcome else self.welcome.message
        firstname = self.user.firstname.upper() if self.uppercase_user else self.user.firstname
        surname = self.user.surname.upper() if self.uppercase_user else self.user.surname
        self.gui_ref.SetLabel(f"{welcome} {firstname} {surname}")


@dataclass
class MediatorEditWelcome(Mediator):
    welcome: Welcome
    gui_ref: wx.TextCtrl

    def Notify(self, target, data):
        super().Notify(target, data)
        self.gui_ref.SetValue(self.welcome.message)


@dataclass
class MediatorEditUserFirstName(Mediator):
    user: User
    gui_ref: wx.TextCtrl

    def Notify(self, target, data):
        super().Notify(target, data)
        self.gui_ref.SetValue(self.user.firstname)


@dataclass
class MediatorEditUserSurName(Mediator):
    user: User
    gui_ref: wx.TextCtrl

    def Notify(self, target, data):
        super().Notify(target, data)
        self.gui_ref.SetValue(self.user.surname)


@dataclass
class MediatorFrameAdornments(Mediator):
    frame_title: str
    frame_ref: wx.Frame
    panel_colour: wx.Colour
    panel_ref: wx.Panel
    panel_colour_randomise: bool

    def Notify(self, target, data):
        super().Notify(target, data)
        self.frame_ref.SetTitle(self.frame_title + " " + time.asctime())
        self.panel_ref.SetBackgroundColour(
            wx.Colour(255, random.randint(120, 250), random.randint(120, 250)) if self.panel_colour_randomise else self.panel_colour
        )
        self.panel_ref.Refresh()  # f.panel_ref.Update() doesn't work, need to Refresh()

#
# Util
#

# def housekeeping():
#     if frame.m_checkBox1.IsChecked():
#         frame.m_checkBox1A.Disable()
#     else:
#         frame.m_checkBox1A.Enable()


#
# Frame with GUI events
#


class MyFrame1A(MyFrame1):
    def on_button_reset_welcome(self, event):
        model.welcome.message = "Hello"

    def on_button_reset_user(self, event):
        model.user.firstname = "Fred"
        model.user.surname = "Flinstone"

    def on_button_change_welcome_model_case(self, event):
        s = model.welcome.message
        model.welcome.message = s.upper() if s[1].islower() else s.lower()

    def on_button_change_user_model_case(self, event):
        f = model.user.firstname
        s = model.user.surname
        model.user.firstname = f.upper() if f[1].islower() else f.lower()
        model.user.surname = s.upper() if s[1].islower() else s.lower()

    def on_check_toggle_welcome_outputs_only(self, event):
        mediator_welcome_left.uppercase_welcome = event.GetEventObject().IsChecked()
        mediator_welcome_user_right.uppercase_welcome = event.GetEventObject().IsChecked()

    def on_check_toggle_user_outputs_only(self, event):
        mediator_welcome_user_right.uppercase_user = event.GetEventObject().IsChecked()

    def on_check_upper_entire_top_right_output(self, event):
        mediator_welcome_user_right.uppercase_welcome = event.GetEventObject().IsChecked()
        mediator_welcome_user_right.uppercase_user = event.GetEventObject().IsChecked()

    def on_enter_welcome(self, event):
        model.welcome.message = event.GetEventObject().GetValue()

    def on_enter_user_firstname(self, event):
        model.user.firstname = event.GetEventObject().GetValue()

    def on_enter_user_surname(self, event):
        model.user.surname = event.GetEventObject().GetValue()

    def onClickRenderNow(self, event):
        model.dirty_all()


#
# Init WxPython
#

app = wx.App()
frame = MyFrame1A(None)
frame.SetTitle("Gui wired via OO Observer")
frame.Show()
frame.SetSize((500, 450))

#
# Wire up and build everything
#

model = Model(Welcome(), User())
mediator_welcome_left = MediatorWelcomeLeft(welcome=model.welcome, gui_ref=frame.m_staticText1)
mediator_welcome_user_right = MediatorWelcomeUserRight(welcome=model.welcome, user=model.user, gui_ref=frame.m_staticText2)
mediator_edit_welcome_msg = MediatorEditWelcome(welcome=model.welcome, gui_ref=frame.m_textCtrl1)
mediator_edit_user_firstname_msg = MediatorEditUserFirstName(user=model.user, gui_ref=frame.m_textCtrl2)
mediator_edit_user_surname_msg = MediatorEditUserSurName(user=model.user, gui_ref=frame.m_textCtrl3)
appgui = MediatorFrameAdornments(
    frame_title="Gui wired via OO Observer",
    frame_ref=frame,
    panel_colour=wx.Colour(255, 255, 135),
    panel_ref=frame.m_panel1,
    panel_colour_randomise=True,
)

# Observer Wiring
model.welcome.AddObserver(mediator_welcome_left)
model.welcome.AddObserver(mediator_welcome_user_right)
model.welcome.AddObserver(mediator_edit_welcome_msg)
model.user.AddObserver(mediator_welcome_user_right)
model.user.AddObserver(mediator_edit_user_firstname_msg)
model.user.AddObserver(mediator_edit_user_surname_msg)
# model.welcome.AddObserver(appgui)
# model.user.AddObserver(appgui)

model.dirty_all()  # initialise the gui with initial model values

app.MainLoop()
