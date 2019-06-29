wx_esper
========

An attempt to use esper ECS for traditional GUI programming.

A modern GUI framework with a model to render might traverse the model and shove
information into the gui controls.  Click and other events might make changes to
the gui widgets directly from then on, or more properly, update the model and then
reflect those changes into the widgets.  
A downside of this naive approach is that if the model is changed by other means
(not by gui clicks but by other parts of the software system) then those changes are
not reflected in the gui.

A MGM pattern approach would have any changes to the model via setters notify
mediators whose job it is to update the gui widgets.  Click and other events thus
need only make changes to the model and the model will notify the mediators as necessary.

To implement the MGM pattern using an ECS (entity component system) architectural
approach is conceptually challenging, because ECS has its roots in game architectures
where entities are game objects which are typically sprites which are rendered by 'systems'
which draw onto a canvas.  How do models, mediators and gui widgets map to ECS concepts,
and how to we remove most of the OO from them, in order to do things the ECS way?

Using ECS approach to implement the MGM design pattern.
-------------------------------------------------------

Whilst there are many possible solutions, the cleanest solution which might be able to be
used across a whole application in a way that makes use of the benefits of ECS is as follows.

Untangle the OO data and behaviour of the mediator. The mediator becomes a mere entity, with its
previous data as a component, and its previous behaviour in a system.

Gui OO widgets are supplied by the framework e.g. wxPython or HTML/DOM and remain unchanged.

OO Models are as they were, or they can be converted to nested dictionaries, it doesn't matter.
If ECS is being used in other areas of your application, then your OO model object might turn
into entities with their own components - not really relevant to this project.

Thus
----
Entities are the mediators, with components being things like model references, gui widget 
references. This is the data that the mediator typically needs, except its broken out as components.

The system contains the code/behaviour of the mediator, which pulls things out of the model and 
into a widget.  Currently we are cheating and have a single Render system which scans for
certain combination of components and knows what to do with them.

The checkbox and button events change the model, then in the asence of a observer pattern,
simply trigger a world.process() to render.  A bit inefficient, but I hope to introduce a dirty flag.

Behaviour we are modelling
--------------------------

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

On Observers and Dirty
----------------------
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
