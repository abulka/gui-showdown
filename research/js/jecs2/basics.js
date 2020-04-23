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

  function toggle_message_case() {
    let options = message.getComponent('displayOptions')
    options.upper = !options.upper
  }
  
  engine.on('tick:before', (engine) => { log_clear() })

  engine.system('pre-render', ['data', 'displayOptions'], (entity, {data, displayOptions}) => {
    data.val = displayOptions.upper ? data.val.toUpperCase() : data.val.toLowerCase()
    // console.log('hi', entity.name, displayOptions, data.val)
  });

  // Define a 'render' system for updating val of
  // entities associated to components 'data'
  engine.system('render', ['data'], (entity, {data}) => {
    // data.val += "x"
    console.log('hi', entity.name, data.val)
    log(`render: ${entity.name}, ${data.val}`);
  });



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
    engine: engine,
    // reset: function() {
    //   init();
    //   draw();
    // },
  }
  
}());

