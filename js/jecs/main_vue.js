//
// Model - The Welcome model and User model are Observable.
//

model = {"welcome_msg": "Welcome", "user": {"name": "Sam", "surname": "Smith"}}

// Vue magic - a mediating observer + more

var vm = new Vue({
  el:"#app",
  data: {
    model: model,  // shared state - could be a vuex one day
    welcome_model_uppercased: false,
    uppercase_welcome: false,
    uppercase_all: false,
  },
  methods:  {
    toggle_welcome_model: function (data) {
      this.model.welcome_msg = this.welcome_model_uppercased ? this.model.welcome_msg.toUpperCase() : this.model.welcome_msg.toLowerCase()
    },
    dump: function() { 
      $('#log').html(syntaxHighlight(JSON.stringify(this._data, null, 2)))  // debug, display entire vue data incl. sub ref to shared model
    }
  },
  updated() {
    this.dump()
  },  
  mounted() {
    this.dump()
  },  
  computed: {
    welcome_msg: function() { 
      let welcome = (this.uppercase_welcome || this.uppercase_all) ? this.model.welcome_msg.toUpperCase() : this.model.welcome_msg
      return welcome
    },
    welcome_user_msg: function() { 
      let welcome = (this.uppercase_welcome || this.uppercase_all) ? this.model.welcome_msg.toUpperCase() : this.model.welcome_msg
      let firstname = this.model.user.name
      let surname = this.model.user.surname
      if (this.uppercase_all) {
        firstname = firstname.toUpperCase()
        surname = surname.toUpperCase()
      }
      return welcome + ' ' + firstname + ' ' + surname 
    }
  }
})

//
// GUI events
//

$('#reset-welcome').on('click', function(e) {
  model.welcome_msg = "Hello"
})

$('#reset-user').on('click', function(e) {
  model.user.name = "Fred"
  model.user.surname = "Flinstone"
})
