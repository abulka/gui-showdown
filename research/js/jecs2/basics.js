// Andy revamp - Apr 2020 - "its gotta be simpler than my first attempt!"

// $(document).ready(function() {
var app = (function () {

  // Instantiating engine, timer and simulator
  var engine = new Jecs.Engine();
    
  // Declare entities - this is like the model, but without data - we attach that later, as 'components'
  const message = engine.entity('model-welcome-message');
  const firstname = engine.entity('model-firstname');
  const surname = engine.entity('model-surname');

  // Associate the model entities to components.
  message.setComponent('data', {val: "Welcome"})
  firstname.setComponent('data', {val: "Sam"})
  surname.setComponent('data', {val: "Smith"})

  // we need display option re uppercase for welcome, the whole user, and the 'welcome user' message (top right)
  // only the first is an entity, the second is a combo of two entities and the third is a combo of three
  message.setComponent('displayOptions', {upper: false})
  firstname.setComponent('displayOptions', {upper: false})
  surname.setComponent('displayOptions', {upper: false})

  // Set Model

  function set_message(val) {
    message.getComponent('data').val = val
  }
  function set_firstname(val) {
    firstname.getComponent('data').val = val
  }
  function set_surname(val) {
    surname.getComponent('data').val = val
  }

  // Toggle Model
  
  function toggle_message() {
    let data = message.getComponent('data')
    data.val = toggleCase(data.val)
  }

  function toggle_user() {
    let data = firstname.getComponent('data')
    data.val = toggleCase(data.val)
    data = surname.getComponent('data')
    data.val = toggleCase(data.val)
  }
  
  // Display Option Checkbox toggles

  function display_option_toggle_message_case(flag) {
    // the key is in here - display options need to be associated with maybe ???
    let options = message.getComponent('displayOptions')
    options.upper = flag //!options.upper
  }
  
  function display_option_toggle_surname_case(flag) {
    let options = surname.getComponent('displayOptions')
    options.upper = flag //!options.upper
  }
    
  function display_option_toggle_firstname_case(flag) {
    let options = firstname.getComponent('displayOptions')
    options.upper = flag //!options.upper
  }

  engine.on('tick:before', (engine) => { log_clear() })

  // engine.system('pre-render', ['data', 'displayOptions'], (entity, {data, displayOptions}) => {
  //   // data.val = displayOptions.upper ? data.val.toUpperCase() : data.val.toLowerCase()
  //   // console.log('hi', entity.name, displayOptions, data.val)
  // });

  // Define a 'render' system for updating val of
  // entities associated to components 'data'
  engine.system('render-model', ['data'], (entity, {data}) => {
    // how to distinguish re who the data is from? Ans: Check entity.name
    // but how to do a combo display that relies on TWO model entities - here we get only one at a time. Ans. buffer?
    if (entity.name == 'model-welcome-message') {
      $('input[name=welcome]').val(data.val)
    }
    else if (entity.name == 'model-firstname') {
      $('input[name=firstname]').val(data.val)
    }
    else if (entity.name == 'model-surname') {
      $('input[name=surname]').val(data.val)
    }
    else {
      console.log('unknown render-model entity?')
    }

    log(`render-model: ${entity.name}, ${data.val}`);
  });

  // buffer
  let welcome_user_render = {welcome, firstname, surname}  // create an empty object to buffer

  engine.system('render-display', ['data', 'displayOptions'], (entity, {data, displayOptions}) => {
    
    // how to distinguish re who the data is from? Ans: Check entity.name
    // but how to do a combo display that relies on TWO model entities - here we get only one at a time. Ans. buffer?
    if (entity.name == 'model-welcome-message') {
      let val = displayOptions.upper ? data.val.toUpperCase() : data.val
      $('#welcome').html(val)
      welcome_user_render.welcome = val
    }
    else if (entity.name == 'model-firstname') {
      let val = displayOptions.upper ? data.val.toUpperCase() : data.val
      welcome_user_render.firstname = val
    }
    else if (entity.name == 'model-surname') {
      let val = displayOptions.upper ? data.val.toUpperCase() : data.val
      welcome_user_render.surname = val
    }
    else {
      console.log('unknown render-display entiry?')
    }

    log(`render-display: ${entity.name}, ${data.val}`);
  });

  engine.on('tick:after', (engine) => { 
    // flush out pending renders
    $('#welcome-user').html(`${welcome_user_render.welcome} ${welcome_user_render.firstname} ${welcome_user_render.surname} `)
  })


  // Util - Logging

  var logarea = document.getElementById('log');

  // Append a line of log
  function log(text) {
    var html = logarea.innerHTML;
    html += (text || '') + '<br/>';
    logarea.innerHTML = html;

    // Scroll log to bottom
    logarea.scrollTop = logarea.scrollHeight;
  }
  function log_clear() {
    logarea.innerHTML = ""
    logarea.scrollTop = logarea.scrollHeight;
  }

  // Util

  function isUpperCaseAt(str, n) {
    return str[n]=== str[n].toUpperCase();
  }

  function toggleCase(str) {  // determine case of string based on arbitrary choice of char 1
    return isUpperCaseAt(str, 1) ? str.toLowerCase() : str.toUpperCase()
  }

  engine.tick()

  /*

  // If you prefer, you can avoid using simulator and start
  // engine iterations manually by calling engine.tick() in a loop.
  var sim = new Jecs.Simulator(engine);

  // Limit the fps to 6
  sim.setFps(6);

  // Start simulator
  sim.start();

  // Stop simulator after three seconds
  setInterval(function() { sim.stop() }, 3000);

  */


// });

  return {
    set_message,
    set_firstname,
    set_surname,
    
    toggle_message,
    toggle_user,
    
    display_option_toggle_message_case,
    display_option_toggle_surname_case,
    display_option_toggle_firstname_case,
    engine,    
  }

  // return {
  //   // simulator: sim,
  //   set_message: set_message,
  //   set_firstname: set_firstname,
  //   set_surname: set_surname,

  //   toggle_message: toggle_message,
  //   toggle_user: toggle_user,

  //   display_option_toggle_message_case: display_option_toggle_message_case,
  //   toggle_surname_case: toggle_surname_case,
  //   engine: engine,
  //   // reset: function() {
  //   //   init();
  //   //   draw();
  //   // },
  // }
  
}());

