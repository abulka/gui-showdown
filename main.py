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
class MUFIRSTNAME:  # User model ref
    model: dict
    key: str

@dataclass
class MUSURNAME:  # User surname model ref
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
class UP_R_WHOLE:  # flag to make upper right message uppercase or not
    pass

@dataclass
class UP_L_AND_R_WELCOME_ONLY:  # flag to make upper left AND upper right (welcome portion ONLY) message uppercase or not
    pass

# @dataclass
# class Final:  # represents info extracted from model as plain string, can be transformed before rendering system
#     welcome: str
#     firstname: str
#     surname: str

@dataclass
class FinalW:  # Final only for Welcome
    s: str

# @dataclass
# class FinalU:  # Final only for User
#     s: str
@dataclass
class FinalUname:  # Final only for User.name
    s: str
@dataclass
class FinalUsurname:  # Final only for User.surname
    s: str


class ModelExtractProcessor(esper.Processor):
    def process(self):
        print("--Model Extract System---")
        for ent, (mw, d) in self.world.get_components(MW, Dirty):
            f = FinalW(s=mw.model[mw.key])
            world.add_component(ent, f)
            dump(f, ent)

        for ent, (mu, d) in self.world.get_components(MUFIRSTNAME, Dirty):
            f = FinalUname(s=mu.model[mu.key])
            world.add_component(ent, f)
            dump(f, ent)

        for ent, (mus, d) in self.world.get_components(MUSURNAME, Dirty):
            f = FinalUsurname(s=mus.model[mus.key])
            world.add_component(ent, f)
            dump(f, ent)

        # for ent, (mu, mus, d) in self.world.get_components(MUFIRSTNAME, MUSURNAME, Dirty):
        #     name = mu.model[mu.key]
        #     surname = mus.model[mus.key]
        #     combined = f"{name} {surname}"
        #     f = FinalU(s=combined)
        #     world.add_component(ent, f)
        #     dump(f, ent)

class CaseTransformProcessor(esper.Processor):
    def process(self):
        print("--Case transform System---")
        for ent, (f, uprw, d) in self.world.get_components(FinalW, UP_L_AND_R_WELCOME_ONLY, Dirty):
            f.s = f.s.upper()
            dump(f, ent)
        for ent, (f, upr, d) in self.world.get_components(FinalW, UP_R_WHOLE, Dirty):
            f.s = f.s.upper()
            dump(f, ent)
        # for ent, (f, upr, d) in self.world.get_components(FinalU, UP_R_WHOLE, Dirty):
        #     f.s = f.s.upper()
        #     dump(f, ent)
        for ent, (f, upr, d) in self.world.get_components(FinalUname, UP_R_WHOLE, Dirty):
            f.s = f.s.upper()
            dump(f, ent)
        for ent, (f, upr, d) in self.world.get_components(FinalUsurname, UP_R_WHOLE, Dirty):
            f.s = f.s.upper()
            dump(f, ent)


class RenderProcessor(esper.Processor):
    def process(self):
        print("--Render System--")
        ents = set()

        for ent, (finalw, guist, d) in self.world.get_components(FinalW, GUIST, Dirty):
            print("mw top left static", ent)
            guist.ref.SetLabel(finalw.s)
            ents.add(ent)
        for ent, (finalw, finalf, finals, guist, d) in self.world.get_components(FinalW, FinalUname, FinalUsurname, GUIST, Dirty):
            print("mw mu mus top right")
            guist.ref.SetLabel(f"{finalw.s} {finalf.s} {finals.s}")
            ents.add(ent)
        # for ent, (finalw, finalu, guist, d) in self.world.get_components(FinalW, FinalU, GUIST, Dirty):
        #     print("mw mu mus top right")
        #     guist.ref.SetLabel(f"{finalw.s} {finalu.s}")
        #     ents.add(ent)
        for ent, (finalw, guitc, d) in self.world.get_components(FinalW, GUITC, Dirty):
            print("mw textctrl")
            guitc.ref.SetValue(finalw.s)
            ents.add(ent)

        # USER 

        # for ent, (finalu, guitc, d) in self.world.get_components(FinalU, GUITC, Dirty):
        #     print("mu textctrl (hopefully both)")
        #     guitc.ref.SetValue(finalu.s)
        #     ents.add(ent)

        # wish we didn't have two loops
        for ent, (finaluname, guitc, d) in self.world.get_components(FinalUname, GUITC, Dirty):
            print("mu textctrl (name)")
            guitc.ref.SetValue(finaluname.s)
            ents.add(ent)
        for ent, (finalusurname, guitc, d) in self.world.get_components(FinalUsurname, GUITC, Dirty):
            print("mu textctrl (surname)")
            guitc.ref.SetValue(finalusurname.s)
            ents.add(ent)

        for ent in list(ents):
            if world.has_component(ent, UP_R_WHOLE):
                world.remove_component(ent, UP_R_WHOLE)
            if world.has_component(ent, UP_L_AND_R_WELCOME_ONLY):
                world.remove_component(ent, UP_L_AND_R_WELCOME_ONLY)
            world.remove_component(ent, Dirty)

class HousekeepingProcessor(esper.Processor):
    def process(self):
        print("--Housekeeping System--")

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
            world.add_component(entity_welcome_left, UP_L_AND_R_WELCOME_ONLY())
            world.add_component(entity_welcome_user_right, UP_L_AND_R_WELCOME_ONLY())
        else:
            if world.has_component(entity_welcome_left, UP_L_AND_R_WELCOME_ONLY):
                world.remove_component(entity_welcome_left, UP_L_AND_R_WELCOME_ONLY)
            if world.has_component(entity_welcome_user_right, UP_L_AND_R_WELCOME_ONLY):
                world.remove_component(entity_welcome_user_right, UP_L_AND_R_WELCOME_ONLY)
        dirty("welcome outputs only")  # doesn't affect welcome edit field
        world.process()

    def onCheck2(self, event):
        # don't change the model - only the UI display
        # how do we tell the 'system' logic to do this?  need a flag or an extra component
        # looks like its going to be an extra component. Pity - that's inefficient and complex.
        #
        # perhaps we need a two pass render which converts model info to plain info then the uppercase/lowercase
        # can further act on that plain info before rendering.
        e = entity_welcome_user_right
        if frame.m_checkBox2.IsChecked():
            world.add_component(e, UP_R_WHOLE())
        else:
            if world.has_component(e, UP_R_WHOLE):
                world.remove_component(e, UP_R_WHOLE)
        dirty("just top right")
        world.process()

    def onEnter(self, event):
        model["welcome_msg"] = frame.m_textCtrl1.GetValue()
        dirty(MW)
        world.process()

    def onClickResetUser( self, event ):
        model["user"]["name"] = "Fred"
        model["user"]["surname"] = "Flinstone"
        dirty(MUFIRSTNAME)
        dirty(MUSURNAME)
        world.process()

    def onEnterUserName( self, event ):
        model["user"]["name"] = frame.m_textCtrl2.GetValue()
        dirty(MUFIRSTNAME)
        world.process()

    def onEnterUserSurname( self, event ):
        model["user"]["surname"] = frame.m_textCtrl3.GetValue()
        dirty(MUSURNAME)
        world.process()

    def onClickRenderNow( self, event ):
        world.process()


world = esper.World()
world.add_processor(ModelExtractProcessor())
world.add_processor(CaseTransformProcessor())
world.add_processor(RenderProcessor())
world.add_processor(HousekeepingProcessor())


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

nice_entity_name = {  # can't we get esper to give us this info?
    1: "entity_welcome_left",
    2: "entity_welcome_user_right",
    3: "entity_edit_welcome_msg",
    4: "entity_edit_user_name_msg",
    5: "entity_edit_user_surname_msg",
}

def dump(component, entity):
    print(f"added {component} to {nice_entity_name[entity]}")
 
world.add_component(entity_welcome_left, MW(model=model, key="welcome_msg"))
world.add_component(entity_welcome_left, GUIST(ref=frame.m_staticText1))

world.add_component(entity_welcome_user_right, MW(model=model, key="welcome_msg"))
world.add_component(entity_welcome_user_right, MUFIRSTNAME(model=model["user"], key="name"))
world.add_component(entity_welcome_user_right, MUSURNAME(model=model["user"], key="surname"))
world.add_component(entity_welcome_user_right, GUIST(ref=frame.m_staticText2))

world.add_component(entity_edit_welcome_msg, MW(model=model, key="welcome_msg"))
world.add_component(entity_edit_welcome_msg, GUITC(ref=frame.m_textCtrl1))

world.add_component(entity_edit_user_name_msg, MUFIRSTNAME(model=model["user"], key="name"))
world.add_component(entity_edit_user_name_msg, GUITC(ref=frame.m_textCtrl2))

world.add_component(entity_edit_user_surname_msg, MUSURNAME(model=model["user"], key="surname"))
world.add_component(entity_edit_user_surname_msg, GUITC(ref=frame.m_textCtrl3))


# Tells us which model each mediator entity cares about, like observer pattern mappings.
# Note this uses the model component ref class, rather than anything about the model dict itself
# We even have arbitrary keys which are more verbose model descriptions to make it easier
dirty_model_to_entities = {
    MW: [entity_welcome_left, entity_welcome_user_right, entity_edit_welcome_msg],
    "welcome outputs only": [entity_welcome_left, entity_welcome_user_right],
    MUFIRSTNAME: [entity_welcome_user_right, entity_edit_user_name_msg],
    MUSURNAME: [entity_welcome_user_right, entity_edit_user_surname_msg],
    "just top right": [entity_welcome_user_right],
}

def dirty_all():
    for e in mediators:
        world.add_component(e, Dirty())

def dirty(component_class):
    # dirty_all()
    # return
    for mediator in dirty_model_to_entities[component_class]:
        print(f"dirty: {mediator} because {component_class}")
        world.add_component(mediator, Dirty())

dirty_all()    
world.process()

app.MainLoop()
