### Behavioural Pattern

- It focus on how **objects commmunicate** and interact, managing the flow of information between entities.
- They are concerned with algorithms and the assignment of responsibilities between objects.
- Instead of simply defining the structure of classes and objects, they define their communication patterns, helping to solve common communication problems between them.
- They simplify complex control flow by defining clear commnuication and behaviour among objects.
- They provide solutions for managing **object relationships** and **communication protocols** to promote **loose coupling** and enhance flexibility.

When to use (Common Application)?

- Managing **state transitions** and **communication** efficiently

1. MEMENTO - also called **snapshot**

Memento is a behavioral design pattern that lets you save and
restore the previous state of an object without revealing the
details of its implementation.

Components:

<!--  -->

- Orginator: the object whose state needs to be saved and restored
- Memento: captures and shows the internal state of the originator
- Caretaker (the history guy): manages and stores the mementos, without modifying them.

when it used?

- Undo/Redo in Applications: in text editors, drawing applications, or any system that needs **history management**.
- State Restoration: used in scenarios where you need to periodically save system states like in games or data recovery and allow users to return to previous states.
commomly used in scenarios where you need to periodically
<!--  -->
