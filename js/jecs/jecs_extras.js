function add_or_remove_component(world, condition, component_c_ref, component_Class, entities) {
    // Adds or removes component from each entity in list, depending on condition
    // AHA only works if there are no parameters, which is fine for Flag component use
    for (let ent of entities) {
        if (condition)
            ent.setComponent(component_c_ref, new component_Class());  // will creating a class instance like this work?
        else {
            if (ent.hasComponent(component_c_ref))
                ent.deleteComponent(component_c_ref)
        }
    }
}
