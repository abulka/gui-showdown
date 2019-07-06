//
// Model - The Welcome model and User model are Observable.
//

class Welcome extends Subject {
  constructor(message) {
      super();
      this._msg = message == undefined ? "Welcome" : message;
    }
  
    get message() {
      return this._msg
    }
  
    set message(v) {
      this._msg = v;
      this.notifyall(`modified ${this._msg}`)
    }
}

class User extends Subject {
  constructor() {
      super();
      this._firstname = "Sam"
      this._surname = "Smith"
    }
  
    get firstname() {
      return this._firstname
    }
  
    set firstname(v) {
      this._firstname = v;
      this.notifyall(`modified ${this._firstname}`)
    }
  
    get surname() {
      return this._surname
    }
  
    set surname(v) {
      this._surname = v;
      this.notifyall(`modified ${this._surname}`)
    }
}

class Model {
  constructor(welcome_model, user_model) {
      this.welcome = welcome_model
      this.user = user_model
    }
  
    dirty_all() {
      this.welcome.notifyall("init dirty")
      this.user.notifyall("init dirty")
    }
}

//
// Mediators - are implemented as Observer classes, contain the behaviour
//

class MediatorWelcomeLeft {
  constructor(welcome_model, id) {
    this.welcome = welcome_model  // ref to Welcome model
    this.gui_div = id             // ref to DOM div where we want the welcome message to appear
    this.uppercase_welcome = false
  }
  
  notify(target, data) {
      console.log(`notification from: ${target ? target.constructor.name : 'null'} data: ${data}`)
      // assert(target == this.welcome || target == null)  // can get target of null when check 2 is triggered
      let msg = this.uppercase_welcome ? this.welcome.message.toUpperCase() : this.welcome.message
      $('#' + this.gui_div).html(msg)
  }
}

class MediatorWelcomeUserRight {
  constructor(welcome_model, user_model, id) {
    this.welcome = welcome_model
    this.user = user_model
    this.gui_div = id
    this.uppercase_welcome = false
    this.uppercase_all = false
  }
  
  notify(target, data) {
    let msg
    console.log(`notification from: ${target ? target.constructor.name : 'null'} data: ${data}`)
    assert(target == this.welcome || target == this.user || target == null)

    if (this.uppercase_all) {
      msg = `${this.welcome.message} ${this.user.firstname} ${this.user.surname}`
      msg = msg.toUpperCase()
    }
    else if (this.uppercase_welcome)
      msg = `${this.welcome.message.toUpperCase()} ${this.user.firstname} ${this.user.surname}`
    else
      msg = `${this.welcome.message} ${this.user.firstname} ${this.user.surname}`

      $('#' + this.gui_div).html(msg)
  }
}

class MediatorEditWelcome {
  constructor(welcome_model, id) {
    this.welcome = welcome_model
    this.gui_input = id  // name (not id) of input to hold welcome message
  }
  
  notify(target, data) {
    console.log(`notification from: ${target.constructor.name} data: ${data}`)
    assert(target == this.welcome)
    $(`input[name=${this.gui_input}]`).val(this.welcome.message)
  }
}

class MediatorEditUserFirstName {
  constructor(user_model, id) {
    this.user = user_model
    this.gui_input = id
  }
  
  notify(target, data) {
    console.log(`notification from: ${target.constructor.name} data: ${data}`)
    assert(target == this.user)
    $(`input[name=${this.gui_input}]`).val(this.user.firstname)
  }
}

class MediatorEditUserSurName {
  constructor(user_model, id) {
    this.user = user_model
    this.gui_input = id
  }
  
  notify(target, data) {
    console.log(`notification from: ${target.constructor.name} data: ${data}`)
    assert(target == this.user)
    $(`input[name=${this.gui_input}]`).val(this.user.surname)
  }
}


// const world = new Ecs();

// class ModelRef {  // Mediator (entity + this component) needs to know about model. Model specific
//   constructor(model, key) {
//     this.model = model;
//     this.key = key;
//     this.finalstr = "";
//   }
// }
// class MultiModelRef {  // Refers to multiple model fields, since can only have one component per entity can't have multiple ModelRefs
//   constructor(refs) {
//     this.refs = refs;  // list of ModelRef
//   }
// }

// class GuiControlRef {  // Mediator (entity + this component) needs to know about a wxPython gui control
//   constructor(ref) {
//     this.ref = ref
//   }
// }
// class ComponentGuiDiv extends GuiControlRef {}
// class ComponentGuiInput extends GuiControlRef {}

// class Flag {}  // Mediator (entity + this component) might have a flag to indicate some behaviour is wanted
// class ComponentUppercaseAll extends Flag {}
// class ComponentUppercaseWelcome extends Flag {}

// const entity_welcome_left = world.entity('entity_welcome_left')
// entity_welcome_left.setComponent('c_model_ref', new ModelRef(model, 'welcome_msg'))
// entity_welcome_left.setComponent('c_gui_div', new ComponentGuiDiv('welcome'))  // id of div to hold welcome message, top left

// const entity_welcome_user_right = world.entity('entity_welcome_user_right')
// entity_welcome_user_right.setComponent('c_multi_model_ref', new MultiModelRef(
//   [
//     new ModelRef(model, 'welcome_msg'),
//     new ModelRef(model["user"], 'name'),
//     new ModelRef(model["user"], 'surname'),
//   ]
// ));
// entity_welcome_user_right.setComponent('c_gui_div', new ComponentGuiDiv('welcome-user'));  // id of div to hold welcome + user message, top right

// const entity_edit_welcome_msg = world.entity('entity_edit_welcome_msg')
// entity_edit_welcome_msg.setComponent('c_model_ref', new ModelRef(model, 'welcome_msg'));
// entity_edit_welcome_msg.setComponent('c_gui_input', new ComponentGuiInput('welcome'));  // name (not id) of input to hold welcome message

// const entity_edit_user_name_msg = world.entity('entity_edit_user_name_msg')
// entity_edit_user_name_msg.setComponent('c_model_ref', new ModelRef(model["user"], 'name'));
// entity_edit_user_name_msg.setComponent('c_gui_input', new ComponentGuiInput('firstname'));  // name (not id) of input to hold first name

// const entity_edit_user_surname_msg = world.entity('entity_edit_user_surname_msg')
// entity_edit_user_surname_msg.setComponent('c_model_ref', new ModelRef(model["user"], 'surname'));
// entity_edit_user_surname_msg.setComponent('c_gui_input', new ComponentGuiInput('surname'));  // name (not id) of input to hold first name

// // Extract

// world.system('extract-model-ref-system', ['c_model_ref'], (entity, {c_model_ref}) => {
//   c_model_ref.finalstr = c_model_ref.model[c_model_ref.key]
//   console.log("c_model_ref.finalstr", c_model_ref.finalstr)
// });
// world.system('extract-multi-model-ref-system', ['c_multi_model_ref'], (entity, {c_multi_model_ref}) => {
//   for (const c_model_ref of c_multi_model_ref.refs) {
//     c_model_ref.finalstr = c_model_ref.model[c_model_ref.key]
//     console.log("c_model_ref.finalstr", c_model_ref.finalstr)
//   }
// });

// // Case transform

// world.system('case-transform-uppercase-welcome', ['c_model_ref', 'c_uppercase_welcome'], (entity, {c_model_ref, c_uppercase_welcome}) => {
//   if (c_model_ref.key == "welcome_msg")
//     c_model_ref.finalstr = c_model_ref.finalstr.toUpperCase()
// });
// world.system('case-transform-uppercase_all-just-welcome', ['c_multi_model_ref', 'c_uppercase_welcome'], (entity, {c_multi_model_ref, c_uppercase_welcome}) => {
//   for (const c_model_ref of c_multi_model_ref.refs)
//     if (c_model_ref.key == "welcome_msg")
//       c_model_ref.finalstr = c_model_ref.finalstr.toUpperCase()
// });
// world.system('case-transform-uppercase_all', ['c_multi_model_ref', 'c_uppercase_all'], (entity, {c_multi_model_ref, c_uppercase_all}) => {
//   for (const c_model_ref of c_multi_model_ref.refs)
//     c_model_ref.finalstr = c_model_ref.finalstr.toUpperCase()
// });

// // Render Systems

// world.system('render-system-top-left', ['c_model_ref', 'c_gui_div'], (entity, {c_model_ref, c_gui_div}) => {
//   if (c_model_ref.key == "welcome_msg")
//     $('#' + c_gui_div.ref).html(c_model_ref.finalstr)
// });

// let msg = {}  // can't target how model ref components get found, so build up what we need here
// world.system('render-system-top-right', ['c_multi_model_ref', 'c_gui_div'], (entity, {c_multi_model_ref, c_gui_div}) => {
//   for (const c_model_ref of c_multi_model_ref.refs)
//     msg[c_model_ref.key] = c_model_ref.finalstr
//   $('#' + c_gui_div.ref).html(`${msg['welcome_msg']} ${msg['name']} ${msg['surname']}`)
// });

// world.system('render-system-text-inputs', ['c_model_ref', 'c_gui_input'], (entity, {c_model_ref, c_gui_input}) => {
//   $(`input[name=${c_gui_input.ref}]`).val(c_model_ref.finalstr)
// });

// Util

// function model_setter_welcome(msg) {
//     model["welcome_msg"] = msg
//     model_welcome_toggle()
// }

function model_welcome_toggle() {
  model.welcome.message = $('input[name=check1]').prop('checked') ? model.welcome.message.toUpperCase() : model.welcome.message.toLowerCase()
}

$('#reset-welcome').on('click', function(e) {
  model.welcome.message = "Hello"
})

$('#reset-user').on('click', function(e) {
  model.user.firstname = "Fred"
  model.user.surname = "Flinstone"
})

$("input[name=check1]").change(function(e) {  // on_check_welcome_model
  // toggle the case of the model's welcome message
  model_welcome_toggle()
})

$("input[name=check2]").change(function(e) {  // on_check_toggle_welcome_outputs_only
  // toggle the case of the welcome output messages only - do not affect model
  mediator_welcome_left.uppercase_welcome = $('input[name=check2]').prop('checked')
  mediator_welcome_user_right.uppercase_welcome = $('input[name=check2]').prop('checked')
  mediator_welcome_left.notify(null, "checked event")  // bit weird having target=null
  mediator_welcome_user_right.notify(null, "checked event")
})

$("input[name=check3]").change(function(e){
  // don't change the model - only the UI display
  mediator_welcome_user_right.uppercase_all = $('input[name=check3]').prop('checked')
  mediator_welcome_user_right.notify(null, "checked event")
});

// $("input").change(function(){
//   alert("The text has been changed.");
// });

$("input[name=welcome]").change(function(e) {  // on_enter_welcome
    model["welcome_msg"] = $(e.target).val()
    world.tick()
})

$("input[name=firstname]").change(function(e) {  // on_enter_user_firstname
  model["user"]["name"] = $(e.target).val()
    world.tick()
})

$("input[name=surname]").change(function(e) {  // on_enter_user_surname
  model["user"]["surname"] = $(e.target).val()
    world.tick()
})

$('#render-now').on('click', function(e) {
  world.tick()
})


//
// Wire up and build everything
//

model = new Model(new Welcome(), new User())
mediator_welcome_left = new MediatorWelcomeLeft(model.welcome, "welcome")
mediator_welcome_user_right = new MediatorWelcomeUserRight(model.welcome, model.user, 'welcome-user')
mediator_edit_welcome_msg = new MediatorEditWelcome(model.welcome, 'welcome')
mediator_edit_user_name_msg = new MediatorEditUserFirstName(model.user, 'firstname')
mediator_edit_user_surname_msg = new MediatorEditUserSurName(model.user, 'surname')

// Observer Wiring
model.welcome.add_observer(mediator_welcome_left)
model.welcome.add_observer(mediator_welcome_user_right)
model.welcome.add_observer(mediator_edit_welcome_msg)
model.user.add_observer(mediator_welcome_user_right)
model.user.add_observer(mediator_edit_user_name_msg)
model.user.add_observer(mediator_edit_user_surname_msg)

// world.tick()
model.dirty_all()  // initialise the gui with initial model values

