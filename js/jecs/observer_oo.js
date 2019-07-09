// https://medium.com/@majdasab/observer-pattern-with-javascript-es6-classes-2a19851e1506

class Subject {
    constructor() {
        this.observers = []
    }

    subscribe(observer) {
        this.observers.push(observer)
    }
    add_observer(observer) {  // psudonym for subscribe
        this.subscribe(observer)
    }

    unsubscribe(observer) {
        let index = this.observers.indexOf(observer)
        if (index > -1)
            this.observers.slice(index, 1)
    }

    notifyall(data) {
        const self = this
        for (let o of this.observers) {
            console.log(`Subject ${this.constructor.name} notifying: ${o.constructor.name}`)
            o.notify(self, data)
        }
    }
}

class Observer {
    notify(target, data) {
        if (this.constructor.name == 'MediatorDumpModels')  // reduce debug noise
            return 

        if (target != null)
            console.log(`  Observer ${this.constructor.name} got notification from: ${target.constructor.name}, data: '${data}'`)
        else
            console.log(`Observer ${this.constructor.name} got direct call to notify(), data: '${data}'`)
    }    
}


// TEST

/*
class Person extends Subject {
    constructor(name) {
        super();
        this._name = name;
      }
    
      get name() {
        return this._name.toUpperCase();
      }
    
      set name(newName) {
        this._name = newName;   // validation could be checked here such as only allowing non numerical values
        this.notifyall(`modified ${this._name}`)
      }
}

class Watcher {
    notify(target, data) {
        console.log(`notification from: ${target.constructor.name} data: ${data}`)
    }
}
p1 = new Person("Mary")
p2 = new Person("Sam")
watcher1 = new Watcher()
watcher2 = new Watcher()
p1.subscribe(watcher1)
p1.name = "Mary Anne"

*/



// SCRAPS


/*
var settings = {
    fonts: "medium",
    colors: "light",
    observers: [],
    addObserver: function (observer) {
       this.observers.push(observer);
    },
    update : function(newSettings) {
       for (k in newSettings)
           this[k] = newSettings[k];
       this.fire();
    },
    fire: function() {
       var self = this;
       observers.forEach(function() { this.update(self); });
    }
  }
*/

/*
https://stackoverflow.com/questions/25417547/observer-pattern-vs-mediator-pattern

where each view would behave somewhat like this:

var view = {
   init: function() {
      //... attach to DOM elements etc...
      settings.addObserver(this); 
   },
   update: function(settings) {
      //... use settings to toggle classes for fonts and colors...
   } 
}

*/

