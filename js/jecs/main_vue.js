//
// Model - The Welcome model and User model are Observable.
//

model = {
  welcomemsg: "Welcome", 
  user: {
    firstname: "Sam", 
    surname: "Smith"
  }
}

// Vue magic - a mediating observer + more

var vm = new Vue({
  el:"#app",
  data: {
    model: model,  // shared state - could be a vuex one day
    uppercase_welcome: false,
    uppercase_user: false,
    uppercase_welcome_user: false,  // just the top right combined message
  },
  methods:  {
    _isUpperCaseAt(str, n) {  // util
      return str[n]=== str[n].toUpperCase();
    },
    change_welcome_model: function (data) {
      this.model.welcomemsg = this._isUpperCaseAt(this.model.welcomemsg, 1) ? this.model.welcomemsg.toLowerCase() : this.model.welcomemsg.toUpperCase()
    },
    change_user_model: function (data) {
      this.model.user.firstname = this._isUpperCaseAt(this.model.user.firstname, 1) ? this.model.user.firstname.toLowerCase() : this.model.user.firstname.toUpperCase()
      this.model.user.surname = this._isUpperCaseAt(this.model.user.surname, 1) ? this.model.user.surname.toLowerCase() : this.model.user.surname.toUpperCase()
    },
    reset_welcome_model: function (data) {
      this.model.welcomemsg = "Hello"
    },
    reset_user_model: function (data) {
      this.model.user.firstname = "Fred"
      this.model.user.surname = "Flinstone"
    },
  },
  computed: {
    welcome_msg: function() { 
      let welcome = this.uppercase_welcome ? this.model.welcomemsg.toUpperCase() : this.model.welcomemsg
      return welcome
    },
    welcome_user_msg: function() { 
      let welcome = (this.uppercase_welcome || this.uppercase_welcome_user) ? this.model.welcomemsg.toUpperCase() : this.model.welcomemsg
      let firstname = (this.uppercase_user || this.uppercase_welcome_user) ? this.model.user.firstname.toUpperCase() : this.model.user.firstname
      let surname = (this.uppercase_user || this.uppercase_welcome_user) ? this.model.user.surname.toUpperCase() : this.model.user.surname
      return welcome + ' ' + firstname + ' ' + surname 
    },
    dump_vue_data: function () {
      return syntaxHighlight(JSON.stringify(this._data, null, 2))
    }
  }
})
