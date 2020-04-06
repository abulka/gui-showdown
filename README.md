# GUI Showdown

The same application, implemented in various ways - which is better, cleaner, more understandable etc? 

Like the TodoMVC "Rosetta Stone" project, but uses a different example application, and includes Python as well as Javascript implementations. 

> This project was originally intended to see if an ECS (Entity Component System), which is commonly used in building games, could be used to implement a "normal" GUI application.

## Five Javascript implementations:

[Live Demo](http://abulka.github.io/gui-showdown) of all Javascript implementations.

| Technique  | Lines | Comment |
| -----------| ----- | ------- |
| OO         | 279  | Gui wired via OO (Object Oriented Models with Observer) 
| MVCA       | 383  | Gui wired via [MVCA](https://github.com/abulka/todomvc-oo) Architectural Pattern 🆕!!
| ECS        | 228  | Gui wired via ECS (Entity Component System)
| PLAIN      | 154  | Gui wired via plain JQuery
| VUE        | 58  | Gui wired via Vue.js

## Two wxPython implementations:

| Technique  | Lines | Comment |
| -----------| ----- | ------- |
| ECS        | 344  | Gui wired via ECS (Entity Component System)
| OO         | 290  | Gui wired via OO (Object Oriented Models with Observer) 

<!-- P.S. Why is the python ESC version bigger than OO, yet the js ESC version is **smaller** than js OO!?? -->

Counting the number of lines is approximate.  Implementation code that is a convenient extension to a library or framework is not counted.  E.g. Vue.js itself is not counted, obviously.  ECS uses Jecs library, which is not counted, nor are some extension functions I added.  OO technique uses an observer design pattern, whose short implementation code is not counted - its the least I could do to help the OO approach which came in at a whopping 300 lines.

There is an index.html launch page to get to all these implementations, as well as a debug view showing models in real time as you work with the GUI.

## The Application being implemented
![The UI](https://github.com/abulka/gui-showdown/raw/master/docs/images/2019-07-17_11-41-03.gif)

### Specification

Whilst not that complex, this application has a few interesting nuances which challenge any implementation. The main nuance is that whilst the "model" can be edited and manipulated (made uppercase, set to certain phrases) the top header area displays the model according to various "display options".  Changing the display options changes how to top area appears but does not change the model.

Specifically, the behaviour we are implementing is:

Model:
- a **welcome message**, default "Welcome"
- a **user**, with a `firstname` and `surname`, default "Sam Smith"

```python
model = {"welcome_msg": "Welcome", "user": {"firstname": "Sam", "surname": "Smith"}}
```

The GUI displays:
- the welcome message twice
    - top left: pure message
    - top right: message + user
- text entry, which allows editing of the welcome message
- text entry, which allows editing of the user name and surname
- checkbox1, which toggles the model welcome message uppercase/lowercase
- checkbox2, which toggles the top right user to uppercase (not via model)
- button1, which resets the welcome message to "Hi"
- button2, which resets the user to "Fred Flinstone"

## Commentary

More commentary and evaluation of the techniques to come.

<!-- Old musings [here](musings.md) -->
