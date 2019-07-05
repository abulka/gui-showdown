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

    affected_entities = {}  # component or str -> [entities]
    world: esper.World

    def add_dependency(self, signal, entities: List):
        # signal can be anything, usually a component class, sometimes a string
        self.affected_entities[signal] = entities

    def dirty_all(self, condition=True, entities=None):
        add_or_remove_component(self.world, condition, component_Class=Dirty, entities=entities)

    def dirty(self, Component, component_filter_f=None, filter_nice_name=""):
        """
        Add the 'Dirty' component to all entities which have registered to be dependent on param 'Component'. 
        
            world:
                entity1 : [Component1-instance, Component2-instance, Dirty]
                                                                     ^^^^^

        Dependencies are managed via 'affected_entities' which is a custom mapping of 'observer' relationships between: 

            component or str -> [entities]

        The idea is that if you modify the data in a particular component 'Component', then the entity is marked Dirty.

        Similarly, if you modify the data in a model that various components of type 'Component' refer to, 
        then all entities containing that Component are marked Dirty.

        ## Example

        Given the world

            world:
                entity1 : [Component1-instance, Component2-instance]
                entity2 : [Component1-instance]
                entity3 : [Component2-instance]

        then calling

            dirty(Component1)

        would result in all entitites containing Component1 *instances* being marked Dirty:

            world:
                entity1 : [Component1-instance, Component2-instance, Dirty]         <--- Dirty added 👍
                entity2 : [Component1-instance, Dirty]                              <--- Dirty added 👍
                entity3 : [Component2-instance]                                     <--- not Dirty

        ## Filtering 

        If supplied, a filtering lambda is called on each instance of Component found, which reduces the number of
        entities affected, because only Component instances that match the filter are counted.  Ideally the filter looks
        at a particular Component instance attribute. 
        
        Thus if there are 10 entities each with a ModelRef component, each of which has a unique 'key' value, the custom
        'affected_entities' entry would look like
        
            ModelRef -> [entity1 ... entity10],
        
        but ideally and abstractly should look like this, to be efficient
        
            ModelRef, with key=a -> [entity1],
            ModelRef, with key=b -> [entity2],
            ModelRef, with key=c -> [entity3, entity4],

        and ideally, to mark things as dirty we call something like 
        
            dirty("ModelRef, with key=b")
            
        But this is not a good implementation because one would have to have 10 entries in the 'affected_entities' dict,
        one for each unique key.
        
        By using the filtering implementation, we keep the original idea of having a single entry in the
        'affected_entities' dict (which is nicer than having 10 separate entries, albiet that single entry does have a
        lot of entities listed in the entitity dependencies list)
        
            ModelRef -> [entity1 ... entity10],

        and instead we call

            dirty(ModelRef, 
                  lambda component : component.key == "surname",     <--- this is the magic lambda
                  filter_nice_name="surname")

        Note: 'filter_nice_name' is a nice printable name for the lambda e.g. what key it is using, for logging purposes.

        ## Using a string instrad of Component type as a dirty signal (param to dirty)

        Component can be a string instead of a Component class type.  This allows for custom more nuanced 'affected_entities'
        mappings.  Filters are not applicable to dirty() calls involving such strings, because caller 

            do.add_dependency("just top", [entity_welcome_left, entity_welcome_user_right])

            do.dirty("just top", 
                     lambda component : component.key == "surname"  <---- doesn't make sense cos can't find component based on str signal
                     )

        What would such a lambda mean?  It can't receive a component instance because a string signal just gives us a list of
        entities to dirty - no components involved.  We just intend to add Dirty to each entity. viz. let's walk through the logic:
        dirty() would look at the first entity 'entity_welcome_left' and since it is not a Component type, it is impossible to 
        try to retrieve a Component instance for that specific Entity.
        """

        # Logging
        filter_msg = f"filter '{filter_nice_name}'" if component_filter_f else "no filter"
        print(f"dirty called on dependent entities of Component={Component} which are {self.affected_entities[Component]} with", filter_msg)

        for entity in self.affected_entities[Component]:
            add_dirty = True
            
            if component_filter_f and type(Component) != str:
                try:
                    component = self.world.component_for_entity(entity, Component)  # retrieve an actual Component instance for a specific Entity
                except KeyError:
                    raise RuntimeError(f"Error in the affected_entities dict: entity {entity} should not be listed as depending on {Component}.")
                add_dirty = component_filter_f(component)  # call the filter, passing the component instance, to see if this entity should be skipped

            if add_dirty:
                print(f"\tcomponent Dirty added to entity {entity}")
                self.world.add_component(entity, Dirty())
