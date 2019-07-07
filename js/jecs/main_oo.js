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

class Model {  // aggregates all the sub models into one housing
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
// Mediators - are implemented as Observer classes, contain the display update behaviour plus refs to model and gui
//

class MediatorWelcomeLeft {
  constructor(welcome_model, id) {
    this.welcome = welcome_model  // ref to Welcome model
    this.gui_div = id             // ref to DOM div where we want the welcome message to appear
    this.uppercase_welcome = false
  }
  
  notify(target, data) {
      console.log(`MediatorWelcomeLeft got notification from: ${target ? target.constructor.name : 'null'} data: ${data}`)

      if (data == "display option change") {
        const display_options = target
        this.uppercase_welcome = display_options.uppercase_welcome
      }

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
    this.uppercase_user = false
    this.uppercase_welcome_user = false
  }
  
  notify(target, data) {
    let msg
    console.log(`MediatorWelcomeUserRight got notification from: ${target ? target.constructor.name : 'null'} data: ${data}`)

    if (data == "display option change") {
      const display_options = target
      this.uppercase_welcome = display_options.uppercase_welcome
      this.uppercase_user = display_options.uppercase_user
      this.uppercase_welcome_user = display_options.uppercase_welcome_user
    }

    let welcome = (this.uppercase_welcome || this.uppercase_welcome_user) ? this.welcome.message.toUpperCase() : this.welcome.message
    let firstname = (this.uppercase_user || this.uppercase_welcome_user) ? this.user.firstname.toUpperCase() : this.user.firstname
    let surname = (this.uppercase_user || this.uppercase_welcome_user) ? this.user.surname.toUpperCase() : this.user.surname
    $('#' + this.gui_div).html(welcome + ' ' + firstname + ' ' + surname )
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

class DisplayOptions extends Subject {
  constructor() {
      super();
      this._uppercase_welcome = false
      this._uppercase_user = false
      this._uppercase_welcome_user = false
  }

  get uppercase_welcome() {
    return this._uppercase_welcome
  }

  set uppercase_welcome(v) {
    this._uppercase_welcome = v;
    this.notifyall("display option change")
  }

  get uppercase_user() {
    return this._uppercase_user
  }

  set uppercase_user(v) {
    this._uppercase_user = v;
    this.notifyall("display option change")
  }

  get uppercase_welcome_user() {
    return this._uppercase_welcome_user
  }

  set uppercase_welcome_user(v) {
    this._uppercase_welcome_user = v;
    this.notifyall("display option change")
  }

  // util

  isUpperCaseAt(str, n) {
    return str[n]=== str[n].toUpperCase();
  }  
}

class MediatorDumpModels {
  constructor(id) {
      this.gui_pre_id = id
  }
  
  notify(target, data) {
    console.log(`notification from: ${target.constructor.name} data: ${data}`)
    let info = {
      model: model,
      display_options: display_options,
      mediator_welcome_left: mediator_welcome_left,
      mediator_welcome_user_right : mediator_welcome_user_right,
      mediator_edit_welcome_msg : mediator_edit_welcome_msg,
      mediator_edit_user_name_msg : mediator_edit_user_name_msg,
      mediator_edit_user_surname_msg : mediator_edit_user_surname_msg,
    }
    $(`#${this.gui_pre_id}`).html(syntaxHighlight(JSON.stringify(info, function(key, value) {

        // skip observers or circular references will break the json
        if (key == 'observers') { 
          return value.id;
        } else {
          return value;
        }

    }, 2)))

  }
}

//
// GUI events
//

$('#change_welcome_model').on('click', function(e) {
  model.welcome.message = display_options.isUpperCaseAt(model.welcome.message, 1) ? model.welcome.message.toLowerCase() : model.welcome.message.toUpperCase()
})

$('#change_user_model').on('click', function(e) {
  model.user.firstname = display_options.isUpperCaseAt(model.user.firstname, 1) ? model.user.firstname.toLowerCase() : model.user.firstname.toUpperCase()
  model.user.surname = display_options.isUpperCaseAt(model.user.surname, 1) ? model.user.surname.toLowerCase() : model.user.surname.toUpperCase()
})

$('#reset_welcome_model').on('click', function(e) {
  model.welcome.message = "Hello"
})

$('#reset_user_model').on('click', function(e) {
  model.user.firstname = "Fred"
  model.user.surname = "Flinstone"
})

$("input[name=uppercase_welcome]").change(function(e) {
  display_options.uppercase_welcome = $(e.target).prop('checked')
})

$("input[name=uppercase_user]").change(function(e) {
  display_options.uppercase_user = $(e.target).prop('checked')
})

$("input[name=uppercase_welcome_user]").change(function(e){
  display_options.uppercase_welcome_user = $(e.target).prop('checked')
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
display_options = new DisplayOptions()
mediator_dump_models = new MediatorDumpModels("debug_info")

// Observer Wiring
model.welcome.add_observer(mediator_welcome_left)
model.welcome.add_observer(mediator_welcome_user_right)
model.welcome.add_observer(mediator_edit_welcome_msg)
model.user.add_observer(mediator_welcome_user_right)
model.user.add_observer(mediator_edit_user_name_msg)
model.user.add_observer(mediator_edit_user_surname_msg)
display_options.add_observer(mediator_welcome_left)
display_options.add_observer(mediator_welcome_user_right)
// debug mediator 
model.welcome.add_observer(mediator_dump_models)
model.user.add_observer(mediator_dump_models)
display_options.add_observer(mediator_dump_models)

model.dirty_all()  // initialise the gui with initial model values
