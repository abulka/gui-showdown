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

# Not used - but would be nice to integrate something like this into the ECS
view_model = {
    "uppercase welcome model": False,
    "uppercase welcome outputs": False,
    "uppercase top right": False,
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
class MUS:  # User surname model ref
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

@dataclass
class UPR:  # flag to make upper right message uppercase or not
    pass

@dataclass
class UPRW:  # flag to make upper left AND upper right (welcome portion ONLY) message uppercase or not
    pass


class RenderProcessor(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        print("RENDER")
        ents = set()

        for ent, (mw, guist, d) in self.world.get_components(MW, GUIST, Dirty):
            # This loop picks up entities who also have MU !! yikes.
            print("mw top left", ent)
            welcome = mw.model[mw.key]

            # See if additional behaviour is needed
            if self.world.has_component(ent, UPRW):
                welcome = welcome.upper()

            guist.ref.SetLabel(welcome)
            ents.add(ent)

        for ent, (mw, guitc, d) in self.world.get_components(MW, GUITC, Dirty):
            print("mw textctrl")
            guitc.ref.SetValue(mw.model[mw.key])
            ents.add(ent)

        for ent, (mw, mu, mus, guist, d) in self.world.get_components(MW, MU, MUS, GUIST, Dirty):
            print("mw mu mus top right")
            welcome = mw.model[mw.key]
            user = f"{mu.model[mu.key]} {mus.model[mus.key]}"

            # See if additional behaviour is needed
            if self.world.has_component(ent, UPRW):
                welcome = welcome.upper()
            if self.world.has_component(ent, UPR):
                welcome = welcome.upper()
                user = user.upper()

            guist.ref.SetLabel(f"{welcome} {user}")
            ents.add(ent)

        for ent, (mu, guitc, d) in self.world.get_components(MU, GUITC, Dirty):
            print("mu name textctrl")
            guitc.ref.SetValue(mu.model[mu.key])
            ents.add(ent)

        for ent, (mus, guitc, d) in self.world.get_components(MUS, GUITC, Dirty):
            print("mus surname textctrl", mus.model[mu.key])
            guitc.ref.SetValue(mus.model[mus.key])
            ents.add(ent)

        for ent in list(ents):
            world.remove_component(ent, Dirty)

        # General housekeeping
        if frame.m_checkBox1.IsChecked():
            frame.m_checkBox1A.Disable()
        else:
            frame.m_checkBox1A.Enable()


def model_welcome_toggle():
        model["welcome_msg"] = model["welcome_msg"].upper() if frame.m_checkBox1.IsChecked() else model["welcome_msg"].lower()

def model_setter_welcome(msg):
        model["welcome_msg"] = msg
        model_welcome_toggle()

class MyFrame1A(MyFrame1):
    def onResetWelcome(self, event):
        model_setter_welcome("Hello")  # so that welcome uppercase toggle is respected
        dirty(MW)
        world.process()

    def onCheck1(self, event):
        # toggle the case of the model's welcome message
        model_welcome_toggle()
        dirty(MW)
        world.process()

    def onCheckToggleWelcomeOutputsOnly(self, event):
        # toggle the case of the welcome output messages only - do not affect model
        if frame.m_checkBox1A.IsChecked():
            world.add_component(entity_welcome_left, UPRW())
            world.add_component(entity_welcome_user_right, UPRW())
        else:
            world.remove_component(entity_welcome_left, UPRW)
            world.remove_component(entity_welcome_user_right, UPRW)
        dirty("welcome outputs only")  # doesn't affect welcome edit field
        world.process()

    def onCheck2(self, event):
        # don't change the model - only the UI display
        # how do we tell the 'system' logic to do this?  need a flag or an extra component
        # looks like its going to be an extra component. Pity - that's inefficient and complex.
        #
        # perhaps we need a two pass render which converts model info to plain info then the uppercase/lowercase
        # can furth act on that plain info before rendering.
        if frame.m_checkBox2.IsChecked():
            world.add_component(entity_welcome_user_right, UPR())
        else:
            world.remove_component(entity_welcome_user_right, UPR)
        dirty("just top right")
        world.process()

    def onEnter(self, event):
        model["welcome_msg"] = frame.m_textCtrl1.GetValue()
        dirty(MW)
        world.process()

    def onClickResetUser( self, event ):
        model["user"]["name"] = "Fred"
        model["user"]["surname"] = "Flinstone"
        dirty(MU)
        dirty(MUS)
        world.process()

    def onEnterUserName( self, event ):
        model["user"]["name"] = frame.m_textCtrl2.GetValue()
        dirty(MU)
        world.process()

    def onEnterUserSurname( self, event ):
        model["user"]["surname"] = frame.m_textCtrl3.GetValue()
        dirty(MUS)
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
world.add_component(entity_welcome_user_right, MUS(model=model["user"], key="surname"))
world.add_component(entity_welcome_user_right, GUIST(ref=frame.m_staticText2))

world.add_component(entity_edit_welcome_msg, MW(model=model, key="welcome_msg"))
world.add_component(entity_edit_welcome_msg, GUITC(ref=frame.m_textCtrl1))

world.add_component(entity_edit_user_name_msg, MU(model=model["user"], key="name"))
world.add_component(entity_edit_user_name_msg, GUITC(ref=frame.m_textCtrl2))

world.add_component(entity_edit_user_surname_msg, MUS(model=model["user"], key="surname"))
world.add_component(entity_edit_user_surname_msg, GUITC(ref=frame.m_textCtrl3))


# Tells us which model each mediator entity cares about, like observer pattern mappings.
# Note this uses the model component ref class, rather than anything about the model dict itself
# We even have arbitrary keys which are more verbose model descriptions to make it easier
dirty_model_to_entities = {
    MW: [entity_welcome_left, entity_welcome_user_right, entity_edit_welcome_msg],
    "welcome outputs only": [entity_welcome_left, entity_welcome_user_right],
    MU: [entity_welcome_user_right, entity_edit_user_name_msg],
    MUS: [entity_welcome_user_right, entity_edit_user_surname_msg],
    "just top right": [entity_welcome_user_right],
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
