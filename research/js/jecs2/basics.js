// Andy revamp - Apr 2020 - "its gotta be simpler than my first attempt!"

// $(document).ready(function() {
var app = (function () {

  // Instantiating engine, timer and simulator
  var engine = new Jecs.Engine();
    
  // Declare entities
  const message = engine.entity('model-welcome-message');
  const firstname = engine.entity('model-firstname');
  const surname = engine.entity('model-surname');

  // Associate the model entities to components.
  message.setComponent('data', {val: "Welcome"})
  firstname.setComponent('data', {val: "Sam"})
  surname.setComponent('data', {val: "Smith"})

  message.setComponent('displayOptions', {upper: false})
  surname.setComponent('displayOptions', {upper: false})

  function toggle_message_case() {
    let options = message.getComponent('displayOptions')
    options.upper = !options.upper
  }
  
  function toggle_surname_case() {
    let options = surname.getComponent('displayOptions')
    options.upper = !options.upper
  }
  
  engine.on('tick:before', (engine) => { log_clear() })

  engine.system('pre-render', ['data', 'displayOptions'], (entity, {data, displayOptions}) => {
    data.val = displayOptions.upper ? data.val.toUpperCase() : data.val.toLowerCase()
    // console.log('hi', entity.name, displayOptions, data.val)
  });

  // buffer
  let welcome_user_render = {welcome, firstname, surname}  // create an empty object to buffer

  // Define a 'render' system for updating val of
  // entities associated to components 'data'
  engine.system('render', ['data'], (entity, {data}) => {
    // data.val += "x"
    console.log('hi', entity.name, data.val)
    
    // how to distinguish re who the data is from? Ans: Check entity.name
    // but how to do a combo display that relies on TWO model entities - here we get only one at a time. Ans. buffer?
    if (entity.name == 'model-welcome-message') {
      $('#welcome').html(data.val)
      $('input[name=welcome]').val(data.val)
      welcome_user_render.welcome = data.val
    }
    else if (entity.name == 'model-firstname') {
      $('input[name=firstname]').val(data.val)
      welcome_user_render.firstname = data.val
    }
    else if (entity.name == 'model-surname') {
      $('input[name=surname]').val(data.val)
      welcome_user_render.surname = data.val
    }
    else {
      console.log('unknown?')
    }

    log(`render: ${entity.name}, ${data.val}`);
  });

  engine.on('tick:after', (engine) => { 
    // flush out pending renders
    $('#welcome-user').html(`${welcome_user_render.welcome} ${welcome_user_render.firstname} ${welcome_user_render.surname} `)
  })


  // util

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
    // simulator: sim,
    toggle_message_case: toggle_message_case,
    toggle_surname_case: toggle_surname_case,
    engine: engine,
    // reset: function() {
    //   init();
    //   draw();
    // },
  }
  
}());

