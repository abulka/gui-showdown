import wx
from gui import MyFrame1  #  <--- the wxformbuilder generated python module
import time
import random
from dataclasses import dataclass, astuple
from typing import List, Any
from observer import Observable, Observer

# The Welcome model and User model are Observable.


@dataclass
class BaseModel(Observable):
    def __post_init__(self):
        super().__init__()

    # def __hash__(self):
    #     return hash(tuple(self))


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
    welcome: Welcome
    user: User

    def dirty_all(self):
        self.welcome.NotifyAll("init dirty")
        self.user.NotifyAll("init dirty")


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
        msg = self.welcome.message.upper() if self.uppercase_welcome else self.welcome.message
        self.gui_ref.SetLabel(msg)
        dump(self.welcome, self)


@dataclass
class MediatorWelcomeUserRight(Mediator):
    welcome: Welcome
    user: User
    gui_ref: wx.StaticText
    uppercase_welcome: bool = False
    uppercase_all: bool = False

    def Notify(self, target, notification_event_type):
        print("top right")
        if self.uppercase_all:
            msg = f"{self.welcome.message} {self.user.firstname} {self.user.surname}"
            msg = msg.upper()
        elif self.uppercase_welcome:
            msg = f"{self.welcome.message.upper()} {self.user.firstname} {self.user.surname}"
        else:
            msg = f"{self.welcome.message} {self.user.firstname} {self.user.surname}"
        self.gui_ref.SetLabel(msg)
        dump(self.welcome, self)
        dump(self.user, self)


@dataclass
class MediatorEditWelcome(Mediator):
    welcome: Welcome
    gui_ref: wx.TextCtrl

    def Notify(self, target, notification_event_type):
        print("edit welcome")
        self.gui_ref.SetValue(self.welcome.message)
        dump(self.welcome, self)


@dataclass
class MediatorEditUserFirstName(Mediator):
    user: User
    gui_ref: wx.TextCtrl

    def Notify(self, target, notification_event_type):
        print("edit user firstname")
        self.gui_ref.SetValue(self.user.firstname)
        dump(self.user, self)


@dataclass
class MediatorEditUserSurName(Mediator):
    user: User
    gui_ref: wx.TextCtrl

    def Notify(self, target, notification_event_type):
        print("edit user surname")
        self.gui_ref.SetValue(self.user.surname)
        dump(self.user, self)


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
        dump(self, self)


# Not used - but would be nice to integrate something like this into the MVC
# but then again, the mediators themselves have these attributes, each mediator entity is like a view model, so
# why replicate that information uncessessarily.
view_model = {"uppercase welcome model": False, "uppercase welcome outputs": False, "uppercase top right": False}


def dump(o, mediator):  # simple logging
    print(f"have set {o} in {nice_mediator_name[id(mediator)]}")


def housekeeping():
    if frame.m_checkBox1.IsChecked():
        frame.m_checkBox1A.Disable()
    else:
        frame.m_checkBox1A.Enable()


def model_welcome_toggle():
    model.welcome.message = model.welcome.message.upper() if frame.m_checkBox1.IsChecked() else model.welcome.message.lower()


# Frame
class MyFrame1A(MyFrame1):
    def onResetWelcome(self, event):
        model.welcome.message = "Hello"

    def on_check_welcome_model(self, event):
        # toggle the case of the model's welcome message
        model_welcome_toggle()
        housekeeping()

    def onCheckToggleWelcomeOutputsOnly(self, event):
        # toggle the case of the welcome output messages only - do not affect model
        mediator_welcome_left.uppercase_welcome = True if frame.m_checkBox1A.IsChecked() else False
        mediator_welcome_user_right.uppercase_welcome = True if frame.m_checkBox1A.IsChecked() else False
        mediator_welcome_left.Notify(None, "checked event")  # bit weird having target=None
        mediator_welcome_user_right.Notify(None, "checked event")
        housekeeping()

    def onCheck2(self, event):
        # don't change the model - only the UI display
        mediator_welcome_user_right.uppercase_all = True if frame.m_checkBox2.IsChecked() else False
        mediator_welcome_user_right.Notify(None, "checked event")  # bit weird having target=None

    def onEnter(self, event):
        model.welcome.message = frame.m_textCtrl1.GetValue()

    def onClickResetUser(self, event):
        model.user.firstname = "Fred"
        model.user.surname = "Flinstone"

    def onEnterUserName(self, event):
        model.user.firstname = frame.m_textCtrl2.GetValue()

    def onEnterUserSurname(self, event):
        model.user.surname = frame.m_textCtrl3.GetValue()

    def onClickRenderNow(self, event):
        world.process()


app = wx.App()
frame = MyFrame1A(None)
frame.Show()
frame.SetSize((500, 400))

model = Model(Welcome(), User())

mediator_welcome_left = MediatorWelcomeLeft(welcome=model.welcome, gui_ref=frame.m_staticText1)
mediator_welcome_user_right = MediatorWelcomeUserRight(welcome=model.welcome, user=model.user, gui_ref=frame.m_staticText2)
mediator_edit_welcome_msg = MediatorEditWelcome(welcome=model.welcome, gui_ref=frame.m_textCtrl1)
mediator_edit_user_name_msg = MediatorEditUserFirstName(user=model.user, gui_ref=frame.m_textCtrl2)
mediator_edit_user_surname_msg = MediatorEditUserSurName(user=model.user, gui_ref=frame.m_textCtrl3)
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
    id(appgui): "mediator for app frame etc",
}
mediators: List[int] = list(nice_mediator_name.keys())

# Observer Wiring
model.welcome.AddObserver(mediator_welcome_left)
model.welcome.AddObserver(mediator_welcome_user_right)
model.welcome.AddObserver(mediator_edit_welcome_msg)
model.welcome.AddObserver(appgui)
model.user.AddObserver(mediator_welcome_user_right)
model.user.AddObserver(mediator_edit_user_name_msg)
model.user.AddObserver(mediator_edit_user_surname_msg)
model.user.AddObserver(appgui)

model.dirty_all()  # initialise the gui with initial model values

app.MainLoop()
