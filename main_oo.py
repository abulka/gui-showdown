import wx
from gui import MyFrame1  #  <--- the wxformbuilder generated python module
import time
import random
from dataclasses import dataclass
from typing import List, Any
from observer import Observable, Observer

# # The only reason we have a deep model like this, is because it is shared and manipulated by
# # many things.  Other 'model' data bits can be put into components directly as a sole place.
# model = {
#     "welcome_msg": "Welcome",
#     "user": {
#         "name": "Sam",
#         "surname": "Smith",
#     }
# }

@dataclass
class Welcome(Observable):
    _msg: str = "Welcome"

    @property
    def message(self) -> str:
        return self._msg

    @message.setter
    def message(self, v: str) -> None:
        self._msg = v
        self.NotifyAll(notificationEventType='')

    def __post_init__(self):
        super().__init__()

@dataclass
class User(Observable):
    _firstname: str = "Sam"
    _surname: str = "Smith"

    @property
    def firstname(self) -> str:
        return self._firstname

    @firstname.setter
    def firstname(self, v: str) -> None:
        self._firstname = v
        self.NotifyAll(notificationEventType='')

    @property
    def surname(self) -> str:
        return self._surname

    @surname.setter
    def surname(self, v: str) -> None:
        self._surname = v
        self.NotifyAll(notificationEventType='')

    def __post_init__(self):
        super().__init__()

@dataclass
class Models:
    welcome: Welcome
    user: User

    def dirty_all(self):
        self.welcome.NotifyAll('init dirty')
        self.user.NotifyAll('init dirty')

@dataclass
class MediatorWelcomeLeft(Observer):
    welcome: Welcome
    gui_ref: wx.StaticText
    uppercase_welcome: bool = False

    def __post_init__(self):
        super().__init__()

    def Notify(self, target, notification_event_type):
        print("top left")
        msg = self.welcome.message.upper() if self.uppercase_welcome else self.welcome.message
        self.gui_ref.SetLabel(msg)

@dataclass
class MediatorWelcomeUserRight(Observer):
    welcome: Welcome
    user: User
    gui_ref: wx.StaticText
    uppercase_welcome: bool = False
    uppercase_all: bool = False

    def __post_init__(self):
        super().__init__()

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

@dataclass
class MediatorEditWelcome(Observer):
    welcome: Welcome
    gui_ref: wx.TextCtrl

    def __post_init__(self):
        super().__init__()

    def Notify(self, target, notification_event_type):
        print("edit welcome")
        self.gui_ref.SetValue(self.welcome.message)

@dataclass
class MediatorEditUserFirstName(Observer):
    user: User
    gui_ref: wx.TextCtrl

    def __post_init__(self):
        super().__init__()

    def Notify(self, target, notification_event_type):
        print("edit user firstname")
        self.gui_ref.SetValue(self.user.firstname)

@dataclass
class MediatorEditUserSurName(Observer):
    user: User
    gui_ref: wx.TextCtrl

    def __post_init__(self):
        super().__init__()

    def Notify(self, target, notification_event_type):
        print("edit user surname")
        self.gui_ref.SetValue(self.user.surname)

@dataclass
class MediatorFrameAdornments(Observer):
    frame_title: str
    frame_ref: wx.Frame
    panel_colour: wx.Colour
    panel_ref: wx.Panel
    panel_colour_randomise: bool

    def Notify(self, target, notification_event_type):
        self.frame_ref.SetTitle(self.frame_title + " " + time.asctime())
        self.panel_ref.SetBackgroundColour(wx.Colour(255, random.randint(120, 250), random.randint(120, 250)) if self.panel_colour_randomise else self.panel_colour)
        self.panel_ref.Refresh()  # f.panel_ref.Update() doesn't work, need to Refresh()

def housekeeping():
    if frame.m_checkBox1.IsChecked():
        frame.m_checkBox1A.Disable()
    else:
        frame.m_checkBox1A.Enable()

def model_welcome_toggle():
        models.welcome.message = models.welcome.message.upper() if frame.m_checkBox1.IsChecked() else models.welcome.message.lower()

class MyFrame1A(MyFrame1):
    def onResetWelcome(self, event):
        models.welcome.message = "Hello"

    def onCheck1(self, event):
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
        models.welcome.message = frame.m_textCtrl1.GetValue()

    def onClickResetUser( self, event ):
        models.user.firstname = "Fred"
        models.user.surname = "Flinstone"

    def onEnterUserName( self, event ):
        models.user.firstname = frame.m_textCtrl2.GetValue()

    def onEnterUserSurname( self, event ):
        models.user.surname = frame.m_textCtrl3.GetValue()

    def onClickRenderNow( self, event ):
        world.process()


app = wx.App()
frame = MyFrame1A(None)
frame.Show()
frame.SetSize((500, 400))

models = Models(
    Welcome(), 
    User()
)

mediator_welcome_left = MediatorWelcomeLeft(
    welcome=models.welcome, 
    gui_ref=frame.m_staticText1
)
mediator_welcome_user_right = MediatorWelcomeUserRight(
    welcome=models.welcome,
    user=models.user,
    gui_ref=frame.m_staticText2
) 
mediator_edit_welcome_msg = MediatorEditWelcome(
    welcome=models.welcome, 
    gui_ref=frame.m_textCtrl1
)
mediator_edit_user_name_msg = MediatorEditUserFirstName(
    user=models.user,
    gui_ref=frame.m_textCtrl2
)
mediator_edit_user_surname_msg = MediatorEditUserSurName(
    user=models.user,
    gui_ref=frame.m_textCtrl3
)
appgui = MediatorFrameAdornments(
    frame_title="Gui wired via MVC",
    frame_ref=frame,
    panel_colour=wx.Colour( 255, 255, 135 ),
    panel_ref=frame.m_panel1,
    panel_colour_randomise=True
)

models.welcome.AddObserver(mediator_welcome_left)
models.welcome.AddObserver(mediator_welcome_user_right)
models.welcome.AddObserver(mediator_edit_welcome_msg)
models.welcome.AddObserver(appgui)
models.user.AddObserver(mediator_welcome_user_right)
models.user.AddObserver(mediator_edit_user_name_msg)
models.user.AddObserver(mediator_edit_user_surname_msg)
models.user.AddObserver(appgui)

models.dirty_all()  # initialise the gui with initial model values

# nice_entity_name = {
#     entity_welcome_left: "mediator for welcome_left",
#     entity_welcome_user_right: "mediator for welcome_user_right",
#     entity_edit_welcome_msg: "mediator for edit_welcome_msg",
#     entity_edit_user_name_msg: "mediator for edit_user_name_msg",
#     entity_edit_user_surname_msg: "mediator for edit_user_surname_msg",
# }
# mediators: List[int] = list(nice_entity_name.keys())

app.MainLoop()
