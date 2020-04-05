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

class Application {
  constructor(config) {
    // Models
    this.welcome_model = new Welcome()
    this.user_model = new User()

      // View state (used to live in controllers in OO version), these control the display of the header titles at top
      this._uppercase_welcome = false
      this._uppercase_user = false
      this._uppercase_welcome_user = false

      this.dirty_startup()
    }
    
    get uppercase_welcome() { 
      return this._uppercase_welcome 
    }
    set uppercase_welcome(val) { 
      this._uppercase_welcome = val
      notify_all("display option change", this, {what: 'uppercase_welcome', is_upper: val})
    }

    get uppercase_user() { 
      return this._uppercase_user 
    }
    set uppercase_user(val) { 
      this._uppercase_user = val
      notify_all("display option change", this, {what: 'uppercase_user', is_upper: val})
    }

    get uppercase_welcome_user() { 
      return this._uppercase_welcome_user 
    }
    set uppercase_welcome_user(val) { 
      this._uppercase_welcome_user = val
      notify_all("display option change", this, {what: 'uppercase_welcome_user', is_upper: val})
    }

    dirty_startup() {
      notify_all("startup", this)
    }
}

// class App {  // aggregates all the sub models into one housing, with some business logic
//   constructor(welcome_model, user_model) {
//       this.welcome_model = welcome_model
//       this.user_model = user_model
//     }
  
//     on_change_welcome_model(event) {
//       this.welcome_model.message = isUpperCaseAt(this.welcome_model.message, 1) ? this.welcome_model.message.toLowerCase() : this.welcome_model.message.toUpperCase()
//     }

//     on_change_user_model(event) {
//       this.user_model.firstname = isUpperCaseAt(this.user_model.firstname, 1) ? this.user_model.firstname.toLowerCase() : this.user_model.firstname.toUpperCase()
//       this.user_model.surname = isUpperCaseAt(this.user_model.surname, 1) ? this.user_model.surname.toLowerCase() : this.user_model.surname.toUpperCase()
//     }

//     on_reset_welcome_model(event) {
//       this.welcome_model.message = "Hello"
//     }
  
//     on_reset_user_model(event) {
//       this.user_model.firstname = "Fred"
//       this.user_model.surname = "Flinstone"
//     }
  
//     dirty_startup() {
//       this.dirty_all()
//       notify_all("startup", this)
//     }

//     dirty_all() {
//       notify_all("modified welcome", this)
//       notify_all("modified user", this)
//     }
// }

//
// Mediators - contain the View/GUI/DOM updating code, some display option flags plus refs to model and DOM
//

class ControllerHeader {
  constructor(app, gui_dict) {
    this.app = app          // ref to Welcome model in app.welcome_model
    this.gui = gui_dict     // refs to DOM div where we want the welcome and welcome user message to appear

    // Gui events - none, because these are 'display only' titles, its the other controller that handles checkbox inputs

		// Internal events - we listen via 'notify()' in order to display as per the view state
		document.addEventListener("display option change", (event) => { this.notify(event) })
		document.addEventListener("startup", (event) => { this.notify(event) })
  }

	notify(event) {
    // We could interrogate event.detail.data.what and event.detail.data.is_upper to do more granular updates, 
    //   but simpler to update whole header here each time
    console.log(`\tControllerHeader got event '${event.type}' data is '${JSON.stringify(event.detail.data)}'`)

    // update the 'welcome' header (top left) based on current view state
    let welcome = this.app.uppercase_welcome ? this.app.welcome_model.message.toUpperCase() : this.app.welcome_model.message
    this.gui.$title_welcome.html(welcome)

    // update the 'welcome user' (top right) header based on current view state
    welcome = this.app.uppercase_welcome || this.app.uppercase_welcome_user ? this.app.welcome_model.message.toUpperCase() : this.app.welcome_model.message
    let firstname = this.app.uppercase_user || this.app.uppercase_welcome_user ? this.app.user_model.firstname.toUpperCase() : this.app.user_model.firstname
    let surname = this.app.uppercase_user || this.app.uppercase_welcome_user ? this.app.user_model.surname.toUpperCase() : this.app.user_model.surname
    this.gui.$title_welcome_user.html(`${welcome} ${firstname} ${surname}`)
  }
  
}

class ControllerDisplayOptions {  // Could merge this with the Controller Header
  constructor(app, gui_dict) {
    this.app = app          // ref to Welcome model available in app.welcome_model
    this.gui = gui_dict

    // Gui events -> this controller
    this.gui.$cb_uppercase_welcome.on('change', (e) => { this.app.uppercase_welcome = $(e.target).prop('checked') })
    this.gui.$cb_uppercase_user.on('change', (e) => { this.app.uppercase_user = $(e.target).prop('checked') })
    this.gui.$cb_uppercase_welcome_user.on('change', (e) => { this.app.uppercase_welcome_user = $(e.target).prop('checked') })

    // Internal events - none, this controller just listens to gui
  }

}

// class MediatorWelcome {
//   constructor(welcome_model, id) {
//     this.welcome_model = welcome_model  // ref to Welcome model
//     this.gui_div = id             // ref to DOM div where we want the welcome message to appear
//     this._uppercase_welcome = false
//   }
  
//   get uppercase_welcome() { 
//     return this._uppercase_welcome 
//   }
//   set uppercase_welcome(val) { 
//     this._uppercase_welcome = val
//     notify_all("display option change", this, `flag uppercase_welcome ${val}`)
//   }

//   on_check_upper_welcome(e) {
//     this.uppercase_welcome = $(e.target).prop('checked')
//   }

//   notify(event) {
//     let msg = this.uppercase_welcome ? this.welcome_model.message.toUpperCase() : this.welcome_model.message
//     $('#' + this.gui_div).html(msg)
//   }
// }

// class MediatorWelcomeUser {
//   constructor(welcome_model, user_model, id) {
//     this.welcome_model = welcome_model
//     this.user_model = user_model
//     this.gui_div = id
//     this._uppercase_welcome = false
//     this._uppercase_user = false
//   }
  
//   get uppercase_welcome() { 
//     return this._uppercase_welcome 
//   }
//   set uppercase_welcome(val) { 
//     this._uppercase_welcome = val
//     notify_all("display option change", this, `flag uppercase_welcome ${val}`)
//   }
  
//   get uppercase_user() { 
//     return this._uppercase_user 
//   }
//   set uppercase_user(val) { 
//     this._uppercase_user = val
//     notify_all("display option change", this, `flag uppercase_user ${val}`)
//   }

//   on_check_upper_welcome(e) {
//     this.uppercase_welcome = $(e.target).prop('checked')
//   }

//   on_check_upper_user(e) {
//     this.uppercase_user = $(e.target).prop('checked')
//   }

//   on_check_upper_welcome_user(e) {
//     this.uppercase_welcome = $(e.target).prop('checked')
//     this.uppercase_user = $(e.target).prop('checked')
//   }

//   notify(event) {
//     let welcome = this.uppercase_welcome ? this.welcome_model.message.toUpperCase() : this.welcome_model.message
//     let firstname = this.uppercase_user ? this.user_model.firstname.toUpperCase() : this.user_model.firstname
//     let surname = this.uppercase_user ? this.user_model.surname.toUpperCase() : this.user_model.surname
//     $('#' + this.gui_div).html(welcome + ' ' + firstname + ' ' + surname )
//   }
// }

// class MediatorEditWelcome {
//   constructor(welcome_model, id) {
//     this.welcome_model = welcome_model
//     this.gui_input = id  // name (not id) of input to hold welcome message
//   }

//   on_keychar_welcome(e) { this.welcome_model.message = $(e.target).val() }

//   notify(event) {
//     $(`input[name=${this.gui_input}]`).val(this.welcome_model.message)
//   }
// }

// class MediatorEditUserFirstName {
//   constructor(user_model, id) {
//     this.user_model = user_model
//     this.gui_input = id
//   }

//   on_keychar_firstname(e) { this.user_model.firstname = $(e.target).val() }

//   notify(event) {
//     $(`input[name=${this.gui_input}]`).val(this.user_model.firstname)
//   }
// }

// class MediatorEditUserSurName {
//   constructor(user_model, id) {
//     this.user_model = user_model
//     this.gui_input = id
//   }
  
//   on_keychar_surname(e) { this.user_model.surname = $(e.target).val() }

//   notify(event) {
//     $(`input[name=${this.gui_input}]`).val(this.user_model.surname)
//   }
// }

// class MediatorPageTitle {
//   constructor(s, $id) {
//     this.s = s
//     this.$id = $id
//   }
  
//   notify(event) {
//     this.$id.html(this.s)
//   }
// }

// class DebugDumpModels {
//   constructor(id) {
//     this.gui_pre_id = id
//   }
  
//   notify(event) {
//     let info = {
//       app_models: app,
//       mediator_welcome: mediator_welcome,
//       mediator_welcome_user : mediator_welcome_user,
//       mediator_edit_welcome : mediator_edit_welcome,
//       mediator_edit_firstname : mediator_edit_firstname,
//       mediator_edit_user_surname : mediator_edit_user_surname,
//     }
//     $(`#${this.gui_pre_id}`).html(syntaxHighlight(JSON.stringify(info, null, 2)))
//   }
// }

// Util

function isUpperCaseAt(str, n) {
    return str[n]=== str[n].toUpperCase();
}  

//
// Create the app and mediators
//

// app = new App(new Welcome(), new User())

// // Mediators (old)
// mediator_welcome = new MediatorWelcome(app.welcome_model, "welcome")
// mediator_welcome_user = new MediatorWelcomeUser(app.welcome_model, app.user_model, 'welcome-user')
// mediator_edit_welcome = new MediatorEditWelcome(app.welcome_model, 'welcome')
// mediator_edit_firstname = new MediatorEditUserFirstName(app.user_model, 'firstname')
// mediator_edit_user_surname = new MediatorEditUserSurName(app.user_model, 'surname')
// mediator_page_title = new MediatorPageTitle("Gui wired via MVCA Architecture", $('#title > h1'))
// mediator_debug_info = new DebugDumpModels("debug_info")

// // Observer Wiring
// document.addEventListener("modified welcome", (event) => { mediator_welcome.notify(event) })
// document.addEventListener("modified welcome", (event) => { mediator_welcome_user.notify(event) })
// document.addEventListener("modified welcome", (event) => { mediator_edit_welcome.notify(event) })
// document.addEventListener("modified user", (event) =>    { mediator_welcome_user.notify(event) })
// document.addEventListener("modified user", (event) =>    { mediator_edit_firstname.notify(event) })
// document.addEventListener("modified user", (event) =>    { mediator_edit_user_surname.notify(event) })
// document.addEventListener("startup", (event) =>          { mediator_page_title.notify(event) })
// document.addEventListener("display option change", (event) => { mediator_welcome.notify(event) })
// document.addEventListener("display option change", (event) => { mediator_welcome_user.notify(event) })
// document.addEventListener("notify all called", (event) => { mediator_debug_info.notify(event) })

// // Gui Event Wiring - front line controller event hander functions

// // button click commands that change the model, go to the app controller
// $('#change_welcome_model').on('click', (event) => { app.on_change_welcome_model(event) })
// $('#change_user_model').on('click', (event) => { app.on_change_user_model(event) })
// $('#reset_welcome_model').on('click', (event) => { app.on_reset_welcome_model(event) })
// $('#reset_user_model').on('click', (event) => { app.on_reset_user_model(event) })
// $('#render-now').on('click', function(e) { app.dirty_all() })
// // text input keystrokes that edit the model, go to the individual mediator controllers
// $('input[name=welcome]').on('keyup', (event) => { mediator_edit_welcome.on_keychar_welcome(event) })
// $('input[name=firstname]').on('keyup', (event) => { mediator_edit_firstname.on_keychar_firstname(event) })
// $('input[name=surname]').on('keyup', (event) => { mediator_edit_user_surname.on_keychar_surname(event) })
// // checkbox display options that change the way the models are rendered, go to the individual mediator controllers
// $('input[name=uppercase_welcome]').on('change', (event) => { mediator_welcome.on_check_upper_welcome(event) })
// $('input[name=uppercase_welcome]').on('change', (event) => { mediator_welcome_user.on_check_upper_welcome(event) })
// $('input[name=uppercase_user]').on('change', (event) => { mediator_welcome_user.on_check_upper_user(event) })
// $('input[name=uppercase_welcome_user]').on('change', (event) => { mediator_welcome_user.on_check_upper_welcome_user(event) })

// app.dirty_startup()  // initialise the gui with initial model values

// New


// (function (window) {
// 	'use strict';

	/*  
		Start here!
		
		Create an instance of 'Application' passing in a config object.

		Controller classes and this config of callbacks are the only things
	 	that know about the UI.
	*/
  // let config = {}

	let config = {
	// 	// Callback to create the todo item controllers - are added as needed

	// 	cb_todo: function (app, todo) {
	// 		new ControllerTodoItem(
	// 			app,
	// 			todo,
	// 			{ $todolist: $('ul.todo-list') }
	// 		)
	// 	},

	// 	// Callbacks to create the permanent controllers

	// 	cb_dump: function (app) {
	// 		new ControllerDebugDumpModels(
	// 			app,
	// 			{
	// 				$toggle_checkbox: $('input[name="debug"]'),
	// 				pre_output: document.querySelector('pre.debug')
	// 			}
	// 		)
	// 	},
		// cb_header: function (app) {
		// 	new ControllerHeader(
		// 		app,
		// 		{
		// 			$input: $('.new-todo'),
		// 			$toggle_all: $('.toggle-all')
		// 		}
		// 	)
		// }
	// 	cb_footer: function (app) {
	// 		new ControllerFooter(
	// 			app,
	// 			{
	// 				$footer: $('footer'),
	// 				$footer_interactive_area: $('.footer')
	// 			})
	// 	}
	}

	let app = new Application(config)
  console.log('created new application')

  // Controllers
  let controller_welcome = new ControllerHeader(app, {
    $title_welcome: $('#welcome'),
    $title_welcome_user: $('#welcome-user'),
  })

  let controller_display_options = new ControllerDisplayOptions(app, {
    $cb_uppercase_welcome: $('input[name=uppercase_welcome]'),
    $cb_uppercase_user: $('input[name=uppercase_user]'),
    $cb_uppercase_welcome_user: $('input[name=uppercase_welcome_user]'),    
  })

// })(window);

