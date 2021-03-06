//
// Models
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

// Util

function isUpperCaseAt(str, n) {
    return str[n]=== str[n].toUpperCase();
}  

// Update 

function update_welcome() {
  let msg = display_options.uppercase_welcome ? model.welcomemsg.toUpperCase() : model.welcomemsg
  $('#welcome').html(msg)
}

function update_welcome_user() {
  let welcome = (display_options.uppercase_welcome || display_options.uppercase_welcome_user) ? model.welcomemsg.toUpperCase() : model.welcomemsg
  let firstname = (display_options.uppercase_user || display_options.uppercase_welcome_user) ? model.user.firstname.toUpperCase() : model.user.firstname
  let surname = (display_options.uppercase_user || display_options.uppercase_welcome_user) ? model.user.surname.toUpperCase() : model.user.surname
  $('#welcome-user').html(welcome + ' ' + firstname + ' ' + surname )
}

function update_edit_welcome_input() {
  $('input[name=welcome]').val(model.welcomemsg)
}

function update_edit_firstname_input() {
  $('input[name=firstname]').val(model.user.firstname)
}

function update_edit_surname_input() {
  $('input[name=surname]').val(model.user.surname)
}

function update_page_title() {
  $('#title > h1').html("Gui wired via Plain JQuery")
}


function update_debug_dump_models() {
  let info = {
    model: model,
    display_options: display_options
  }
  $('#debug_info').html(syntaxHighlight(JSON.stringify(info, null, 2)))
}

function update_all() {
  update_welcome()
  update_welcome_user()
  update_edit_welcome_input()
  update_edit_firstname_input()
  update_edit_surname_input()
  update_page_title()
  update_debug_dump_models()
}

//
// GUI events
//

$('#change_welcome_model').on('click', function(e) {
  model.welcomemsg = isUpperCaseAt(model.welcomemsg, 1) ? model.welcomemsg.toLowerCase() : model.welcomemsg.toUpperCase()
  update_welcome()
  update_welcome_user()
  update_edit_welcome_input()
  update_debug_dump_models()
})

$('#change_user_model').on('click', function(e) {
  model.user.firstname = isUpperCaseAt(model.user.firstname, 1) ? model.user.firstname.toLowerCase() : model.user.firstname.toUpperCase()
  model.user.surname = isUpperCaseAt(model.user.surname, 1) ? model.user.surname.toLowerCase() : model.user.surname.toUpperCase()
  update_welcome_user()
  update_edit_firstname_input()
  update_edit_surname_input()
  update_debug_dump_models()
})

$('#reset_welcome_model').on('click', function(e) {
  model.welcomemsg = "Hello"
  update_welcome()
  update_welcome_user()
  update_edit_welcome_input()
  update_debug_dump_models()
})

$('#reset_user_model').on('click', function(e) {
  model.user.firstname = "Fred"
  model.user.surname = "Flinstone"
  update_welcome_user()
  update_edit_firstname_input()
  update_edit_surname_input()
  update_debug_dump_models()
})

$("input[name=uppercase_welcome]").on('change', function(e) {
  display_options.uppercase_welcome = $(e.target).prop('checked')
  update_welcome()
  update_welcome_user()
  update_debug_dump_models()
})

$("input[name=uppercase_user]").on('change', function(e) {
  display_options.uppercase_user = $(e.target).prop('checked')
  update_welcome_user()
  update_debug_dump_models()
})

$("input[name=uppercase_welcome_user]").on('change', function(e){
  display_options.uppercase_welcome_user = $(e.target).prop('checked')
  update_welcome_user()
  update_debug_dump_models()
});

$( "input[name=welcome]" ).on('keyup', function(e) {  // use 'change' if you want to wait for ENTER
  model.welcomemsg = $(e.target).val()
  update_welcome()
  update_welcome_user()
  update_debug_dump_models()
});

$("input[name=firstname]").on('keyup', function(e) {
  model.user.firstname = $(e.target).val()
  update_welcome_user()
  update_debug_dump_models()
})

$("input[name=surname]").on('keyup', function(e) {
  model.user.surname = $(e.target).val()
  update_welcome_user()
  update_debug_dump_models()
})

$('#render-now').on('click', function(e) {
  update_all()
})

update_all()
