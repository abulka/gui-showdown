def add_or_remove_component(world, condition: bool, component_Class, entities: list):
    # Adds or removes component from each entity in list, depending on condition
    for ent in entities:
        if condition:
            world.add_component(ent, component_Class())
        else:
            if world.has_component(ent, component_Class):
                world.remove_component(ent, component_Class)

"""
example uses of above, now no longer used


add_or_remove_component(
    world,
    condition=event.GetEventObject().IsChecked(),
    component_Class=ComponentUppercaseWelcome,
    entities=[entity_welcome_left, entity_welcome_user_right],
)

add_or_remove_component(
    world,
    condition=event.GetEventObject().IsChecked(),
    component_Class=ComponentUppercaseUser,
    entities=[entity_welcome_user_right],
)

add_or_remove_component(world, 
    condition=event.GetEventObject().IsChecked(), 
    component_Class=ComponentUppercaseAll, entities=[entity_welcome_user_right])


P.S. instead of adding or removing components to flag things, I now add an options component to all relevant entities
and update it.  Makes the system logic simpler (checking for less component types means less systems/system loops). Also
less components to track.  

Also turns out less flags needed e.g. uppercase_all was removed. A global display options still needs 'uppercase all
viz. uppercase welcome and user on the rhs.' but when each entity has its own display options, just those two flags PER
ENTITY give more info and the third flag is not needed, because we know the context of the two flags, whereas in a
global dict two flags apply to all entities and we can't figure out a special case for the top right message unless we
introduce that extra flag.

"""

