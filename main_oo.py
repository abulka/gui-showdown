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


@dataclass
class MediatorWelcomeLeft(Observer):
    model: Welcome
    gui_ref: wx.StaticText

    def __post_init__(self):
        super().__init__()

    def Notify(self, target, notification_event_ype):
        print("top left")
        self.gui_ref.SetLabel(self.model.message)

@dataclass
class MediatorWelcomeUserRight(Observer):
    welcome: Welcome
    user: User
    gui_ref: wx.StaticText

    def __post_init__(self):
        super().__init__()

    def Notify(self, target, notification_event_ype):
        print("top right")
        self.gui_ref.SetLabel(f"{self.welcome.message} {self.user.firstname} {self.user.surname}")

@dataclass
class MediatorEditWelcome(Observer):
    welcome: Welcome
    gui_ref: wx.TextCtrl

    def __post_init__(self):
        super().__init__()

    def Notify(self, target, notification_event_ype):
        print("edit welcome")
        self.gui_ref.SetValue(self.welcome.message)

@dataclass
class MediatorEditUserFirstName(Observer):
    user: User
    gui_ref: wx.TextCtrl

    def __post_init__(self):
        super().__init__()

    def Notify(self, target, notification_event_ype):
        print("edit user firstname")
        self.gui_ref.SetValue(self.user.firstname)

@dataclass
class MediatorEditUserSurName(Observer):
    user: User
    gui_ref: wx.TextCtrl

    def __post_init__(self):
        super().__init__()

    def Notify(self, target, notification_event_ype):
        print("edit user surname")
        self.gui_ref.SetValue(self.user.surname)


class MyFrame1A(MyFrame1):
    def onResetWelcome(self, event):
        models.welcome.message = "Hello"

    def onCheck1(self, event):
        # toggle the case of the model's welcome message
        model_welcome_toggle()
        do.dirty(ModelWelcome)
        world.process()

    def onCheckToggleWelcomeOutputsOnly(self, event):
        # toggle the case of the welcome output messages only - do not affect model
        add_or_remove_component(
            world, 
            condition=frame.m_checkBox1A.IsChecked(), 
            component_Class=UP_L_AND_R_WELCOME_ONLY, 
            entities=[entity_welcome_left, entity_welcome_user_right])
        do.dirty("welcome display only, not via model")  # doesn't affect welcome text edit field
        world.process()

    def onCheck2(self, event):
        # don't change the model - only the UI display
        add_or_remove_component(
            world, 
            condition=frame.m_checkBox2.IsChecked(), 
            component_Class=UP_R_WHOLE, 
            entities=[entity_welcome_user_right])
        do.dirty("just top right")
        world.process()

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
    model=models.welcome, 
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

models.welcome.AddObserver(mediator_welcome_left)
models.welcome.AddObserver(mediator_welcome_user_right)
models.welcome.AddObserver(mediator_edit_welcome_msg)
models.user.AddObserver(mediator_welcome_user_right)
models.user.AddObserver(mediator_edit_user_name_msg)
models.user.AddObserver(mediator_edit_user_surname_msg)

models.welcome.message = "howdy"
models.user.firstname = "Andy"
models.user.surname = "BBB"

# world = esper.World()
# world.add_processor(ModelExtractProcessor())
# world.add_processor(CaseTransformProcessor())
# world.add_processor(RenderProcessor())
# world.add_processor(HousekeepingProcessor())
# world.add_processor(FunProcessor())

# entity_welcome_left = world.create_entity()
# entity_welcome_user_right = world.create_entity()
# entity_edit_welcome_msg = world.create_entity()
# entity_edit_user_name_msg = world.create_entity()
# entity_edit_user_surname_msg = world.create_entity()

# nice_entity_name = {
#     entity_welcome_left: "mediator for welcome_left",
#     entity_welcome_user_right: "mediator for welcome_user_right",
#     entity_edit_welcome_msg: "mediator for edit_welcome_msg",
#     entity_edit_user_name_msg: "mediator for edit_user_name_msg",
#     entity_edit_user_surname_msg: "mediator for edit_user_surname_msg",
# }
# mediators: List[int] = list(nice_entity_name.keys())

# world.add_component(entity_welcome_left, ModelWelcome(model=model, key="welcome_msg"))
# world.add_component(entity_welcome_left, GuiStaticText(ref=frame.m_staticText1))

# world.add_component(entity_welcome_user_right, ModelWelcome(model=model, key="welcome_msg"))
# world.add_component(entity_welcome_user_right, ModelFirstname(model=model["user"], key="name"))
# world.add_component(entity_welcome_user_right, ModelSurname(model=model["user"], key="surname"))
# world.add_component(entity_welcome_user_right, GuiStaticText(ref=frame.m_staticText2))

# world.add_component(entity_edit_welcome_msg, ModelWelcome(model=model, key="welcome_msg"))
# world.add_component(entity_edit_welcome_msg, GuiTextControl(ref=frame.m_textCtrl1))

# world.add_component(entity_edit_user_name_msg, ModelFirstname(model=model["user"], key="name"))
# world.add_component(entity_edit_user_name_msg, GuiTextControl(ref=frame.m_textCtrl2))

# world.add_component(entity_edit_user_surname_msg, ModelSurname(model=model["user"], key="surname"))
# world.add_component(entity_edit_user_surname_msg, GuiTextControl(ref=frame.m_textCtrl3))

# world.add_component(entity_edit_user_surname_msg, FrameAdornments(frame_title="Gui wired via ESC",
#                                                                   frame_ref=frame,
#                                                                   panel_colour=wx.Colour( 255, 255, 135 ),
#                                                                   panel_ref=frame.m_panel1,
#                                                                   panel_colour_randomise=True
#                                                                   ))

# do = DirtyObserver(world)
# do.add_dependency(ModelWelcome, [entity_welcome_left, entity_welcome_user_right, entity_edit_welcome_msg])
# do.add_dependency(ModelFirstname, [entity_welcome_user_right, entity_edit_user_name_msg])
# do.add_dependency(ModelSurname, [entity_welcome_user_right, entity_edit_user_surname_msg])
# do.add_dependency("welcome display only, not via model", [entity_welcome_left, entity_welcome_user_right])
# do.add_dependency("just top right", [entity_welcome_user_right])

# do.dirty_all(entities=mediators)    
# world.process()

app.MainLoop()
