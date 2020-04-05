# GUI Showdown

Contains two wx python programs

| Technique  | Lines | Comment |
| -----------| ----- | ------- |
| ECS        | 344  | Gui wired via ECS (Entity Component System)
| OO         | 290  | Gui wired via OO (Object Oriented Models with Observer) 

P.S. Why is the python ESC version bigger than OO, yet the js ESC version is **smaller** than js OO!??

Contains five js programs

| Technique  | Lines | Comment |
| -----------| ----- | ------- |
| OO         | 279  | Gui wired via OO (Object Oriented Models with Observer) 
| ECS        | 228  | Gui wired via ECS (Entity Component System)
| PLAIN      | 154  | Gui wired via plain JQuery
| VUE        | 58  | Gui wired via Vue.js
| MVCA       | 383  | Gui wired via [MVCA](https://github.com/abulka/todomvc-oo) Architectura Pattern

[Live Demo](http://abulka.github.io/gui-showdown)

Counting the number of lines is approximate.  Implementation code that is a convenient extension to a library or framework is not counted.  E.g. Vue.js itself is not counted, obviously.  ECS uses Jecs library, which is not counted, nor are some extension functions I added.  OO technique uses an observer design pattern, whose short implementation code is not counted - its the least I could do to help the OO approach which came in at a whopping 300 lines.

There is an index.html launch page to get to all these implementations, as well as a debug view showing models in real time as you work with the GUI.

## Commentary

More commentary to come.

Old musings [here](musings.md)
