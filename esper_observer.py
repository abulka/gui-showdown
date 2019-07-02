from dataclasses import dataclass
from typing import List
from esper_extras import add_or_remove_component
import esper


@dataclass
class Dirty:  # Mark that component needs rendering
    pass


@dataclass
class DirtyObserver:
    """
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
    """

    affected_entities = {}
    world: esper.World

    def add_dependency(self, signal, entities: List):
        # signal can be anything, usually a component class, sometimes a string
        self.affected_entities[signal] = entities

    def dirty_all(self, condition=True, entities=None):
        add_or_remove_component(self.world, condition, component_Class=Dirty, entities=entities)

    def dirty(self, signal):
        for mediator in self.affected_entities[signal]:
            print(f"dirty: {mediator} because of {signal}")
            self.world.add_component(mediator, Dirty())
