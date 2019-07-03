model = {"welcome_msg": "Welcome", "user": {"name": "Sam", "surname": "Smith"}}

const world = new Ecs();

class ModelRef {  // Mediator (entity + this component) needs to know about model. Model specific
  constructor(model, key) {
    this.model = model;
    this.key = key;
    this.finalstr = "";
  }
}
class ComponentModelWelcome extends ModelRef {}
class ComponentModelFirstname extends ModelRef {}
class ComponentModelSurname extends ModelRef {}

class GuiControlRef {  // Mediator (entity + this component) needs to know about a wxPython gui control
  constructor(ref) {
    this.ref = ref
  }
}
class ComponentGuiDiv extends GuiControlRef {}
class ComponentGuiInput extends GuiControlRef {}

const entity_welcome_left = world.entity('entity_welcome_left')
entity_welcome_left.setComponent('c_welcome', new ComponentModelWelcome(model, 'welcome_msg'))
entity_welcome_left.setComponent('c_gui_div', new ComponentGuiDiv('welcome'))  // id of div to hold welcome message, top left

const entity_welcome_user_right = world.entity('entity_welcome_user_right')
entity_welcome_user_right.setComponent('c_welcome', { model: model, key: 'welcome_msg' });
entity_welcome_user_right.setComponent('c_firstname', new ComponentModelFirstname(model["user"], 'name'));
entity_welcome_user_right.setComponent('c_surname', new ComponentModelSurname(model["user"], 'surname'));
entity_welcome_user_right.setComponent('c_gui_div', new ComponentGuiDiv('welcome-user'));  // id of div to hold welcome + user message, top right

const entity_edit_welcome_msg = world.entity('entity_edit_welcome_msg')
entity_edit_welcome_msg.setComponent('c_welcome', { model: model, key: 'welcome_msg' });
entity_edit_welcome_msg.setComponent('ComponentGuiInput', { ref: 'welcome' });  // name (not id) of input to hold welcome message

const entity_edit_user_name_msg = world.entity('entity_edit_user_name_msg')
entity_edit_user_name_msg.setComponent('c_firstname', new ComponentModelFirstname(model["user"], 'name'));
entity_edit_user_name_msg.setComponent('ComponentGuiInput', { ref: 'firstname' });  // name (not id) of input to hold first name

const entity_edit_user_surname_msg = world.entity('entity_edit_user_surname_msg')
entity_edit_user_surname_msg.setComponent('c_surname', new ComponentModelSurname(model["user"], 'surname'));
entity_edit_user_surname_msg.setComponent('ComponentGuiInput', { ref: 'surname' });  // name (not id) of input to hold first name


// ComponentModelFirstname
// ComponentModelSurname
// ComponentGuiInput
// $('input[name=welcome]')

// console.log(`entity_welcome_left has ComponentModelWelcome? ${entity_welcome_left.hasComponent('ComponentModelWelcome')}`)

// const fred = world.entity('fred')
// fred.setComponent('mary_jane', { x: 0, y: 0 });

// // Declare a 'player' entity
// const player = world.entity('player');
// // Associate the player entity to components.
// // In this case we set 'position' and 'speed'.
// player.setComponent('position', { x: 0, y: 0 });
// player.setComponent('speed', { x: 0.5, y: 0.7 });
// // Define a 'move' system for updating position of
// // entities associated to components 'position' and 'speed'
// world.system('move', ['position', 'speed'], (entity, {position, speed}) => {
//   position.x += speed.x;
//   position.y += speed.y;
//   $('#log').html(`x=${position.x} <br>y=${position.y}<br>entity=${entity}`)
//   console.log(`move: entity ${entity} has component position ${position} component speed ${speed}`)
// });

// AHA - the variables receiving the component must be named exactly the same as the component name

// world.system('DebugSystem1', ['ComponentModelWelcome'], (entity, {ComponentModelWelcome,}) => {
//   console.log(`DebugSystem1 - ComponentModelWelcome: entity ${entity} has component ${ComponentModelWelcome}`)
// });

// world.system('DebugSystem2', ['position'], (entity, {position,}) => {
//   console.log(`DebugSystem2 - position: entity ${entity} has component ${position}`)
// });

// world.system('DebugSystem3', ['mary_jane'], (entity, {mary_jane,}) => {
//   console.log(`DebugSystem3 - mary: entity ${entity} has component ${mary_jane}`)
// });

world.system('RenderProcessor', ['c_welcome', 'c_gui_div'], (entity, {c_welcome, c_gui_div}) => {
  // console.log("render textctrl for component", ComponentModelWelcome, "component", ComponentGuiDiv, "entity is", entity)
  let msg = c_welcome.model[c_welcome.key]
  $('#' + c_gui_div.ref).html(msg)
});

world.system('RenderProcessor2', ['c_welcome', 'c_firstname', 'c_surname', 'c_gui_div'], (entity, {c_welcome, c_firstname, c_surname, c_gui_div}) => {
  console.log("top right", entity)
  let welcome = c_welcome.model[c_welcome.key]
  let firstname = c_firstname.model[c_firstname.key]
  let surname = c_surname.model[c_surname.key]
  let msg = `${welcome} ${firstname} ${surname}`  // need surname, need model extract processor stage first
  $('#' + c_gui_div.ref).html(msg)
});

world.system('RenderProcessor3', ['c_welcome', 'ComponentGuiInput'], (entity, {c_welcome, ComponentGuiInput}) => {
  console.log("welcome text input", entity)
  let welcome = c_welcome.model[c_welcome.key]
  $(`input[name=${ComponentGuiInput.ref}]`).val(welcome)
});

world.system('RenderProcessor4', ['c_firstname', 'ComponentGuiInput'], (entity, {c_firstname, ComponentGuiInput}) => {
  console.log("firstname text input", entity)
  let firstname = c_firstname.model[c_firstname.key]
  $(`input[name=${ComponentGuiInput.ref}]`).val(firstname)
});

world.system('RenderProcessor5', ['c_surname', 'ComponentGuiInput'], (entity, {c_surname, ComponentGuiInput}) => {
  console.log("surname text input", entity)
  let surname = c_surname.model[c_surname.key]
  $(`input[name=${ComponentGuiInput.ref}]`).val(surname)
});

function model_setter_welcome(msg) {
    model["welcome_msg"] = msg
    model_welcome_toggle()
}

function model_welcome_toggle() {
  model["welcome_msg"] = $('input[name=check1]').prop('checked') ? model["welcome_msg"].toUpperCase() : model["welcome_msg"].toLowerCase()
  world.tick()
}

$('#reset-welcome').on('click', function(e) {
  model_setter_welcome("Hello")  // so that welcome uppercase toggle is respected
})

$('#reset-user').on('click', function(e) {
  console.log('eee')
})

world.tick()

// // Instantiate a simulator
// // If you prefer, you can avoid using simulator and start
// // engine iterations manually by calling ecs.tick() in a loop.
// const sim = new Ecs.Simulator(ecs);
 
// // Limit the fps to 60
// // sim.setFps(60);
// sim.setFps(6);
 
// // Start simulator
// sim.start();

// console.log("sim", sim)


// var game = (function () {
//   // 'Screen' <div>
//   var screen = document.getElementById('screen');

//   // Logging <div>
//   var logarea = document.getElementById('log');

//   // Instantiating engine, timer and simulator
//   var ecs = new Ecs();
//   var timer = new Ecs.Timer(ecs);
//   var sim = new Ecs.Simulator(ecs);
  
//   // Possible move direction
//   var up = { x: 0, y: -1 };
//   var down = { x: 0, y: 1 };
//   var left = { x: -1, y: 0 };
//   var right = { x: 1, y: 0 };
//   var stop = { x: 0, y: 0 };

//   // Map cell types
//   var empty = 0;
//   var wall = 1;
//   var food = 2;

//   // Map size
//   var mapw = 50;
//   var maph = 10;

//   // Map cell array
//   var map = [];

//   // Calculate initial players energy and food energy
//   var initialEnergy = mapw * maph;
//   var foodEnergy = Math.floor(Math.sqrt(initialEnergy));

//   // Entities
//   var knight;
//   var ogre;
//   var fps;
  
//   // Position components (will be associated to entities)
//   var knightPosition = {};
//   var ogrePosition = {};

//   // FPS component used to calculate
//   var fpsData = {
//     sum: 0,           // Sum of calculated instant fps
//     sumStartTime: 0,  // fps summing start time
//     count: 0,         // Number of fps summed
//     avg: 0            // Frames Per Second calculated over one second
//   };

//   // Append a line of log
//   function log(text) {
//     var html = logarea.innerHTML;
//     html += (text || '') + '<br/>';
//     logarea.innerHTML = html;

//     // Scroll log to bottom
//     logarea.scrollTop = logarea.scrollHeight;
//   }

//   // Initialize map
//   function initMap() {
//     var x,
//       y,
//       rnd,
//       cellType;
//     var totalFood,
//       totalInnerWalls;

//     log('Initializing world map...');

//     map = [];
//     for (y = 0; y < maph; y += 1) {
//       for (x = 0; x < mapw; x += 1) {
//         cellType = empty;
//         if (x === 0 || y === 0 || x === mapw - 1 || y === maph - 1) {
//           // Wall on boundaries
//           cellType = wall;
//         } else {
//           rnd = Math.random();
//           if (rnd > 0.7) cellType = food;
//           else if (rnd > 0.6) cellType = wall;
//         }
//         map.push(cellType);
//       }
//     }
//   }

//   // Initializes map and components
//   function init() {
//     // reset timer
//     timer.reset();
    
//     // Reset FPS component
//     fpsData.sum = 0;
//     fpsData.sumStartTime = 0;
//     fpsData.count = 0;
//     fpsData.avg = 0
//     fps.setComponent('fps', fpsData);
    
//     // Init knight components
//     knightPosition.x = 1 + parseInt(Math.floor(Math.random() * (mapw - 2)), 10);
//     knightPosition.y = 1 + parseInt(Math.floor(Math.random() * (maph - 2)), 10);
//     knight.setComponent('position', knightPosition);
//     knight.setComponent('direction', {x: 0, y: 0});
//     knight.setComponent('energy', initialEnergy);

//     // Init ogre components
//     ogrePosition.x = 1 + parseInt(Math.floor(Math.random() * (mapw - 2)), 10);
//     ogrePosition.y = 1 + parseInt(Math.floor(Math.random() * (maph - 2)), 10);
//     ogre.setComponent('position', ogrePosition);
//     ogre.setComponent('direction', {x: 0, y: 0});
//     ogre.setComponent('energy', initialEnergy);

//     // Init world map
//     initMap();
//   }

//   // Set a value on the map
//   function mapSet(x, y, v) {
//     map[(mapw * y) + x] = v;
//   }

//   // Get a value from the map
//   function mapGet(x, y) {
//     return map[(mapw * y) + x];
//   }

//   log('Setup entities...');
//   fps = ecs.entity('fps');
//   knight = ecs.entity('knight');
//   ogre = ecs.entity('ogre');

//   // A system for calculating FPS
//   ecs.system('fps-updater', ['fps'], function(entity, components) {
//     var time = timer.getTime();
//     var fpsData = components.fps;

//     // Calculate average FPS over one second
//     if(time.delta > 0) {
//       var fps = 1000 / time.delta;
//       if(fpsData.sumStartTime === 0) fpsData.sumStartTime = time.now;
//       fpsData.sum += fps;
//       fpsData.count++;
//       if(time.now - fpsData.sumStartTime > 1000) {
//         fpsData.avg = fpsData.sum / fpsData.count;
//         fpsData.sumStartTime = time.now;
//         fpsData.sum = fps;
//         fpsData.count = 1;
//       }
//     }
//   });

//   // Think system
//   log('Setup think system...');
//   ecs.system('think', ['position', 'direction'], function(entity, components) {
//     var x = components.position.x;
//     var y = components.position.y;
//     var direction = components.direction;
//     var newDirection = stop;
    
//     // Next position if not changing direction
//     var nx = x + direction.x;
//     var ny = y + direction.y;

//     // Directions to food or empty cells
//     var foodCellDirections = [];
//     var emptyCellDirections = [];

//     // Surrounding cell types
//     var upType;
//     var rightType;
//     var downType;
//     var leftType;

//     // If next cell is a food cell then don't change direction
//     if(mapGet(nx, ny) === food) return;

//     upType = mapGet(x, y - 1);
//     rightType = mapGet(x + 1, y);
//     downType = mapGet(x, y + 1);
//     leftType = mapGet(x - 1, y);

//     // First looks for food cells
//     if(upType === food) foodCellDirections.push(up);
//     if(rightType === food) foodCellDirections.push(right);
//     if(downType === food) foodCellDirections.push(down);
//     if(leftType === food) foodCellDirections.push(left);

//     // If there's at least a food cell near, then move randomly to one of them
//     if(foodCellDirections.length > 0) {
//       newDirection = foodCellDirections[Math.floor(Math.random() * foodCellDirections.length)];
//       direction.x = newDirection.x;
//       direction.y = newDirection.y;
//       return;
//     }

//     // No food cells.
//     // If moving and next cell is an empty cell then don't change direction 90% of times.
//     // Randomness limits stuck situations.
//     if(!_.isEqual(direction, stop) && mapGet(nx, ny) === empty) {
//       if(Math.random() < 0.90) return;
//     }

//     // Looks for empty cells
//     if(upType === empty) emptyCellDirections.push(up);
//     if(rightType === empty) emptyCellDirections.push(right);
//     if(downType === empty) emptyCellDirections.push(down);
//     if(leftType === empty) emptyCellDirections.push(left);

//     // If there's at least an empty cell near, then move randomly to one of them
//     if(emptyCellDirections.length > 0) {
//       newDirection = emptyCellDirections[Math.floor(Math.random() * emptyCellDirections.length)];
//     }

//     direction.x = newDirection.x;
//     direction.y = newDirection.y;
//   });

//   // Move system
//   log('Setup move system...');
//   ecs.system('move', ['position', 'direction', 'energy'], function(entity, components) {
//     var position = components.position;
//     var direction = components.direction;
//     var energy = components.energy;

//     if (energy === 0) {
//       // Dead
//       sim.stop();
//       log(entity.name + ' is dead, game is over!');
//       return;
//     }

//     entity.components.energy -= 1;
//     position.x += direction.x;
//     position.y += direction.y;
//   });

//   log('Setup eat system...');
//   ecs.system('eat', ['position', 'energy'], function(entity, components) {
//     var x = components.position.x;
//     var y = components.position.y;

//     if (mapGet(x, y) === food) {
//       mapSet(x, y, empty);
//       entity.components.energy += foodEnergy;
//       log(entity.name + ' eats food and raise his energy to ' + entity.components.energy);
//     }
//   });

//   // Draw to 'screen'
//   function draw() {
//     var buffer = '';
//     var x,
//       y,
//       i,
//       row,
//       cell;

//     buffer += 'Knight (' + knight.components.position.x + ',' + knight.components.position.y + ') energy: ' + knight.components.energy + '<br/>';
//     buffer += 'Ogre (' + ogre.components.position.x + ',' + ogre.components.position.y + ') energy: ' + ogre.components.energy + '<br/>';

//     i = 0;
//     for (y = 0; y < maph; y += 1) {
//       row = '';
//       for (x = 0; x < mapw; x += 1, i += 1) {
//         cell = map[i];
//         if (knightPosition.x === x && knightPosition.y === y) row += 'O';
//         else if (ogrePosition.x === x && ogrePosition.y === y) row += 'X';
//         else if (cell === wall) row += '#';
//         else if (cell === food) row += '.';
//         else row += '&nbsp;';
//       }
//       buffer += row + '<br/>';
//     }

//     var time = timer.getTime();
//     buffer += '<br/>';
//     buffer += 'FPS: ' + fpsData.avg.toFixed(2) + '<br/>';
//     buffer += time.total + ' milliseconds total.';
//     screen.innerHTML = buffer;
//   }

//   // Redraw map each tick
//   ecs.on('tick-after', draw);

//   // Init map and components
//   init();

//   // Initial draw
//   draw();

//   return {
//     simulator: sim,
//     reset: function() {
//       init();
//       draw();
//     },
//   };
// }());


