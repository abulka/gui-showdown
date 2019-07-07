//
// Model
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

// util

function isUpperCaseAt(str, n) {
    return str[n]=== str[n].toUpperCase();
}  

function update_welcome_top_left() {
  $('#welcome').html(model.welcomemsg)
}

function update_welcome_user_top_right() {
  let welcome = (display_options.uppercase_welcome || display_options.uppercase_welcome_user) ? model.welcomemsg.toUpperCase() : model.welcomemsg
  let firstname = (display_options.uppercase_user || display_options.uppercase_welcome_user) ? model.user.firstname.toUpperCase() : model.user.firstname
  let surname = (display_options.uppercase_user || display_options.uppercase_welcome_user) ? model.user.surname.toUpperCase() : model.user.surname
  $('#welcome-user').html(welcome + ' ' + firstname + ' ' + surname )
}

function update_all() {
  update_welcome_top_left()
  update_welcome_user_top_right()
}


//
// GUI events
//

$('#change_welcome_model').on('click', function(e) {
  // even this modelling might be too much for this pure approach !!  but we do need a pure model...!!!!
  model.welcomemsg = isUpperCaseAt(model.welcomemsg, 1) ? model.welcomemsg.toLowerCase() : model.welcomemsg.toUpperCase()
  update_welcome_top_left()
  update_welcome_user_top_right()
})

$('#change_user_model').on('click', function(e) {
  model.user.firstname = isUpperCaseAt(model.user.firstname, 1) ? model.user.firstname.toLowerCase() : model.user.firstname.toUpperCase()
  model.user.surname = isUpperCaseAt(model.user.surname, 1) ? model.user.surname.toLowerCase() : model.user.surname.toUpperCase()
  update_welcome_user_top_right()
})

$('#reset_welcome_model').on('click', function(e) {
  model.welcomemsg = "Hello"
  update_welcome_top_left()
  update_welcome_user_top_right()
})

$('#reset_user_model').on('click', function(e) {
  model.user.firstname = "Fred"
  model.user.surname = "Flinstone"
  update_welcome_user_top_right()
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

// //
// // Wire up and build everything
// //

// model = new Model(new Welcome(), new User())
// mediator_welcome_left = new MediatorWelcomeLeft(model.welcome, "welcome")
// mediator_welcome_user_right = new MediatorWelcomeUserRight(model.welcome, model.user, 'welcome-user')
// mediator_edit_welcome_msg = new MediatorEditWelcome(model.welcome, 'welcome')
// mediator_edit_user_name_msg = new MediatorEditUserFirstName(model.user, 'firstname')
// mediator_edit_user_surname_msg = new MediatorEditUserSurName(model.user, 'surname')
// display_options = new DisplayOptions()
// mediator_dump_models = new MediatorDumpModels("debug_info")

// // Observer Wiring
// model.welcome.add_observer(mediator_welcome_left)
// model.welcome.add_observer(mediator_welcome_user_right)
// model.welcome.add_observer(mediator_edit_welcome_msg)
// model.user.add_observer(mediator_welcome_user_right)
// model.user.add_observer(mediator_edit_user_name_msg)
// model.user.add_observer(mediator_edit_user_surname_msg)
// display_options.add_observer(mediator_welcome_left)
// display_options.add_observer(mediator_welcome_user_right)
// // debug mediator 
// model.welcome.add_observer(mediator_dump_models)
// model.user.add_observer(mediator_dump_models)
// display_options.add_observer(mediator_dump_models)

// model.dirty_all()  // initialise the gui with initial model values

update_all()
