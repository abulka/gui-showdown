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
  
//   // Quick test of NestedDictAccess
//   m = new NestedDictAccess(model, ["user", "firstname"])
//   assert(m.val == "Sam")
//   m.val = "Mary"
//   assert(m.val == "Mary")
  