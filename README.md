# wx_esper

An attempt to use esper ECS for traditional GUI programming.

A modern GUI framework with a model to render might traverse the model and shove
information into the gui controls.  Click and other events might make changes to
the gui widgets directly from then on, or more properly, update the model and then
reflect those changes into the widgets.  
A downside of this naive approach is that if the model is changed by other means
(not by gui clicks but by other parts of the software system) then those changes are
not reflected in the gui.

A MGM pattern (or MVC) approach would have any changes to the model via setters notify
mediators (controllers) whose job it is to update the gui widgets (view).  Click and other events thus need only make changes to the model and the model will notify the mediators (controllers) as necessary.

To implement the MGM pattern using an ECS (entity component system) architectural
approach is conceptually challenging, because ECS has its roots in game architectures
where entities are game objects which are typically sprites which are rendered by 'systems'
which draw onto a canvas.  How do models, mediators and gui widgets map to ECS concepts,
and how to we remove most of the OO from them, in order to do things the ECS way?

## Using ECS approach to implement the MGM / MVC design pattern.

Whilst there are many possible solutions, the cleanest solution which might be able to be
used across a whole application in a way that makes use of the benefits of ECS is as follows.

Untangle the OO data and behaviour of the mediator. The mediator becomes a mere entity, with its
previous data as a component, and its previous behaviour in a system.

Gui OO widgets are supplied by the framework e.g. wxPython or HTML/DOM and remain unchanged.

OO Models are as they were, or they can be converted to nested dictionaries, it doesn't matter.
If ECS is being used in other areas of your application, then your OO model object might turn
into entities with their own components - not really relevant to this project.

### Thus

Entities are the mediators, with components being things like model references, gui widget 
references. This is the data that the mediator typically needs, except its broken out as components.

The system contains the code/behaviour of the mediator, which pulls things out of the model and 
into a widget.  Currently we are cheating and have a single Render system which scans for
certain combination of components and knows what to do with them.

The checkbox and button events change the model, then in the asence of a observer pattern,
simply trigger a world.process() to render.  A bit inefficient, but I hope to introduce a dirty flag.

## Code Example

The behaviour we are modelling is:

Model:
- a welcome message, default "Hi"
- a user, default "Andy"

The GUI displays:
- the welcome message twice
    - top left: pure message
    - top right: message + user
- text entry, which allows editing of the welcome message
- text entry, which allows editing of the user name and surname
- checkbox1, which toggles the model welcome message uppercase/lowercase
- checkbox2, which toggles the top right user to uppercase (not via model)
- button1, which resets the welcome message to "Hi"
- button2, which resets the user to "Fred Flinstone"

## On Observers and Dirty

** Note that in the absence of an observer pattern being implemented, you can instead
simply loop through all mediators and trigger them, thus updating the GUI to the state of the
current model. This loop could be called periodically and strategically.  Its a cheap way.
Adding a dirty flag to model entities would allow us to skip mediators that don't need to 
be triggered, thus is more efficient.  Even better optimisation is achieved with dirty models
and sets, like the way ECS systems query for components that match - you can include a dirty
component and the set-based lookup speed will be more efficient (rather than looping through
all possible mediators and triggering only those whose associated models are 'dirty').

When implementing dirty, it is more efficient to dirty certain mediators, but 
is this complexity worth it?  

For example, rather than not having dirty flags, or having a `dirty_all()` call (which amounts to everything being dirty thus no point in the dirty flag) - we could be more specific:

```python
def onCheck1(self, event):
    world.add_component(entity_welcome_left, Dirty())

    world.add_component(entity_welcome_user_right, Dirty())

    world.process()
```

Perhaps an observer system is indeed best to have after all.  The model would have to be an observable object though - not a pure dict.  And the mediators would have to observers - thus objects too?  

But neither is an object in this ECS project - how do we implement an observer pattern within ECS without objects?

There are some discussions here about implementing observer in ECS:

* https://www.reddit.com/r/gamedev/comments/2rrie6/ecs_and_observer_pattern/
* https://www.reddit.com/r/gamedev/comments/65qhd0/event_queues_vs_observerssubjects_in_entity/

more thinking required...

### Interim Observer Solution

Is to pass a parameter to `dirty()` which 
tells us which model each mediator entity cares about, like observer pattern mappings.

Note this uses the model component ref class, rather than anything about the model dict itself.
We even have arbitrary keys which are more verbose model descriptions to make it easier.

```python
dirty_model_to_entities = {
    MW: [entity_welcome_left, entity_welcome_user_right, entity_edit_welcome_msg],
    "welcome outputs only": [entity_welcome_left, entity_welcome_user_right],
    MU: [entity_welcome_user_right, entity_edit_user_name_msg],
    MUS: [entity_welcome_user_right, entity_edit_user_surname_msg],
    "just top right": [entity_welcome_user_right],
}
```
SEE HEAPS MORE DOCO IN THE `esper_observer.py` file.

## Dirty Observer 
Extracted here: (copy only - the file is the master, not this)

Alternative to the Observer pattern. Rather than the traditional model.addObserver(mediator)
we instead add_dependency(signal, mediators). Instead of a setter on the model broadcasting
to all interested observers, it is the responsibility of the users of the model to
explicitly call dirty(signal) which actually doesn't broadcast, 
but instead simply adds a Dirty component to the relevant observers - only a
world.process() will trigger processing by the systems of the Dirty mediators 
(or in ECS speak, mediator entities who have the Dirty component attached.)

The burden on the users of the model is not so bad, because we can create arbitrary
dependencies from arbitrary signal names, using add_dependency(), and list multiple
dependant entities (mediators).  Typically a signal name would be the component
class specific to a model aspect, however its often also useful to have arbitrary 
signal names (strings) which are descriptive of the spefic subset of mediators we are
targeting.

### Benefits over a traditional Observer system:

We centralise all the dependencies in one data structure 'affected_entities' rather
than having each model inherit from Observable and do its own secret thing. This potentially
makes things easier to debug and reason about.

Dirty concept marks mediators but doesn't do anything till later, thus allowing all our
gui updates to happen at a time of our choosing rather than immediately after each model setter.

DirtyObserver can be used with simple model classes, even pure data structures ! 
because it doesn't require that the model be a special kind of 
class, which inherits from Observable.  It thus doesn't require the model to be 
interspersed with observers.Notify() broadcast calls within itself.

### Similarities:

The builder of the application has to register dependencies between models and mediators.
Traditionally done by model.addObserver(), here done by add_dependency(). 

### Downsides:

However the traditional approach was set and forget, whereas the new approach requires
that the user of the model send a signal, albiet a usefully abstract named one.

The traditional approach auto broadcasted, whereas the new approach needs an explicit
call to world.process()

Both these downsides mean that the traditional

```python
# one time setup
model.addObserver(mediator)

model.info = 100
```

is enough to trigger the mediator whereas the new system requires

```python
# one time setup
do = DirtyObserver()
do.add_dependency('model info changed', mediator)

model.info = 100
do.dirty('model info changed')  # downside, but at least its explicit not magical
world.process()                 # downside, but can be deferred, which is a benefit
```

to achive the same thing.


## View Model in the future?

```python
# Not used - but would be nice to integrate something like this into the ECS
view_model = {
    "uppercase welcome model": False,
    "uppercase welcome outputs": False,
    "uppercase top right": False,
}
```

But no point adding more and more complexity till the flaws are worked out, or this approach
abandoned.

# Evaluation So Far - Flaws

The implementation is quite big and complex with some flaws:

The render 'system' is picking up the same mediators multiple times because if a mediator has components A, B, C and you are just looking for A, B then you will pick it up - both in the A,B pass and also in the A,B,C pass.
This means multiple renderings of the same info - inefficient!

For each model element we have to add a unique component.

The hacky observer implementation means maintaining a table of keys to mediator entities affected, including adding helpfully named special keys for special situations. Whilst this is hacky and ongoing, at least the table nicely centralises and summarises what KEY affects what.  The events need to call dirty(KEY).

Needing to call `world.process()` after each event is a bit annoying. On the other hand we have the opportunity to delay calling that and putting it into some other background update loop.  Possibly integrate it with the main wx loop, the way I once did with pygame and the way wxasync library does.

Adding addition components like `UPR()` to mediator entities to flag extra mediator behaviour like performing an uppercase operation seems a little extreme - was thinking that a simple flag on an existing component would be better?

### SUMMARY OF WHAT'S BAD
The explosion of components is a worry, and the duplicate renderings is a worry.
The additional components just to flag uppercase etc. is a bit much.

### SUMMARY OF WHAT'S GOOD
What's nice is the setup of the mediators is quite clear and centralised e.g.

```python
world.add_component(entity_welcome_left, MW(model=model, key="welcome_msg"))
world.add_component(entity_welcome_left, GUIST(ref=frame.m_staticText1))

world.add_component(entity_welcome_user_right, MW(model=model, key="welcome_msg"))
world.add_component(entity_welcome_user_right, MU(model=model["user"], key="name"))
world.add_component(entity_welcome_user_right, MUS(model=model["user"], key="surname"))
world.add_component(entity_welcome_user_right, GUIST(ref=frame.m_staticText2))

# etc.
```

## Multiple Systems

We now have multiple systems doing a staged approach. E.g. A compute text stage which creates a final component containing the string to render.  The render stage then only targets those final components.  Seems to work and feels a bit better.

# Retrospective on Component types

Components for entities (mediators) represent
- how to get to specific bits of models information (model obj or dict, key) - different components need to be created for each model field to allow targeted behaviour.  If targeted behaviour is not necessary that more course grained components could be used.
- how to get to gui widgets (gui ref components) - different ones for each gui widget type e.g. static vs textentry
- flags for whether a system should render e.g. `Dirty` component
- flags for extra transformations like uppercase something

So in a sense, a traditional mediator would be an class containing

    class Mediator:
        model reference
        gui reference

a component approach makes a mediator a mere entity with the components

    model ref component
        model reference
    gui ref component
        gui reference

Note that a model reference could be a single pointer to a field if the model is an object, or a combination of dict reference and a key, if the model is a dict.

Note that a gui reference is simply a reference to a widget control e.g. `GuiStaticText(ref=frame.m_staticText2)`

# View Model

Something like

```python
view_model = {
    "uppercase welcome model": False, 
    "uppercase welcome outputs": False, 
    "uppercase top right": False
}
```

## In ECS
Not used - but would be nice to integrate something like this into the ECS
but then again, the data components attached to a mediator entity is like a view model, so
why replicate that information uncessessarily.

## In MVC
Not used - but would be nice to integrate something like this into the MVC
but then again, the mediators themselves have these attributes, each mediator entity is like a view model, so
why replicate that information uncessessarily.

# The model

The only reason we have a deep model like this, is because it is shared and manipulated by
many things.  Other 'model' data bits can be put into components directly as a sole place.

ECS version:

```python
model = {"welcome_msg": "Welcome", "user": {"name": "Sam", "surname": "Smith"}}
```

MVC version:

A bunch of models classes, implementing Observer.

# Learnings from the javascript version

Both the Python and Javascript 'extract' systems extract the same entities several times, which is redundant. 

Python:

    --Model Extract System---
    have set ComponentModelWelcome(model={'welcome_msg': 'Welcome', 'user': {'name': 'Sam', 'surname': 'Smith'}}, key='welcome_msg', finalstr='Welcome') for mediator for welcome_left
    have set ComponentModelWelcome(model={'welcome_msg': 'Welcome', 'user': {'name': 'Sam', 'surname': 'Smith'}}, key='welcome_msg', finalstr='Welcome') for mediator for welcome_user_right
    have set ComponentModelWelcome(model={'welcome_msg': 'Welcome', 'user': {'name': 'Sam', 'surname': 'Smith'}}, key='welcome_msg', finalstr='Welcome') for mediator for edit_welcome_msg
    have set ComponentModelFirstname(model={'name': 'Sam', 'surname': 'Smith'}, key='name', finalstr='Sam') for mediator for welcome_user_right
    have set ComponentModelFirstname(model={'name': 'Sam', 'surname': 'Smith'}, key='name', finalstr='Sam') for mediator for edit_user_name_msg
    have set ComponentModelSurname(model={'name': 'Sam', 'surname': 'Smith'}, key='surname', finalstr='Smith') for mediator for welcome_user_right
    have set ComponentModelSurname(model={'name': 'Sam', 'surname': 'Smith'}, key='surname', finalstr='Smith') for mediator for edit_user_surname_msg

Javascript:

    3 c_welcome.finalstr Welcome
    2 main.js:52 c_firstname.finalstr Sam
    2 main.js:56 c_surname.finalstr Smith

This is because we are matching entities (mediators) that have the component e.g. c_welcome - which is basically many entities.  Actually now that I think about it - perhaps this is the CORRECT behaviour since each mediator has its own copy!

## Trying to make systems more efficiently in Javascript

Fails because the `jecs` framework has a particular way of building systems that does not lend itself to meta looping around it:

This Python technique:

```python
for Component in (ComponentModelWelcome, ComponentModelFirstname, ComponentModelSurname):
  for ent, (component, _) in self.world.get_components(Component, Dirty):
    component.finalstr = component.model[component.key]
    logsimple(component, ent)
```

does not translate well into 

```javascript
for (let component of ['c_welcome', 'c_firstname', 'c_surname']) {
  let processor_name = 'extract-' + component + '-processor'
  world.system(processor_name, [component], (entity, {componentXXXXXXXXX}) => {
    entity.finalstr = component.model[component.key]
    console.log("entity.finalstr", entity.finalstr)
  });
}
```

because the ATTEMPT AT JAVASCRIPT TRANSLATION DOESN'T WORK BECAUSE componentXXXXXXXXX NEEDS TO BE A VARIABLE NOT A STRING

