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
    Tells us which model each mediator entity cares about, like observer pattern mappings.
    Note this uses the model component ref class, rather than anything about the model dict itself
    We even have arbitrary keys which are more verbose model descriptions to make it easier
    """
    affected_entities = {}
    mediators: List
    world: esper.World

    def add_dependency(self, signal, entities: List):
        self.affected_entities[signal] = entities

    def dirty_all(self, condition=True):
        add_or_remove_component(self.world, condition, Dirty, entities=self.mediators)

    def dirty(self, component_class):
        for mediator in self.affected_entities[component_class]:
            print(f"dirty: {mediator} because {component_class}")
            self.world.add_component(mediator, Dirty())

