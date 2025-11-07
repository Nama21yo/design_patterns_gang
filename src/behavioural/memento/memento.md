# Memento Pattern: Problem and Solution

## The Problem

Imagine you're building a text editor. Besides editing text, users expect common features like **undo**. A naive approach to implement this is to save the entire state of the editor before every change. To do this, you'd need to:

- Make copies of all relevant fields (like text content, cursor position, formatting, etc.).
- Store these snapshots somewhere (like a list or stack) so you can roll back to a previous state whenever the user requests an undo.

**What's the challenge?**

1. **Encapsulation Breaks:** Many objects keep their internal state private. If you copy an object's state from outside, you might need to expose private data, making the class less robust and more error-prone in the face of change.
2. **Maintenance Issues:** If you refactor your objects (add/remove fields), you'd need to update the code that makes copies everywhere. This is brittle and hard to maintain.
3. **Security:** If snapshot objects are public or expose internal state, any code can inspect or modify private data, violating encapsulation and introducing potential bugs.

## The Solution: The Memento Pattern

The **Memento** pattern solves these problems by delegating responsibility for making and restoring state snapshots to the _object itself_.

- **Originator**: The object whose state we want to save or restore. It creates a special snapshot object (the **Memento**) containing its own private data.
- **Memento**: Holds a snapshot of the Originator's state. It is usually immutable and only accessible by the Originator.
- **Caretaker**: Stores Mementos and uses them to restore state when required—but cannot access or modify the Mementos' inner data.

This way, you can:

- Save the Originator's state via a Memento **without exposing or breaking encapsulation**.
- Keep the Memento’s structure private and internal to the Originator;
  the Caretaker never needs to know or depend on the Originator’s internals.
- Refactor your originators without having to change the Caretaker or code that handles undo/redo functionality.[1][2][5]

## How It Works: Visual Overview

1. **Saving state**: The Caretaker asks the Originator for a Memento—`createMemento()`. The Originator returns a snapshot of its state, packaged up (privately!) in a Memento object.
2. **Undoing**: When the user triggers "undo," the Caretaker gives the most recent Memento back to the Originator, which reads out its data and restores its state—all from within itself, keeping private fields truly private.

## Sample Structure (Pseudocode)

```python
class Editor:  # originator
    def __init__(self):
        self._text = ''
        self._cursor = 0
    def set_text(self, text):
        self._text = text
    def create_memento(self):
        return self._Memento(self._text, self._cursor)
    def restore(self, memento):
        self._text = memento.text
        self._cursor = memento.cursor
    class _Memento:
        def __init__(self, text, cursor):
            self.text = text
            self.cursor = cursor

class History:  # caretaker
    def __init__(self):
        self._stack = []
    def save(self, memento):
        self._stack.append(memento)
    def undo(self):
        return self._stack.pop() if self._stack else None
```

In this example:

- `Editor` is the Originator and manages its own snapshots.
- `_Memento` is an inner class that only `Editor` can access.
- `History` is the Caretaker: it stores but **cannot modify or inspect** mementos.

## Key Points Recap

- **Encapsulation preserved:** Only the Originator accesses the Memento's contents.
- **Easy undo/redo:** Caretaker manages history without knowing details.
- **Adaptable:** If the Originator changes, only its code updates—no need to modify Caretaker or Memento interfaces.[5][2]

## When to Use the Memento Pattern

- When you need to implement undo/redo features.
- When you want to make backups or rollback mechanisms without exposing internal state.
- When changes to object internals shouldn't ripple out to external classes—preserve encapsulation![1][2][5]

Would you like to see a full real-world example in code, or discuss some pros/cons of this approach next?

---

If you want this tailored for a specific language or interview setting, let me know!

[1](https://www.geeksforgeeks.org/system-design/memento-design-pattern/)
[2](https://refactoring.guru/design-patterns/memento)
[3](https://www.baeldung.com/java-memento-design-pattern)
[4](https://algomaster.io/learn/lld/memento)
[5](https://reactiveprogramming.io/blog/en/design-patterns/memento)
[6](https://dotnettutorials.net/lesson/memento-design-pattern/)
[7](https://blog.postsharp.net/memento)
[8](https://www.tutorialspoint.com/design_pattern/memento_pattern.htm)
