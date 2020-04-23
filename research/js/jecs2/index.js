// Andy revamp - Apr 2020 - "its gotta be simpler than my first attempt!"

// Instantiating engine, timer and simulator
var engine = new Jecs.Engine();
var sim = new Jecs.Simulator(engine);
  
// Instantiate a new engine
// const engine = new Engine();

// Declare entities
const message = engine.entity('model-welcome-message');
const firstname = engine.entity('model-firstname');
const surname = engine.entity('model-surname');


// Associate the player entity to components.
// In this case we set 'position' and 'speed'.
// player.setComponent('position', { x: 0, y: 0 });
// player.setComponent('speed', { x: 0.5, y: 0.7 });
message.setComponent('data', {val: ""})
firstname.setComponent('data', {val: ""})
surname.setComponent('data', {val: ""})

// Define a 'move' system for updating position of
// entities associated to components 'position' and 'speed'
engine.system('render', ['data'], (entity, {data}) => {
  data.val += "x"
  console.log('hi', entity.name, data.val)
});

// If you prefer, you can avoid using simulator and start
// engine iterations manually by calling engine.tick() in a loop.

// Limit the fps to 60
sim.setFps(6);

// Start simulator
sim.start();

setInterval(function() { sim.stop() }, 3000);
