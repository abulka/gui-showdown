// Andy revamp - Apr 2020 - "its gotta be simpler than my first attempt!"

// Instantiating engine, timer and simulator
var engine = new Jecs.Engine();
var sim = new Jecs.Simulator(engine);
  
// Declare entities
const message = engine.entity('model-welcome-message');
const firstname = engine.entity('model-firstname');
const surname = engine.entity('model-surname');

// Associate the model entities to components.
message.setComponent('data', {val: ""})
firstname.setComponent('data', {val: ""})
surname.setComponent('data', {val: ""})

// Define a 'render' system for updating val of
// entities associated to components 'data'
engine.system('render', ['data'], (entity, {data}) => {
  data.val += "x"
  console.log('hi', entity.name, data.val)
});

// If you prefer, you can avoid using simulator and start
// engine iterations manually by calling engine.tick() in a loop.

// Limit the fps to 6
sim.setFps(6);

// Start simulator
sim.start();

// Stop simulator after three seconds
setInterval(function() { sim.stop() }, 3000);
