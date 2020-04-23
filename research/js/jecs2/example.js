// import { Engine, Simulator } from 'jecs';

// Instantiating engine, timer and simulator
var engine = new Jecs.Engine();
var timer = new Jecs.Timer(engine);
var sim = new Jecs.Simulator(engine);
  
// Instantiate a new engine
// const engine = new Engine();

// Declare a 'player' entity
const player = engine.entity('player');

// Associate the player entity to components.
// In this case we set 'position' and 'speed'.
player.setComponent('position', { x: 0, y: 0 });
player.setComponent('speed', { x: 0.5, y: 0.7 });

// Define a 'move' system for updating position of
// entities associated to components 'position' and 'speed'
engine.system('move', ['position', 'speed'], (entity, {position, speed}) => {
  position.x += speed.x;
  position.y += speed.y;
  console.log('hi', position.x, position.y)
});

// Instantiate a simulator
// If you prefer, you can avoid using simulator and start
// engine iterations manually by calling engine.tick() in a loop.
// const sim = new Simulator(engine);

// Limit the fps to 60
sim.setFps(6);

// Start simulator
sim.start();

setInterval(function() { sim.stop() }, 3000);
