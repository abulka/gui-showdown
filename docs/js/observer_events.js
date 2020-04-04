/**
 * Idiomatic Javascript eventing to implement Subject/Observer pattern
 * 
 * Subjects call this function e.g. notify_all("hello")
 * Observers should be wired up with e.g. document.addEventListener("hello", (event) => { ... })
 * 
 * The attribute event.detail can be interrogated by the receiving observer function for the 'from' and 'data' information
 * The custom event generated here is broadcast to the document element, an arbitrary decision
 * 
 * @param {string} event_name name of the event
 * @param {object} from typically who is doing the notification, caller passes this in explicitly [optional]
 * @param {object or dictionary} data arbitrary info [optional]
 */
function notify_all(event_name, from, data) {
    document.dispatchEvent(new CustomEvent(event_name, { detail: {from: from, data: data } }))
    console.log(`notify all of event '${event_name}' ${from != null ? 'from: ' + from.constructor.name : from} ${data != null ? 'data: ' + data : ''}`)
  
    // debugging hook
    document.dispatchEvent(new CustomEvent("notify all called", { detail: {event_name: event_name, target: from, data: data } }))
  }
