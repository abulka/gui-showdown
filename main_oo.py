import wx
from gui import MyFrame1  #  <--- the wxformbuilder generated python module
import time
import random
from dataclasses import dataclass, astuple
from typing import List, Any
from observer import Observable, Observer

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
        self.NotifyAll(notificationEventType="")


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
        self.NotifyAll(notificationEventType="")

    @property
    def surname(self) -> str:
        return self._surname

    @surname.setter
    def surname(self, v: str) -> None:
        self._surname = v
        self.NotifyAll(notificationEventType="")


@dataclass
class Model:
    """Main model, contains both the welcome model and the user model"""

    welcome: Welcome
    user: User

    def dirty_all(self):
        self.welcome.NotifyAll("init dirty")
        self.user.NotifyAll("init dirty")


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
    uppercase_welcome: bool = False

    def Notify(self, target, notification_event_type):
        print("top left")

        if notification_event_type == "display option change":
            display_options = target
            self.uppercase_welcome = display_options.uppercase_welcome

        msg = self.welcome.message.upper() if self.uppercase_welcome else self.welcome.message
        self.gui_ref.SetLabel(msg)
        logsimple(self.welcome, self)


@dataclass
class MediatorWelcomeUserRight(Mediator):
    welcome: Welcome
    user: User
    gui_ref: wx.StaticText
    uppercase_welcome: bool = False
    uppercase_user: bool = False
    uppercase_welcome_user: bool = False

    def Notify(self, target, notification_event_type):
        print("top right")

        if notification_event_type == "display option change":
            display_options = target
            self.uppercase_welcome = display_options.uppercase_welcome
            self.uppercase_user = display_options.uppercase_user
            self.uppercase_welcome_user = display_options.uppercase_welcome_user

        welcome = self.welcome.message.upper() if (self.uppercase_welcome or self.uppercase_welcome_user) else self.welcome.message
        firstname = self.user.firstname.upper() if (self.uppercase_user or self.uppercase_welcome_user) else self.user.firstname
        surname = self.user.surname.upper() if (self.uppercase_user or self.uppercase_welcome_user) else self.user.surname
        self.gui_ref.SetLabel(f"{welcome} {firstname} {surname}")

        logsimple(self.welcome, self)
        logsimple(self.user, self)


@dataclass
class MediatorEditWelcome(Mediator):
    welcome: Welcome
    gui_ref: wx.TextCtrl

    def Notify(self, target, notification_event_type):
        print("edit welcome")
        self.gui_ref.SetValue(self.welcome.message)
        logsimple(self.welcome, self)


@dataclass
class MediatorEditUserFirstName(Mediator):
    user: User
    gui_ref: wx.TextCtrl

    def Notify(self, target, notification_event_type):
        print("edit user firstname")
        self.gui_ref.SetValue(self.user.firstname)
        logsimple(self.user, self)


@dataclass
class MediatorEditUserSurName(Mediator):
    user: User
    gui_ref: wx.TextCtrl

    def Notify(self, target, notification_event_type):
        print("edit user surname")
        self.gui_ref.SetValue(self.user.surname)
        logsimple(self.user, self)


@dataclass
class DisplayOptions(BaseModel):
    _uppercase_welcome = False
    _uppercase_user = False
    _uppercase_welcome_user = False

    @property
    def uppercase_welcome(self) -> str:
        return self._uppercase_welcome

    @uppercase_welcome.setter
    def uppercase_welcome(self, v: str) -> None:
        self._uppercase_welcome = v
        self.NotifyAll(notificationEventType="display option change")

    @property
    def uppercase_user(self) -> str:
        return self._uppercase_user

    @uppercase_user.setter
    def uppercase_user(self, v: str) -> None:
        self._uppercase_user = v
        self.NotifyAll(notificationEventType="display option change")

    @property
    def uppercase_welcome_user(self) -> str:
        return self._uppercase_welcome_user

    @uppercase_welcome_user.setter
    def uppercase_welcome_user(self, v: str) -> None:
        self._uppercase_welcome_user = v
        self.NotifyAll(notificationEventType="display option change")


@dataclass
class MediatorFrameAdornments(Mediator):
    frame_title: str
    frame_ref: wx.Frame
    panel_colour: wx.Colour
    panel_ref: wx.Panel
    panel_colour_randomise: bool

    def Notify(self, target, notification_event_type):
        self.frame_ref.SetTitle(self.frame_title + " " + time.asctime())
        self.panel_ref.SetBackgroundColour(
            wx.Colour(255, random.randint(120, 250), random.randint(120, 250)) if self.panel_colour_randomise else self.panel_colour
        )
        self.panel_ref.Refresh()  # f.panel_ref.Update() doesn't work, need to Refresh()
        logsimple(self, self)


#
# Util
#


def logsimple(o, mediator):  # simple logging
    print(f"have set {o} in {nice_mediator_name[id(mediator)]}")


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
        display_options.uppercase_welcome = frame.m_checkBox1A.IsChecked()  # TODO use event.target

    def on_check_toggle_user_outputs_only(self, event):
        display_options.uppercase_user = frame.m_checkBox1A1.IsChecked()  # TODO use event.target

    def on_check_upper_entire_top_right_output(self, event):
        display_options.uppercase_welcome_user = frame.m_checkBox2.IsChecked()  # TODO use event.target

    def on_enter_welcome(self, event):
        model.welcome.message = frame.m_textCtrl1.GetValue()

    def on_enter_user_firstname(self, event):
        model.user.firstname = frame.m_textCtrl2.GetValue()

    def on_enter_user_surname(self, event):
        model.user.surname = frame.m_textCtrl3.GetValue()

    def onClickRenderNow(self, event):
        model.dirty_all()


#
# Init WxPython
#

app = wx.App()
frame = MyFrame1A(None)
frame.Show()
frame.SetSize((500, 450))

#
# Wire up and build everything
#

model = Model(Welcome(), User())
mediator_welcome_left = MediatorWelcomeLeft(welcome=model.welcome, gui_ref=frame.m_staticText1)
mediator_welcome_user_right = MediatorWelcomeUserRight(welcome=model.welcome, user=model.user, gui_ref=frame.m_staticText2)
mediator_edit_welcome_msg = MediatorEditWelcome(welcome=model.welcome, gui_ref=frame.m_textCtrl1)
mediator_edit_user_name_msg = MediatorEditUserFirstName(user=model.user, gui_ref=frame.m_textCtrl2)
mediator_edit_user_surname_msg = MediatorEditUserSurName(user=model.user, gui_ref=frame.m_textCtrl3)
display_options = DisplayOptions()
appgui = MediatorFrameAdornments(
    frame_title="Gui wired via MVC",
    frame_ref=frame,
    panel_colour=wx.Colour(255, 255, 135),
    panel_ref=frame.m_panel1,
    panel_colour_randomise=True,
)

nice_mediator_name = {
    id(mediator_welcome_left): "mediator for welcome_left",
    id(mediator_welcome_user_right): "mediator for welcome_user_right",
    id(mediator_edit_welcome_msg): "mediator for edit_welcome_msg",
    id(mediator_edit_user_name_msg): "mediator for edit_user_name_msg",
    id(mediator_edit_user_surname_msg): "mediator for edit_user_surname_msg",
    id(display_options): "mediator for display_options",
    id(appgui): "mediator for app frame etc",
}
mediators: List[int] = list(nice_mediator_name.keys())

# Observer Wiring
model.welcome.AddObserver(mediator_welcome_left)
model.welcome.AddObserver(mediator_welcome_user_right)
model.welcome.AddObserver(mediator_edit_welcome_msg)
# model.welcome.AddObserver(appgui)
model.user.AddObserver(mediator_welcome_user_right)
model.user.AddObserver(mediator_edit_user_name_msg)
model.user.AddObserver(mediator_edit_user_surname_msg)
# model.user.AddObserver(appgui)
display_options.AddObserver(mediator_welcome_left)
display_options.AddObserver(mediator_welcome_user_right)

model.dirty_all()  # initialise the gui with initial model values

app.MainLoop()
