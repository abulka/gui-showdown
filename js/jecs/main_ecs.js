//
// Model
//

var model = {
  welcomemsg: "Welcome", 
  user: {
    firstname: "Sam", 
    surname: "Smith"
  }
}

const world = new Ecs();

//
// Components
//

class ModelRef {  // Reference to a shared model object
  constructor(model, keys) {
    this.model = model;  // any object/dict
    this.keys = keys;  // ['a', 'b'] would refer to model.a.b
    this.finalstr = "";
  }

  // dynamically access or set nested dictionary keys

  get val() {
    let data = this.model
    for (let k of this.keys)
      data = data[k]
    return data
  }

  set val(val) {
    let data = this.model
    let numkeys = this.keys.length
    let lastkey = this.keys.slice(-1)
    for (let k of this.keys.slice(0, numkeys - 1))  // for assignment drill down to *second* last key
      data = data[k]
    data[lastkey] = val
  }
}

// Quick test of ModelRef
m = new ModelRef(model, ["user", "firstname"])
assert(m.val == "Sam")
m.val = "Mary"
assert(m.val == "Mary")


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
class Flag {}  // Mediator (entity + this component) might have a flag to indicate some behaviour is wanted

//
// Wire up and build everything
//

const entity_welcome_left = world.entity('entity_welcome_left')
entity_welcome_left.setComponent('c_model_ref', new ModelRef(model, ['welcomemsg']))
entity_welcome_left.setComponent('c_gui_div', new GuiControlRef('welcome'))  // id of div to hold welcome message, top left

const entity_welcome_user_right = world.entity('entity_welcome_user_right')
entity_welcome_user_right.setComponent('c_multi_model_ref', new MultiModelRef(
  [
    new ModelRef(model, ['welcomemsg']),
    new ModelRef(model, ["user", "firstname"]),
    new ModelRef(model, ["user", "surname"]),
  ]
));
entity_welcome_user_right.setComponent('c_gui_div', new GuiControlRef('welcome-user'));  // id of div to hold welcome + user message, top right

const entity_edit_welcome_msg = world.entity('entity_edit_welcome_msg')
entity_edit_welcome_msg.setComponent('c_model_ref', new ModelRef(model, ['welcomemsg']));
entity_edit_welcome_msg.setComponent('c_gui_input', new GuiControlRef('welcome'));  // name (not id) of input to hold welcome message

const entity_edit_user_name_msg = world.entity('entity_edit_user_name_msg')
entity_edit_user_name_msg.setComponent('c_model_ref', new ModelRef(model, ["user", "firstname"]));
entity_edit_user_name_msg.setComponent('c_gui_input', new GuiControlRef('firstname'));  // name (not id) of input to hold first name

const entity_edit_user_surname_msg = world.entity('entity_edit_user_surname_msg')
entity_edit_user_surname_msg.setComponent('c_model_ref', new ModelRef(model, ["user", "surname"]));
entity_edit_user_surname_msg.setComponent('c_gui_input', new GuiControlRef('surname'));  // name (not id) of input to hold first name

const entity_dump_models = world.entity('entity_dump_models')
entity_dump_models.setComponent('c_debug_dump_options', {verbose: false});  // dict as component is ok

// Extract systems - pull info from model into component 'finalstr' field for later manipulation by other systems

world.system('extract-model-ref-system', ['c_model_ref'], (entity, {c_model_ref}) => {
  // Tip - the variables receiving the component must be named exactly the same as the component name
  let c = c_model_ref
  c.finalstr = c.val
});
world.system('extract-multi-model-ref-system', ['c_multi_model_ref'], (entity, {c_multi_model_ref}) => {
  for (const c of c_multi_model_ref.refs) {  // each 'c' is a ModelRef component 
    c.finalstr = c.val
  }
});

// Case transform systems

world.system('case-transform-uppercase-welcome', ['c_model_ref', 'c_uppercase_welcome'], (entity, {c_model_ref, c_uppercase_welcome}) => {
  let c = c_model_ref
  if (c.keys.includes("welcomemsg"))
    c.finalstr = c.finalstr.toUpperCase()
});
world.system('case-transform-uppercase_welcome_user_welcome', ['c_multi_model_ref', 'c_uppercase_welcome'], (entity, {c_multi_model_ref, c_uppercase_welcome}) => {
  for (const c of c_multi_model_ref.refs)  // each 'c' is a ModelRef component 
    if (c.keys.includes("welcomemsg"))
      c.finalstr = c.finalstr.toUpperCase()
});
world.system('case-transform-uppercase_welcome_user_user', ['c_multi_model_ref', 'c_uppercase_user'], (entity, {c_multi_model_ref, c_uppercase_user}) => {
  for (const c of c_multi_model_ref.refs)  // each 'c' is a ModelRef component 
    if (c.keys.includes("firstname") || c.keys.includes("surname"))
      c.finalstr = c.finalstr.toUpperCase()
});
world.system('case-transform-uppercase_welcome_user', ['c_multi_model_ref', 'c_uppercase_welcome_user'], (entity, {c_multi_model_ref, c_uppercase_welcome_user}) => {
  for (const c of c_multi_model_ref.refs)  // each 'c' is a ModelRef component
    c.finalstr = c.finalstr.toUpperCase()
});

// Render Systems

world.system('render-system-top-left', ['c_model_ref', 'c_gui_div'], (entity, {c_model_ref, c_gui_div}) => {
  if (c_model_ref.keys.includes("welcomemsg"))
    $('#' + c_gui_div.ref).html(c_model_ref.finalstr)
});

let msg = {}  // can't target how model ref components get found, so build up what we need here
world.system('render-system-top-right', ['c_multi_model_ref', 'c_gui_div'], (entity, {c_multi_model_ref, c_gui_div}) => {
  for (const c_model_ref of c_multi_model_ref.refs)
    msg[c_model_ref.keys.slice(-1)] = c_model_ref.finalstr
  $('#' + c_gui_div.ref).html(`${msg['welcomemsg']} ${msg['firstname']} ${msg['surname']}`)
});

world.system('render-system-text-inputs', ['c_model_ref', 'c_gui_input'], (entity, {c_model_ref, c_gui_input}) => {
  $(`input[name=${c_gui_input.ref}]`).val(c_model_ref.finalstr)
});

world.system('render-system-dump-models', ['c_debug_dump_options'], (entity, {c_debug_dump_options}) => {
  let part1_html = syntaxHighlight(JSON.stringify({model: model}, null, 2))
  let part2_html = dump_world(world, c_debug_dump_options.verbose)
  $('#debug_info').html(part1_html + '<br>' + part2_html)
});

// Util

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
  add_or_remove_component(world, 
    $(e.target).prop('checked'), 
    'c_uppercase_welcome', 
    Flag, 
    [entity_welcome_left, entity_welcome_user_right])
  world.tick()
})

$("input[name=uppercase_user]").change(function(e) {
  add_or_remove_component(world, 
    $(e.target).prop('checked'), 
    'c_uppercase_user', 
    Flag, 
    [entity_welcome_user_right])  
  world.tick()
})

$("input[name=uppercase_welcome_user]").change(function(e) {
  add_or_remove_component(world, 
    $(e.target).prop('checked'), 
    'c_uppercase_welcome_user', 
    Flag, 
    [entity_welcome_user_right])
  world.tick()
});

$("input[name=verbose_debug]").change(function(e) {
  let component = {verbose: $(e.target).prop('checked')}
  entity_dump_models.setComponent('c_debug_dump_options', component)  // replaces any existing component
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
