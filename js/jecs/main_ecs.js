//
// Model - The Welcome model and User model are Observable.
//

model = {
  welcomemsg: "Welcome", 
  user: {
    firstname: "Sam", 
    surname: "Smith"
  }
}
display_options = {
  uppercase_welcome: false,
  uppercase_user: false,
  uppercase_welcome_user: false,
}

const world = new Ecs();

class ModelRef {  // Mediator (entity + this component) needs to know about model. Model specific
  constructor(model, key) {
    this.model = model;
    this.key = key;
    this.finalstr = "";
  }
}
class MultiModelRef {  // Refers to multiple model fields, since can only have one component per entity can't have multiple ModelRefs
  constructor(refs) {
    this.refs = refs;  // list of ModelRef
  }
}

class GuiControlRef {  // Mediator (entity + this component) needs to know about a wxPython gui control
  constructor(ref) {
    this.ref = ref
  }
}
class ComponentGuiDiv extends GuiControlRef {}
class ComponentGuiInput extends GuiControlRef {}

class Flag {}  // Mediator (entity + this component) might have a flag to indicate some behaviour is wanted
class ComponentUppercaseWelcome extends Flag {}
class ComponentUppercaseUser extends Flag {}
class ComponentUppercaseWelcomeUser extends Flag {}

//
// Wire up and build everything
//

const entity_welcome_left = world.entity('entity_welcome_left')
entity_welcome_left.setComponent('c_model_ref', new ModelRef(model, 'welcomemsg'))
entity_welcome_left.setComponent('c_gui_div', new ComponentGuiDiv('welcome'))  // id of div to hold welcome message, top left

const entity_welcome_user_right = world.entity('entity_welcome_user_right')
entity_welcome_user_right.setComponent('c_multi_model_ref', new MultiModelRef(
  [
    new ModelRef(model, 'welcomemsg'),
    new ModelRef(model["user"], 'firstname'),
    new ModelRef(model["user"], 'surname'),
  ]
));
entity_welcome_user_right.setComponent('c_gui_div', new ComponentGuiDiv('welcome-user'));  // id of div to hold welcome + user message, top right

const entity_edit_welcome_msg = world.entity('entity_edit_welcome_msg')
entity_edit_welcome_msg.setComponent('c_model_ref', new ModelRef(model, 'welcomemsg'));
entity_edit_welcome_msg.setComponent('c_gui_input', new ComponentGuiInput('welcome'));  // name (not id) of input to hold welcome message

const entity_edit_user_name_msg = world.entity('entity_edit_user_name_msg')
entity_edit_user_name_msg.setComponent('c_model_ref', new ModelRef(model["user"], 'firstname'));
entity_edit_user_name_msg.setComponent('c_gui_input', new ComponentGuiInput('firstname'));  // name (not id) of input to hold first name

const entity_edit_user_surname_msg = world.entity('entity_edit_user_surname_msg')
entity_edit_user_surname_msg.setComponent('c_model_ref', new ModelRef(model["user"], 'surname'));
entity_edit_user_surname_msg.setComponent('c_gui_input', new ComponentGuiInput('surname'));  // name (not id) of input to hold first name

const entity_dump_models = world.entity('entity_dump_models')
entity_dump_models.setComponent('c_models_to_dump', {});  // possibly fill this in

// Extract systems - pull info from model into component 'finalstr' field for later manipulation by other systems

world.system('extract-model-ref-system', ['c_model_ref'], (entity, {c_model_ref}) => {
  // Tip - the variables receiving the component must be named exactly the same as the component name
  c_model_ref.finalstr = c_model_ref.model[c_model_ref.key]
  console.log("c_model_ref.finalstr", c_model_ref.finalstr)
});
world.system('extract-multi-model-ref-system', ['c_multi_model_ref'], (entity, {c_multi_model_ref}) => {
  for (const c_model_ref of c_multi_model_ref.refs) {
    c_model_ref.finalstr = c_model_ref.model[c_model_ref.key]
    console.log("c_model_ref.finalstr", c_model_ref.finalstr)
  }
});

// Case transform systems

world.system('case-transform-uppercase-welcome', ['c_model_ref', 'c_uppercase_welcome'], (entity, {c_model_ref, c_uppercase_welcome}) => {
  if (c_model_ref.key == "welcomemsg")
    c_model_ref.finalstr = c_model_ref.finalstr.toUpperCase()
});
world.system('case-transform-uppercase_welcome_user_welcome', ['c_multi_model_ref', 'c_uppercase_welcome'], (entity, {c_multi_model_ref, c_uppercase_welcome}) => {
  for (const c_model_ref of c_multi_model_ref.refs)
    if (c_model_ref.key == "welcomemsg")
      c_model_ref.finalstr = c_model_ref.finalstr.toUpperCase()
});
world.system('case-transform-uppercase_welcome_user_user', ['c_multi_model_ref', 'c_uppercase_user'], (entity, {c_multi_model_ref, c_uppercase_user}) => {
  for (const c_model_ref of c_multi_model_ref.refs)
    if (c_model_ref.key == "firstname" || c_model_ref.key == "surname")
      c_model_ref.finalstr = c_model_ref.finalstr.toUpperCase()
});
world.system('case-transform-uppercase_all', ['c_multi_model_ref', 'c_uppercase_welcome_user'], (entity, {c_multi_model_ref, c_uppercase_welcome_user}) => {
  for (const c_model_ref of c_multi_model_ref.refs)
    c_model_ref.finalstr = c_model_ref.finalstr.toUpperCase()
});

// Render Systems

world.system('render-system-top-left', ['c_model_ref', 'c_gui_div'], (entity, {c_model_ref, c_gui_div}) => {
  if (c_model_ref.key == "welcomemsg")
    $('#' + c_gui_div.ref).html(c_model_ref.finalstr)
});

let msg = {}  // can't target how model ref components get found, so build up what we need here
world.system('render-system-top-right', ['c_multi_model_ref', 'c_gui_div'], (entity, {c_multi_model_ref, c_gui_div}) => {
  for (const c_model_ref of c_multi_model_ref.refs)
    msg[c_model_ref.key] = c_model_ref.finalstr
  $('#' + c_gui_div.ref).html(`${msg['welcomemsg']} ${msg['firstname']} ${msg['surname']}`)
});

world.system('render-system-text-inputs', ['c_model_ref', 'c_gui_input'], (entity, {c_model_ref, c_gui_input}) => {
  $(`input[name=${c_gui_input.ref}]`).val(c_model_ref.finalstr)
});

world.system('render-system-dump-models', ['c_models_to_dump'], (entity, {c_models_to_dump}) => {
  // could pass in some info in c_models_to_dump but let's not, just grab what we need from globals etc.

  let info = {
    model: model,
    display_options: display_options,
  }
  let part1 = syntaxHighlight(JSON.stringify(info, null, 2))

  
  info = {entities: {}}
  // info.entities = Object.entries(world.entities) // this becomes circular, so loop through ourselves instead
  for (ent of Object.entries(world.entities)) {
    let entity_name = ent[0]
    let entity = ent[1]

    if (c_models_to_dump.verbose)
      info.entities[entity_name] = Object.entries(entity.components)
    else
      info.entities[entity_name] = Object.keys(entity.components)
  }
  let part2 = syntaxHighlight(JSON.stringify(info, function(key, value) {
    // skip observers or circular references that will break the json dump

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

  $('#debug_info').html(part1 + '<br>' + part2)
});

// Util

function model_setter_welcome(msg) {
    model["welcome_msg"] = msg
    model_welcome_toggle()
}

function isUpperCaseAt(str, n) {
  return str[n]=== str[n].toUpperCase();
}

//
// GUI events
//

$('#change_welcome_model').on('click', function(e) {
  model.welcomemsg = isUpperCaseAt(model.welcomemsg, 1) ? model.welcomemsg.toLowerCase() : model.welcomemsg.toUpperCase()
  world.tick()
})

$('#change_user_model').on('click', function(e) {
  model.user.firstname = isUpperCaseAt(model.user.firstname, 1) ? model.user.firstname.toLowerCase() : model.user.firstname.toUpperCase()
  model.user.surname = isUpperCaseAt(model.user.surname, 1) ? model.user.surname.toLowerCase() : model.user.surname.toUpperCase()
  world.tick()
})

$('#reset_welcome_model').on('click', function(e) {
  model.welcomemsg = "Hello"
  world.tick()
})

$('#reset_user_model').on('click', function(e) {
  model.user.firstname = "Fred"
  model.user.surname = "Flinstone"
  world.tick()
})

$("input[name=uppercase_welcome]").change(function(e) {
  display_options.uppercase_welcome = $(e.target).prop('checked')

  // above is redundant because component has this info
  add_or_remove_component(world, 
    $(e.target).prop('checked'), 
    'c_uppercase_welcome', 
    ComponentUppercaseWelcome, 
    [entity_welcome_left, entity_welcome_user_right])
  world.tick()
})

$("input[name=uppercase_user]").change(function(e) {
  display_options.uppercase_user = $(e.target).prop('checked')

  // above is redundant because component has this info
  add_or_remove_component(world, 
    $(e.target).prop('checked'), 
    'c_uppercase_user', 
    ComponentUppercaseUser, 
    [entity_welcome_user_right])  
  world.tick()
})

$("input[name=uppercase_welcome_user]").change(function(e) {
  display_options.uppercase_welcome_user = $(e.target).prop('checked')
  // above is redundant because component has this info
  add_or_remove_component(world, 
    $(e.target).prop('checked'), 
    'c_uppercase_welcome_user', 
    ComponentUppercaseWelcomeUser, 
    [entity_welcome_user_right])
  world.tick()
});

$("input[name=verbose_debug]").change(function(e) {
  let component = {verbose: $(e.target).prop('checked')}
  entity_dump_models.setComponent('c_models_to_dump', component)  // replaces any existing component
  world.tick()
});

$("input[name=welcome]").keypress(function(e) {
    model["welcomemsg"] = $(e.target).val()
    world.tick()
})

$("input[name=firstname]").keypress(function(e) {
  model["user"]["firstname"] = $(e.target).val()
  world.tick()
})

$("input[name=surname]").keypress(function(e) {
  model["user"]["surname"] = $(e.target).val()
  world.tick()
})

$('#render-now').on('click', function(e) {
  world.tick()
})

world.tick()
