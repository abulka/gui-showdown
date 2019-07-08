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

class ModelRef extends NestedDictAccess {  // Reference to a shared model object
  constructor(model, keys) {
    super(model, keys)
    this.finalstr = "";
  }
}

class MultiModelRef {  // Refers to multiple model fields, since can only have one component per entity can't have multiple ModelRefs
  constructor(refs) {
    this.refs = refs;  // list of ModelRefs
  }
}

class GuiControlRef {  // Mediator (entity + this component) needs to know about a wxPython gui control
  constructor(el, eltype) {
    this.el = el          // JQuery reference to element
    this.eltype = eltype  // e.g. 'div' or 'input', tells render system what kind of DOM element to render/set
  }
}

class DisplayOptions {
  constructor() {
    this.uppercase_welcome = false
    this.uppercase_user = false
  }
}

//
// Wire up and build everything
//

const entity_welcome_left = world.entity('entity_welcome_left')
entity_welcome_left.setComponent('c_model_ref', new ModelRef(model, ['welcomemsg']))
entity_welcome_left.setComponent('c_gui_ref', new GuiControlRef($('#welcome'), 'div'))  // id of div to hold welcome message, top left
entity_welcome_left.setComponent('c_display_options', new DisplayOptions())

const entity_welcome_user_right = world.entity('entity_welcome_user_right')
entity_welcome_user_right.setComponent('c_multi_model_ref', new MultiModelRef(
  [
    new ModelRef(model, ['welcomemsg']),
    new ModelRef(model, ["user", "firstname"]),
    new ModelRef(model, ["user", "surname"]),
  ]
));
entity_welcome_user_right.setComponent('c_gui_ref', new GuiControlRef($('#welcome-user'), 'div'));
entity_welcome_user_right.setComponent('c_display_options', new DisplayOptions())

const entity_edit_welcome_msg = world.entity('entity_edit_welcome_msg')
entity_edit_welcome_msg.setComponent('c_model_ref', new ModelRef(model, ['welcomemsg']));
entity_edit_welcome_msg.setComponent('c_gui_ref', new GuiControlRef($('input[name=welcome]'), 'input'));

const entity_edit_user_name_msg = world.entity('entity_edit_user_name_msg')
entity_edit_user_name_msg.setComponent('c_model_ref', new ModelRef(model, ["user", "firstname"]));
entity_edit_user_name_msg.setComponent('c_gui_ref', new GuiControlRef($('input[name=firstname]'), 'input'));

const entity_edit_user_surname_msg = world.entity('entity_edit_user_surname_msg')
entity_edit_user_surname_msg.setComponent('c_model_ref', new ModelRef(model, ["user", "surname"]));
entity_edit_user_surname_msg.setComponent('c_gui_ref', new GuiControlRef($('input[name=surname]'), 'input'));

const entity_dump_models = world.entity('entity_dump_models')
entity_dump_models.setComponent('c_debug_dump_options', {el: $('#debug_info'), verbose: true});  // dict as component is ok

// Extract systems - pull info from model into component 'finalstr' field for later manipulation by other systems

world.system('extract-model-ref-system', ['c_model_ref'], (entity, {c_model_ref}) => {
  // Tip - the variables receiving the component must be named exactly the same as the component name
  let c = c_model_ref
  c.finalstr = c.val
});
world.system('extract-multi-model-ref-system', ['c_multi_model_ref'], (entity, {c_multi_model_ref}) => {
  for (const c of c_multi_model_ref.refs)  // each 'c' is a ModelRef component 
    c.finalstr = c.val
});

// Case transform systems

world.system('case-transform-uppercase-welcome', ['c_model_ref', 'c_display_options'], (entity, {c_model_ref, c_display_options}) => {
  let c = c_model_ref
  if (c_display_options.uppercase_welcome && c.keys.includes("welcomemsg"))
    c.finalstr = c.finalstr.toUpperCase()
});
world.system('case-transform-uppercase_welcome_user_welcome', ['c_multi_model_ref', 'c_display_options'], (entity, {c_multi_model_ref, c_display_options}) => {
  for (const c of c_multi_model_ref.refs)  // each 'c' is a ModelRef component 
    if (
      (c_display_options.uppercase_welcome && c.keys.includes("welcomemsg")) ||
      (c_display_options.uppercase_user && (c.keys.includes("firstname") || c.keys.includes("surname"))) ||
      (c_display_options.uppercase_welcome_user)
    )
      c.finalstr = c.finalstr.toUpperCase()
});

// Render Systems

world.system('render-system-divs-and-inputs', ['c_model_ref', 'c_gui_ref'], (entity, {c_model_ref, c_gui_ref}) => {
  let $el = c_gui_ref.el
  if (c_model_ref.keys.includes("welcomemsg") && c_gui_ref.eltype == 'div')
    $el.html(c_model_ref.finalstr)
  else if (c_gui_ref.eltype == 'input')
    $el.val(c_model_ref.finalstr)
});

let msg = {}  // can't target how model ref components get found, so build up multi model output string here, via dict
world.system('render-system-top-right', ['c_multi_model_ref', 'c_gui_ref'], (entity, {c_multi_model_ref, c_gui_ref}) => {
  let $el = c_gui_ref.el
  for (const c_model_ref of c_multi_model_ref.refs)
    msg[c_model_ref.keys.slice(-1)] = c_model_ref.finalstr
  $el.html(`${msg['welcomemsg']} ${msg['firstname']} ${msg['surname']}`)
});

world.system('render-system-dump-models', ['c_debug_dump_options'], (entity, {c_debug_dump_options}) => {
  let $el = c_debug_dump_options.el
  let part1_html = syntaxHighlight(JSON.stringify({
    model: model, 
    entity_welcome_left_display_options: entity_welcome_left.components.c_display_options,
    entity_welcome_user_right_display_options: entity_welcome_user_right.components.c_display_options,
  }, null, 2))
  let part2_html = dump_world(world, c_debug_dump_options.verbose)
  $el.html(part1_html + '<br>' + part2_html)
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
  entity_welcome_left.components.c_display_options.uppercase_welcome = $(e.target).prop('checked')
  entity_welcome_user_right.components.c_display_options.uppercase_welcome = $(e.target).prop('checked')
  world.tick()
})

$("input[name=uppercase_user]").change(function(e) {
  entity_welcome_user_right.components.c_display_options.uppercase_user = $(e.target).prop('checked')
  world.tick()
})

$("input[name=uppercase_welcome_user]").change(function(e) {
  entity_welcome_user_right.components.c_display_options.uppercase_welcome = $(e.target).prop('checked')
  entity_welcome_user_right.components.c_display_options.uppercase_user = $(e.target).prop('checked')
  world.tick()
});

$("input[name=verbose_debug]").change(function(e) {
  let component = {el: $('#debug_info'), verbose: $(e.target).prop('checked')}
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
