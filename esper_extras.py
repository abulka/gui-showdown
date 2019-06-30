def add_or_remove_component(world, condition: bool, component_Class, entities: list):
    # Adds or removes component from each entity in list, depending on condition
    for ent in entities:
        if condition:
            world.add_component(ent, component_Class())
        else:
            if world.has_component(ent, component_Class):
                world.remove_component(ent, component_Class)

 