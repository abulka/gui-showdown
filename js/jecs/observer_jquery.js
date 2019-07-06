// https://api.jquery.com/category/callbacks-object/

// extra node bootstrap
// var jsdom = require("jsdom");
// const { JSDOM } = jsdom;
// const { window } = new JSDOM();
// const { document } = (new JSDOM('')).window;
// global.document = document;
// var $ = jQuery = require('jquery')(window);

const jsdom = require("jsdom");
const dom = new jsdom.JSDOM(`<!DOCTYPE html>
<div id="fred"</div>
<div id="mary"</div>
</html>
`);
var $ = require("jquery")(dom.window);

// console.log($('div'))

// $.getJSON('https://api.github.com/users/nhambayi',function(data) {
//   console.log(data);
// });

// npm install jquery
// var $ = require("jquery");

var clickCallbacks = $.Callbacks();

clickCallbacks.add(function() { //one one function piece
    //parse and do something on the scope of `this`
    var c = parseInt(this.text(), 10);
    this.text(c + 1);
});
clickCallbacks.add(function(id) { //add a second non-related function piece
    //do something with the arguments that were passed
    $('span', '#last').text(id);
});

$('.click').click(function() {
    var $ele = $(this).next('div').find('[id^="clickCount"]');
    clickCallbacks.fireWith($ele, [this.id]); //do two separate but related things.
});

// console.log($)

class Person {
   constructor(name) {
       this.observers = $.Callbacks();
       this._name = name;
     }
   
     get name() {
       return this._name.toUpperCase();
     }
   
     set name(newName) {
       this._name = newName;   // validation could be checked here such as only allowing non numerical values
      //  this.observers.fireWith(this, `modified ${this._name}`)
       this.observers.fireWith(`modified ${this._name}`)
     }
}

class Watcher {
   notify0(target, data) {
       console.log(`notification from: ${target.constructor.name} data: ${data}`)
   }
   notify(data) {
       console.log(`got notification, data: ${data}`)
   }
}
p1 = new Person("Mary")
p2 = new Person("Sam")
watcher1 = new Watcher()
watcher2 = new Watcher()

// p1.subscribe(watcher1)
p1.observers.add(watcher1.notify)

p1.name = "Mary Anne"



/// another e.g.

function fn1( value ) {
   console.log( value );
 }
  
 function fn2( value ) {
   console.log( "fn2 says: " + value );
   return false;
 }
 
var callbacks = $.Callbacks();
callbacks.add( fn1 );
 
// Outputs: foo!
callbacks.fire( "foo!" );
 
callbacks.add( fn2 );
 
// Outputs: bar!, fn2 says: bar!
callbacks.fire( "bar!" );
