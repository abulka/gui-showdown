/**
 * NestedDictAccess - wraps an object 'model' so that setting .val will
 * get or set the key specified in that object. The parameter 'keys'
 * is a list of keys, which allows drilling through sub objects/dicts 
 * during that get or set access.
 * 
 * E.g. The keys ["user", "firstname"] will access model.user.firstname
 * 
 * Reason for this class? Well, it lets you record what you want to access once
 * then generic functions can later access that attribute without knowing
 * specifically what they are accessing. I suppose its like a 
 * factory function returning a lambda, where
 * you wrap some behaviour in a function and then users of that function 
 * simply call that function, not knowing the behaviour.
 */
class NestedDictAccess {  // Reference to a shared model object
    constructor(model, keys) {
      this.model = model;  // any object/dict
      this.keys = keys;  // ['a', 'b'] would refer to model.a.b
      this.finalstr = "";
    }
  
    // dynamically access or set nested dictionary keys
  
    get val() {
      let data = this.model
      for (let k of this.keys)
        data = data[k]
      return data
    }
  
    set val(val) {
      let data = this.model
      let numkeys = this.keys.length
      let lastkey = this.keys.slice(-1)
      for (let k of this.keys.slice(0, numkeys - 1))  // for assignment drill down to *second* last key
        data = data[k]
      data[lastkey] = val
    }
}
  
// Quick test of NestedDictAccess
// (uncomment all the code below this line)
// -----------------------------------------------------

function assert(condition, message) {
  if (!condition) {
      message = message || "Assertion failed";
      if (typeof Error !== "undefined") {
          throw new Error(message);
      }
      throw message; // Fallback
  }
}
var model = {
  welcomemsg: "Welcome", 
  user: {
    firstname: "Sam", 
    surname: "Smith"
  }
}
assert(model.user.firstname == "Sam")
let m_firstname = new NestedDictAccess(model, ["user", "firstname"])
assert(m_firstname.val == "Sam")
m_firstname.val = "Mary"
assert(m_firstname.val == "Mary")
assert(model.user.firstname == "Mary")

/**
 * I suppose it could be done with a functions but have to mention the 
 * object name 'obj' each time
 */
let surname_set = (obj, val) => { obj.user.surname = val }
let surname_get = (obj) => { return obj.user.surname }
// test
assert(model.user.surname == "Smith")
assert(surname_get(model) == "Smith")
surname_set(model, "Flinstone")  // change it using the lambda
assert(model.user.surname == "Flinstone")
assert(surname_get(model) == "Flinstone")

/** 
 * I suppose it could be done with lambdas, functions which return a function locked to an obj
 */ 
let factory_model_surname_set = function (obj) { return (val)=> { obj.user.surname = val }}
let factory_model_surname_get = function (obj) { return () => { return obj.user.surname }}
// create the lambda functions
let m_surname_set = factory_model_surname_set(model)
let m_surname_get = factory_model_surname_get(model)
// test
assert(model.user.surname == "Flinstone")
assert(m_surname_get() == "Flinstone")  // lambda approach, notice we don't mention 'model' its baked in
m_surname_set("Jones")  // lambda approach, again
assert(model.user.surname == "Jones")
