/*
An Implementation of the Observer design pattern for Javascript.

Subject classes should inherit from Subject and call notifyall() to broadcast, 'data' is arbitrary and optional.
Observer classes should inherit from Observer and implement notify(from, data) to receive the notification.

As a debugging aid, each notify() also emits a custom event 'observer-notification' which can be listened for e.g.
document.addEventListener("observer-notification", (event) => { ... }) where event.detail will contain { from: from,
data: data }
*/

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
    notify(from, data) {

        document.dispatchEvent(new CustomEvent("observer-notification", {  // debug functions can listen for this
            detail: { from: from, data: data }
          }));      
      
        if (from != null)
            console.log(`  Observer ${this.constructor.name} got notification from: ${from.constructor.name}, data: '${data}'`)
        else
            console.log(`Observer ${this.constructor.name} got direct call to notify(), data: '${data}'`)
    }    
}
