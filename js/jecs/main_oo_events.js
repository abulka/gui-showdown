//
// Idiomatic Javascript Eventing to implement Subject/Observer pattern
///

function notify_all(event_name, target, data) {
  document.dispatchEvent(new CustomEvent(event_name, { detail: {target: target, data: data } }))
  document.dispatchEvent(new CustomEvent("observer-notification", { detail: {target: target, data: data } }))  // debugging hook
  console.log(`notify all of '${event_name}' ${target != null ? 'from: ' + target.constructor.name : target} ${data != null ? 'data: ' + data : ''}`)
}

//
// Model - The Welcome model and User model are Observable.
//

class Welcome {
  constructor(message) {
      this._msg = message == undefined ? "Welcome" : message;
    }
  
    get message() {
      return this._msg
    }
  
    set message(v) {
      this._msg = v;
      notify_all("modified welcome", this, this._msg)
    }
}

class User {
  constructor() {
      this._firstname = "Sam"
      this._surname = "Smith"
    }
  
    get firstname() {
      return this._firstname
    }
  
    set firstname(v) {
      this._firstname = v;
      notify_all("modified user", this, this._firstname)
    }
  
    get surname() {
      return this._surname
    }
  
    set surname(v) {
      this._surname = v;
      notify_all("modified user", this, this._surname)
    }
}

class Model {  // aggregates all the sub models into one housing
  constructor(welcome_model, user_model) {
      this.welcome = welcome_model
      this.user = user_model
    }
  
    dirty_startup() {
      this.dirty_all()
      notify_all("startup", this)
    }

    dirty_all() {
      notify_all("modified welcome", this)
      notify_all("modified user", this)
    }
}

//
// Mediators - are implemented as Observer classes, contain the display update behaviour plus refs to model and gui
//

class MediatorWelcomeLeft {
  constructor(welcome_model, id) {
    this.welcome = welcome_model  // ref to Welcome model
    this.gui_div = id             // ref to DOM div where we want the welcome message to appear
    this._uppercase_welcome = false
  }
  
  get uppercase_welcome() { 
    return this._uppercase_welcome 
  }
  set uppercase_welcome(val) { 
    this._uppercase_welcome = val
    notify_all("display option change", this, "uppercase_welcome")
    // this.notify(this, 'display option change')
    // document.dispatchEvent(new CustomEvent("observer-notification", { details: {target: this, data: 'display option change' } }))  // FIXME this is bad
  }

  notify(event) {
    let msg = this.uppercase_welcome ? this.welcome.message.toUpperCase() : this.welcome.message
    $('#' + this.gui_div).html(msg)
  }
}

class MediatorWelcomeUserRight {
  constructor(welcome_model, user_model, id) {
    this.welcome = welcome_model
    this.user = user_model
    this.gui_div = id
    this._uppercase_welcome = false
    this._uppercase_user = false
  }
  
  get uppercase_welcome() { 
    return this._uppercase_welcome 
  }
  set uppercase_welcome(val) { 
    this._uppercase_welcome = val
    // TODO actually rather than calling yourself, should emit an event so that the debugging hook can work. A bit inefficient but better
    // this.notify(this, 'display option change')
    // document.dispatchEvent(new CustomEvent("observer-notification", { details: {target: this, data: 'display option change' } }))  // FIXME this is bad
    notify_all("display option change", this, "uppercase_welcome")
  }
  
  get uppercase_user() { 
    return this._uppercase_user 
  }
  set uppercase_user(val) { 
    this._uppercase_user = val
    // this.notify(this, 'display option change')
    // document.dispatchEvent(new CustomEvent("observer-notification", { details: {target: this, data: 'display option change' } }))  // FIXME this is bad
    notify_all("display option change", this, "uppercase_user")
  }

  notify(event) {
    let welcome = this.uppercase_welcome ? this.welcome.message.toUpperCase() : this.welcome.message
    let firstname = this.uppercase_user ? this.user.firstname.toUpperCase() : this.user.firstname
    let surname = this.uppercase_user ? this.user.surname.toUpperCase() : this.user.surname
    $('#' + this.gui_div).html(welcome + ' ' + firstname + ' ' + surname )
  }
}

class MediatorEditWelcome {
  constructor(welcome_model, id) {
    this.welcome = welcome_model
    this.gui_input = id  // name (not id) of input to hold welcome message
  }
  
  notify(event) {
    $(`input[name=${this.gui_input}]`).val(this.welcome.message)
  }
}

class MediatorEditUserFirstName {
  constructor(user_model, id) {
    this.user = user_model
    this.gui_input = id
  }
  
  notify(event) {
    $(`input[name=${this.gui_input}]`).val(this.user.firstname)
  }
}

class MediatorEditUserSurName {
  constructor(user_model, id) {
    this.user = user_model
    this.gui_input = id
  }
  
  notify(event) {
    $(`input[name=${this.gui_input}]`).val(this.user.surname)
  }
}

class MediatorPageTitle {
  constructor(s, $id) {
    this.s = s
    this.$id = $id
  }
  
  notify(event) {
    this.$id.html(this.s)
  }
}

class DebugDumpModels {  // Not an OO Observer (to avoid infinite recursion), but a listener nevertheless
  constructor(id) {
    this.gui_pre_id = id
  }
  
  notify_ocurred(target) {
    let info = {
      model: model,
      mediator_welcome_left: mediator_welcome_left,
      mediator_welcome_user_right : mediator_welcome_user_right,
      mediator_edit_welcome_msg : mediator_edit_welcome_msg,
      mediator_edit_user_name_msg : mediator_edit_user_name_msg,
      mediator_edit_user_surname_msg : mediator_edit_user_surname_msg,
    }
    $(`#${this.gui_pre_id}`).html(syntaxHighlight(JSON.stringify(info, function(key, value) {

        // skip 'observers' fields or circular references will break the generated json
        if (key == 'observers') { 
          return value.id;
        } else {
          return value;
        }

    }, 2)))

  }
}

// Util

function isUpperCaseAt(str, n) {
    return str[n]=== str[n].toUpperCase();
}  

//
// GUI events
//

$('#change_welcome_model').on('click', function(e) {
  model.welcome.message = isUpperCaseAt(model.welcome.message, 1) ? model.welcome.message.toLowerCase() : model.welcome.message.toUpperCase()
})

$('#change_user_model').on('click', function(e) {
  model.user.firstname = isUpperCaseAt(model.user.firstname, 1) ? model.user.firstname.toLowerCase() : model.user.firstname.toUpperCase()
  model.user.surname = isUpperCaseAt(model.user.surname, 1) ? model.user.surname.toLowerCase() : model.user.surname.toUpperCase()
})

$('#reset_welcome_model').on('click', function(e) {
  model.welcome.message = "Hello"
})

$('#reset_user_model').on('click', function(e) {
  model.user.firstname = "Fred"
  model.user.surname = "Flinstone"
})

$("input[name=uppercase_welcome]").change(function(e) {
  mediator_welcome_left.uppercase_welcome = $(e.target).prop('checked')
  mediator_welcome_user_right.uppercase_welcome = $(e.target).prop('checked')
})

$("input[name=uppercase_user]").change(function(e) {
  mediator_welcome_user_right.uppercase_user = $(e.target).prop('checked')
})

$("input[name=uppercase_welcome_user]").change(function(e){
  mediator_welcome_user_right.uppercase_welcome = $(e.target).prop('checked')
  mediator_welcome_user_right.uppercase_user = $(e.target).prop('checked')
});

$( "input[name=welcome]" ).keypress(function(e) {  // use 'change' if you want to wait for ENTER
  model.welcome.message = $(e.target).val()
});

$("input[name=firstname]").keypress(function(e) {
  model.user.firstname = $(e.target).val()
})

$("input[name=surname]").keypress(function(e) {
  model.user.surname = $(e.target).val()
})

$('#render-now').on('click', function(e) {
  model.dirty_all()
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
mediator_page_title = new MediatorPageTitle("Gui wired via OO + Events", $('#title > h1'))
controller_dump_models = new DebugDumpModels("debug_info")  // not an OO Observer (to avoid infinite recursion), but a listener nevertheless

// Observer Wiring
document.addEventListener("modified welcome", (event) => { mediator_welcome_left.notify(event) })
document.addEventListener("modified welcome", (event) => { mediator_welcome_user_right.notify(event) })
document.addEventListener("modified welcome", (event) => { mediator_edit_welcome_msg.notify(event) })
document.addEventListener("modified user", (event) =>    { mediator_welcome_user_right.notify(event) })
document.addEventListener("modified user", (event) =>    { mediator_edit_user_name_msg.notify(event) })
document.addEventListener("modified user", (event) =>    { mediator_edit_user_surname_msg.notify(event) })
document.addEventListener("startup", (event) =>          { mediator_page_title.notify(event) })
document.addEventListener("display option change", (event) => { mediator_welcome_left.notify(event) })
document.addEventListener("display option change", (event) => { mediator_welcome_user_right.notify(event) })
document.addEventListener("observer-notification", (event) => { controller_dump_models.notify_ocurred(event.target) }) // Must use arrow function to get correct value of 'this'

// document.addEventListener("modified welcome", (event) => { mediator_welcome_left.notify(event.target, event.details) })
// document.addEventListener("modified welcome", (event) => { mediator_welcome_user_right.notify(event.target, event.details) })
// document.addEventListener("modified user", (event) => { mediator_welcome_user_right.notify(event.target, event.details) })
// document.addEventListener("modified welcome", (event) => { mediator_edit_welcome_msg.notify(event.target, event.details) })
// document.addEventListener("modified user", (event) => { mediator_edit_user_name_msg.notify(event.target, event.details) })
// document.addEventListener("modified user", (event) => { mediator_edit_user_surname_msg.notify(event.target, event.details) })
// document.addEventListener("startup", (event) => { mediator_page_title.notify(event.target, event.details) })
// document.addEventListener("observer-notification", (event) => { controller_dump_models.notify_ocurred(event.target) }) // Must use arrow function to get correct value of 'this'

model.dirty_startup()  // initialise the gui with initial model values
