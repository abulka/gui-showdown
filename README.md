wx_esper
========

An attempt to use esper ECS for traditional GUI programming.

Using ECS approach to implement the MGM design pattern.
-------------------------------------------------------

Entities are the mediators, with components being things like model references, gui widget 
references. This is the data that the mediator typically needs, except its broken out as components.

The system contains the code/behaviour of the mediator, which pulls things out of the model and 
into a widget.  Currently we are cheating and have a single Render system which scans for
certain combination of components and knows what to do with them.

The checkbox and button events change the model, then in the ansence of a observer pattern,
simply trigger a world.process() to render.  A bit inefficient, but I hope to introduce a dirty flag.

Behaviour we are modelling
--------------------------

Model:
- a welcome message, default "Hi"
- a user, default "Andy", cannot change

The GUI displays:
- the welcome message twice
    - top left: pure message
    - top right: message + user
- text entry, which allows editing of the welcome message
- checkbox, which converts the welcome message uppercase/lowercase
- checkbox, which converts top right message to uppercase TODO
- button, which resets the welcome message to "Hi"
