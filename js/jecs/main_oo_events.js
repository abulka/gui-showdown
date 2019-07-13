//
// Models
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

class App {  // aggregates all the sub models into one housing, with some business logic
  constructor(welcome_model, user_model) {
      this.welcome_model = welcome_model
      this.user_model = user_model
    }
  
    on_change_welcome_model(event) {
      this.welcome_model.message = isUpperCaseAt(this.welcome_model.message, 1) ? this.welcome_model.message.toLowerCase() : this.welcome_model.message.toUpperCase()
    }

    on_change_user_model(event) {
      this.user_model.firstname = isUpperCaseAt(this.user_model.firstname, 1) ? this.user_model.firstname.toLowerCase() : this.user_model.firstname.toUpperCase()
      this.user_model.surname = isUpperCaseAt(this.user_model.surname, 1) ? this.user_model.surname.toLowerCase() : this.user_model.surname.toUpperCase()
    }

    on_reset_welcome_model(event) {
      this.welcome_model.message = "Hello"
    }
  
    on_reset_user_model(event) {
      this.user_model.firstname = "Fred"
      this.user_model.surname = "Flinstone"
    }
  
    on_keychar_welcome(e) { this.welcome_model.message = $(e.target).val() }
    on_keychar_firstname(e) { this.user_model.firstname = $(e.target).val() }
    on_keychar_surname(e) { this.user_model.surname = $(e.target).val() }

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
// Mediators - contain the View/GUI/DOM updating code, some display option flags plus refs to model and DOM
//

class MediatorWelcomeLeft {
  constructor(welcome_model, id) {
    this.welcome_model = welcome_model  // ref to Welcome model
    this.gui_div = id             // ref to DOM div where we want the welcome message to appear
    this._uppercase_welcome = false
  }
  
  get uppercase_welcome() { 
    return this._uppercase_welcome 
  }
  set uppercase_welcome(val) { 
    this._uppercase_welcome = val
    notify_all("display option change", this, `flag uppercase_welcome ${val}`)
  }

  on_check_upper_welcome(e) {
    this.uppercase_welcome = $(e.target).prop('checked')
  }

  notify(event) {
    let msg = this.uppercase_welcome ? this.welcome_model.message.toUpperCase() : this.welcome_model.message
    $('#' + this.gui_div).html(msg)
  }
}

class MediatorWelcomeUserRight {
  constructor(welcome_model, user_model, id) {
    this.welcome_model = welcome_model
    this.user_model = user_model
    this.gui_div = id
    this._uppercase_welcome = false
    this._uppercase_user = false
  }
  
  get uppercase_welcome() { 
    return this._uppercase_welcome 
  }
  set uppercase_welcome(val) { 
    this._uppercase_welcome = val
    notify_all("display option change", this, `flag uppercase_welcome ${val}`)
  }
  
  get uppercase_user() { 
    return this._uppercase_user 
  }
  set uppercase_user(val) { 
    this._uppercase_user = val
    notify_all("display option change", this, `flag uppercase_user ${val}`)
  }

  on_check_upper_welcome(e) {
    this.uppercase_welcome = $(e.target).prop('checked')
  }

  on_check_upper_user(e) {
    this.uppercase_user = $(e.target).prop('checked')
  }

  on_check_upper_welcome_user(e) {
    this.uppercase_welcome = $(e.target).prop('checked')
    this.uppercase_user = $(e.target).prop('checked')
  }

  notify(event) {
    let welcome = this.uppercase_welcome ? this.welcome_model.message.toUpperCase() : this.welcome_model.message
    let firstname = this.uppercase_user ? this.user_model.firstname.toUpperCase() : this.user_model.firstname
    let surname = this.uppercase_user ? this.user_model.surname.toUpperCase() : this.user_model.surname
    $('#' + this.gui_div).html(welcome + ' ' + firstname + ' ' + surname )
  }
}

class MediatorEditWelcome {
  constructor(welcome_model, id) {
    this.welcome_model = welcome_model
    this.gui_input = id  // name (not id) of input to hold welcome message
  }
  
  notify(event) {
    $(`input[name=${this.gui_input}]`).val(this.welcome_model.message)
  }
}

class MediatorEditUserFirstName {
  constructor(user_model, id) {
    this.user_model = user_model
    this.gui_input = id
  }
  
  notify(event) {
    $(`input[name=${this.gui_input}]`).val(this.user_model.firstname)
  }
}

class MediatorEditUserSurName {
  constructor(user_model, id) {
    this.user_model = user_model
    this.gui_input = id
  }
  
  notify(event) {
    $(`input[name=${this.gui_input}]`).val(this.user_model.surname)
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

class DebugDumpModels {
  constructor(id) {
    this.gui_pre_id = id
  }
  
  notify(event) {
    let info = {
      app_models: app,
      mediator_welcome_left: mediator_welcome_left,
      mediator_welcome_user_right : mediator_welcome_user_right,
      mediator_edit_welcome_msg : mediator_edit_welcome_msg,
      mediator_edit_user_name_msg : mediator_edit_user_name_msg,
      mediator_edit_user_surname_msg : mediator_edit_user_surname_msg,
    }
    $(`#${this.gui_pre_id}`).html(syntaxHighlight(JSON.stringify(info, null, 2)))
  }
}

// Util

function isUpperCaseAt(str, n) {
    return str[n]=== str[n].toUpperCase();
}  

//
// Create the app and mediators
//

app = new App(new Welcome(), new User())
mediator_welcome_left = new MediatorWelcomeLeft(app.welcome_model, "welcome")
mediator_welcome_user_right = new MediatorWelcomeUserRight(app.welcome_model, app.user_model, 'welcome-user')
mediator_edit_welcome_msg = new MediatorEditWelcome(app.welcome_model, 'welcome')
mediator_edit_user_name_msg = new MediatorEditUserFirstName(app.user_model, 'firstname')
mediator_edit_user_surname_msg = new MediatorEditUserSurName(app.user_model, 'surname')
mediator_page_title = new MediatorPageTitle("Gui wired via OO + Events", $('#title > h1'))
controller_dump_models = new DebugDumpModels("debug_info")

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
document.addEventListener("notify all called", (event) => { controller_dump_models.notify(event) })

// Gui Event Wiring
$('#change_welcome_model').on('click', (event) => { app.on_change_welcome_model(event) })
$('#change_user_model').on('click', (event) => { app.on_change_user_model(event) })
$('#reset_welcome_model').on('click', (event) => { app.on_reset_welcome_model(event) })
$('#reset_user_model').on('click', (event) => { app.on_reset_user_model(event) })
$('input[name=welcome]').on('keyup', (event) => { app.on_keychar_welcome(event) })
$('input[name=firstname]').on('keyup', (event) => { app.on_keychar_firstname(event) })
$('input[name=surname]').on('keyup', (event) => { app.on_keychar_surname(event) })
$('input[name=uppercase_welcome]').on('change', (event) => { mediator_welcome_left.on_check_upper_welcome(event) })
$('input[name=uppercase_welcome]').on('change', (event) => { mediator_welcome_user_right.on_check_upper_welcome(event) })
$('input[name=uppercase_user]').on('change', (event) => { mediator_welcome_user_right.on_check_upper_user(event) })
$('input[name=uppercase_welcome_user]').on('change', (event) => { mediator_welcome_user_right.on_check_upper_welcome_user(event) })
$('#render-now').on('click', function(e) { app.dirty_all() })

app.dirty_startup()  // initialise the gui with initial model values
