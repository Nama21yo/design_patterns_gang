### Behavioural Pattern

- It focus on how **objects commmunicate** and interact, managing the flow of information between entities.
- They are concerned with algorithms and the assignment of responsibilities between objects.
- Instead of simply defining the structure of classes and objects, they define their communication patterns, helping to solve common communication problems between them.
- They simplify complex control flow by defining clear commnuication and behaviour among objects.
- They provide solutions for managing **object relationships** and **communication protocols** to promote **loose coupling** and enhance flexibility.

When to use (Common Application)?

- Managing **state transitions** and **communication** efficiently

1. MEMENTO - also called **snapshot**

Problem - How to provide undo/redo functionality without exposing the object's internal state or breaking encapsulation?

Memento is a behavioral design pattern that lets you save and
restore the previous state of an object without revealing the
details of its implementation.

The main idea is to capture a snapshot of an object's state at a certain moment and store it separately so that the object can return to that state later if needed. This is especially useful for implementing features like undo/redo, rollback, or version history in applications such as text editors, games, and CAD tools.
Components:

<!--  -->

- Orginator: the object whose state needs to be saved and restored. The object whose state needs to be saved or restored. It creates and uses Memento objects to store its state
- Memento: captures and shows the internal state of the originator. A small object that stores the internal state of the Originator. It’s usually immutable and provides limited access to ensure encapsulation isn’t broken 
- Caretaker (the history guy): manages and stores the mementos, without modifying them. Manages storage and retrieval of Memento objects. It doesn’t modify them but serves as a middleman between the Originator and stored states (like a history manager) 

Implementation Concept
1. The Originator class creates a Memento containing a copy of its current state.

2. The Caretaker stores this Memento (in a list or stack, for history management).

3. When the user wants to revert, the Caretaker passes the stored Memento back to the Originator.

4. The Originator restores its state from that Memento.


when it used?

- Undo/Redo in Applications: in text editors, drawing applications, or any system that needs **history management**.
- State Restoration: used in scenarios where you need to periodically save system states like in games or data recovery and allow users to return to previous states.
commomly used in scenarios where you need to periodically
<!--  -->
