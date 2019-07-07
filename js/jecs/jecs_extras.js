function add_or_remove_component(world, condition, component_c_ref, component_Class, entities) {
    // Adds or removes component from each entity in list, depending on condition
    // AHA only works if there are no parameters, which is fine for Flag component use
    for (let ent of entities) {
        if (condition)
            ent.setComponent(component_c_ref, new component_Class());  // adds a new component
        else {
            if (ent.hasComponent(component_c_ref))
                ent.deleteComponent(component_c_ref)
        }
    }
}

function dump_world(world, verbose) {

    info = {entities: {}}
    
    // info.entities = Object.entries(world.entities) // this becomes circular, so loop through ourselves instead
    for (ent of Object.entries(world.entities)) {
      let entity_name = ent[0]
      let entity = ent[1]
      info.entities[entity_name] = verbose ? Object.entries(entity.components) : Object.keys(entity.components)
    }

    // syntax hightlight, but use filter to skip observers or circular references that will break the json dump
    return syntaxHighlight(JSON.stringify(info, function(key, value) {
  
      if (key == 'model') { 
        return '<see above>'
      } 
      else if (key == 'entity_dump_models') {
        return undefined  // this entity used to debug dump the world, don't list it in debug info
      } 
      else {
        return value;
      }
  
    }, 2))
}