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


//
// Application
//


class Application {
  constructor(config) {
    this.config = config  // callbacks for creating controllers

    // Models
    this.welcome_model = new Welcome()
    this.user_model = new User()

    // View state (used to live in controllers in OO version), these control the display of the header titles at top
    this._uppercase_welcome = false
    this._uppercase_user = false
    this._uppercase_welcome_user = false

    this.config.cb_create_controllers1(this)
    this.config.cb_create_controllers2(this)
    this.config.cb_debug_dump_controller(this)

    this.dirty_startup()
  }

  // getters / setters which broadcast

  get uppercase_welcome() {
    return this._uppercase_welcome
  }
  set uppercase_welcome(val) {
    this._uppercase_welcome = val
    notify_all("display option change", this, { what: 'uppercase_welcome', is_upper: val })
  }

  get uppercase_user() {
    return this._uppercase_user
  }
  set uppercase_user(val) {
    this._uppercase_user = val
    notify_all("display option change", this, { what: 'uppercase_user', is_upper: val })
  }

  get uppercase_welcome_user() {
    return this._uppercase_welcome_user
  }
  set uppercase_welcome_user(val) {
    this._uppercase_welcome_user = val
    notify_all("display option change", this, { what: 'uppercase_welcome_user', is_upper: val })
  }

  // business logic

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

  dirty_startup() {
    notify_all("startup", this)
  }
}


//
// Controllers
//


class ControllerHeader {
  constructor(app, gui_dict) {
    this.app = app          // ref to Welcome model in app.welcome_model
    this.gui = gui_dict     // refs to DOM div where we want the welcome and welcome user message to appear

    // Gui events - none, because these are 'display only' titles, its the other controller that handles checkbox inputs

    // Internal events - we listen via 'notify()' in order to display as per the view state
    document.addEventListener("display option change", (event) => { this.notify(event) })
    document.addEventListener("startup", (event) => { this.notify(event) })
    document.addEventListener("modified welcome", (event) => { this.notify(event) })
    document.addEventListener("modified user", (event) => { this.notify(event) })  // either firstname or surname
  }

  _debug_report_state() {
    let report = {}
    report[this.constructor.name] = {
      gui: Object.keys(this.gui),
      listening: {
        gui_events: [],
        internal_events: ["display option change", "modified welcome", "modified user", "startup"]
      },
    }
    return report
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

  _debug_report_state() {
    let report = {}
    report[this.constructor.name] = {
      gui: Object.keys(this.gui),
      listening: {
        gui_events: 'change',
        internal_events: []
      },
    }
    return report
  }
}


class ControllerEditors {
  constructor(app, gui_dict) {
    this.app = app
    this.gui = gui_dict

    // Gui events -> this controller, which then manipulate the model
    this.gui.$input_welcome.on('keyup', (event) => { this.app.welcome_model.message = $(event.target).val() })
    this.gui.$input_firstname.on('keyup', (event) => { this.app.user_model.firstname = $(event.target).val() })
    this.gui.$input_surname.on('keyup', (event) => { this.app.user_model.surname = $(event.target).val() })

    // Internal events - typically from the model
    document.addEventListener("modified welcome", (event) => { this.notify(event) })
    document.addEventListener("modified user", (event) => { this.notify(event) })  // either firstname or surname
    document.addEventListener("startup", (event) => { this.notify(event) })
  }

  notify(event) {
    console.log(`\tControllerEditors got event '${event.type}' data is '${JSON.stringify(event.detail.data)}'`)
    if (event.type == "startup") {
      this.gui.$input_welcome.val(this.app.welcome_model.message)
      this.gui.$input_firstname.val(this.app.user_model.firstname)
      this.gui.$input_surname.val(this.app.user_model.surname)
    }
    // this level of granular updates is tedious, could always update all input fields each time if you wanted
    else if (event.type == "modified welcome")
      this.gui.$input_welcome.val(this.app.welcome_model.message)
    else if (event.type == "modified user") {
      this.gui.$input_firstname.val(this.app.user_model.firstname)
      this.gui.$input_surname.val(this.app.user_model.surname)
    }
  }

  _debug_report_state() {
    let report = {}
    report[this.constructor.name] = {
      gui: Object.keys(this.gui),
      listening: {
        gui_events: 'keyup',
        internal_events: ["modified welcome", "modified user", "startup"]
      },
    }
    return report
  }
}


class ControllerButtons {  // The four buttons which cause a change in the models
  constructor(app, gui_dict) {
    this.app = app
    this.gui = gui_dict

    // Gui events -> this controller, which then manipulate the model via the app
    this.gui.$btn_change_welcome_model.on('click', (event) => { this.app.on_change_welcome_model(event) })
    this.gui.$btn_change_user_model.on('click', (event) => { this.app.on_change_user_model(event) })
    this.gui.$btn_reset_welcome_model.on('click', (event) => { this.app.on_reset_welcome_model(event) })
    this.gui.$btn_reset_user_model.on('click', (event) => { this.app.on_reset_user_model(event) })

    // Internal events - none, this controller just listens to gui
  }

  _debug_report_state() {
    let report = {}
    report[this.constructor.name] = {
      gui: Object.keys(this.gui),
      listening: {
        gui_events: 'click',
        internal_events: []
      },
    }
    return report
  }
}


class ControllerPageTitle {
  constructor(app, $gui_h1, title) {
    this.app = app
    this.$gui_h1 = $gui_h1
    this.title = title

    // Internal events - only runs at startup and never changes
    document.addEventListener("startup", (event) => { this.notify(event) })
  }

  _debug_report_state() {
    let report = {}
    report[this.constructor.name] = {
      gui: '$gui_h1',
      listening: {
        gui_events: [],
        internal_events: ["startup"]
      },
    }
    return report
  }

  notify(event) {
    this.$gui_h1.html(this.title)
  }
}


class ControllerDebugDumpModels {
  constructor(app, gui_dict) {
    this.app = app
    this.gui = gui_dict

    // Gui events
    this.gui.$toggle_checkbox.on('change', (event) => { this.display_debug_info(event) })

    // Internal events - listen to special meta event which is broadcast each event
    document.addEventListener("notify all called", (event) => { this.notify(event) })
  }

  display_debug_info(event) {
    this.gui.$pre_output[0].style.display = event.target.checked ? 'block' : 'none'
  }

  
  _debug_report_state() {
    let report = {}
    report[this.constructor.name] = {
      gui: Object.keys(this.gui),
      listening: {
        gui_events: ['change'],
        internal_events: ["notify all called"]
      }
    }
    return report
  }

  notify(event) {

    // build controller report
    let all_controllers_info = {}
    for (const controller of all_controllers) {
      let dict = controller._debug_report_state()
      let key = Object.keys(dict)[0]
      all_controllers_info[key] = dict[key]
    }

    let info = {
      app: this.app,
      controllers: all_controllers_info,
    }
    this.gui.$pre_output.html(syntaxHighlight(JSON.stringify(info, null, 2)))

  }
}


// Util

function isUpperCaseAt(str, n) {
  return str[n] === str[n].toUpperCase();
}


//
// Bootstrapping
//

let all_controllers = []  // record them for debug dump purposes

let config = {
  // Controller classes and this config of callbacks (to create the controllers) are the only things
  // that know about the UI.


  cb_debug_dump_controller: function (app) {
    all_controllers.push(
      new ControllerDebugDumpModels(
        app,
        {
          $toggle_checkbox: $('input[name="debug"]'),
          $pre_output: $('#debug_info')

        }
      ))
  },

  cb_create_controllers1: function (app) {
    all_controllers.push(
      new ControllerHeader(app, {
        $title_welcome: $('#welcome'),
        $title_welcome_user: $('#welcome-user'),
      }))

    all_controllers.push(
      new ControllerDisplayOptions(app, {
        $cb_uppercase_welcome: $('input[name=uppercase_welcome]'),
        $cb_uppercase_user: $('input[name=uppercase_user]'),
        $cb_uppercase_welcome_user: $('input[name=uppercase_welcome_user]'),
      }))
  },

  cb_create_controllers2: function (app) {
    all_controllers.push(
      new ControllerEditors(app, {
        $input_welcome: $('input[name=welcome]'),
        $input_firstname: $('input[name=firstname]'),
        $input_surname: $('input[name=surname]')
      }))

    all_controllers.push(
      new ControllerButtons(app, {
        $btn_change_welcome_model: $('#change_welcome_model'),
        $btn_change_user_model: $('#change_user_model'),
        $btn_reset_welcome_model: $('#reset_welcome_model'),
        $btn_reset_user_model: $('#reset_user_model'),
      }))

    all_controllers.push(
      new ControllerPageTitle(app, $('#title > h1'), "Gui wired via MVCA Architecture"))
  }

}

// Create an instance of 'Application' passing in a config object.
let app = new Application(config)
