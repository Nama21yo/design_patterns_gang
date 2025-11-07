# Command Pattern Explained

## Intent

The **Command pattern** is a behavioral design pattern that encapsulates a request or operation as a separate object (called a "command"). This lets you parameterize clients with different requests, queue or log requests, and support features like undoable operations, all while decoupling the sender (caller) from the receiver (the object that performs the operation).[1][2][3][5][6][7]

---

## Problem

Suppose you have a system where you want to issue requests to objects (like buttons to control a remote, menu actions in a GUI, or tasks in a queue). If you hard-code each request in the sender (like having each button directly call a method on a receiver), you get tightly coupled and rigid code:

- Adding a new action requires modifying the sender's logic.
- Recording, undoing, or scheduling actions is nearly impossible.
- Senders must know the details of every receiver and operation.

**Example:**
A remote control class with methods like `onLightButtonPressed()` and `onStereoButtonPressed()` is tightly coupled to the devices. To add new devices, you have to change the remote itself, which violates Open/Closed Principle.

---

## Solution

The **Command pattern** solves this by turning each request into its own object. Each command object:

- Knows which receiver to act on.
- Knows how to invoke the receiver's operation(s).
- Can optionally store arguments, log when it was created/executed, or implement undo logic.

The sender/invoker (such as a remote control or menu item) holds a reference to a command object and simply calls `execute()`—it doesn’t care about _how_ or _what_ gets done.[2][3][5][6][7][1]

> **Decoupling:** The sender (invoker) and the receiver never talk directly. Everything flows through the command.

### Benefits:

- **Decouples sender from receiver.**
- **Flexible and extensible**: Add/remove/modify commands without touching the invoker.
- **Support for undo, queuing, and logging.**
- **Easy to record, schedule, or batch operations.**

---

## Structure (Core Participants)

1. **Command (interface/abstract):** Declares the `execute()` method.
2. **ConcreteCommand:** Implements the command interface, calls receiver(s) to carry out the operation. Often stores arguments for later use; may support `undo()`.
3. **Receiver:** The object that knows how to implement the actual business logic.
4. **Invoker:** Asks the command to carry out the request (“press button,” “select menu item”); stores and executes commands but never knows details.
5. **Client:** Creates command and receiver objects, wires up the invoker with command objects.

---

## Example: Smart Home Remote (Pseudocode)

```typescript
// 1. Command Interface
interface Command {
  execute(): void;
}

// 2. Receivers
class Light {
  on() {
    console.log("Light is ON");
  }
  off() {
    console.log("Light is OFF");
  }
}

// 3. Concrete Commands
class LightOnCommand implements Command {
  constructor(private light: Light) {}
  execute() {
    this.light.on();
  }
}
class LightOffCommand implements Command {
  constructor(private light: Light) {}
  execute() {
    this.light.off();
  }
}

// 4. Invoker
class RemoteControl {
  private slot!: Command;
  setCommand(command: Command) {
    this.slot = command;
  }
  pressButton() {
    this.slot.execute();
  }
}

// 5. Client wires it all up
const light = new Light();
const lightOn = new LightOnCommand(light);
const lightOff = new LightOffCommand(light);
const remote = new RemoteControl();
remote.setCommand(lightOn);
remote.pressButton(); // Light is ON
remote.setCommand(lightOff);
remote.pressButton(); // Light is OFF
```

You can add new commands (e.g., StereoOnCommand) **without** changing the invoker or receiver, demonstrating extensibility and decoupling.

---

## When to Use the Command Pattern

- When you need to queue, schedule, log, or undo operations.
- When you want to parameterize an object with actions to perform.
- When you want to support callbacks, transactions, or scripting.
- When senders and receivers should be decoupled and either can evolve independently.
- GUI frameworks (buttons, menus), macro recording, job queues, remote controls, distributed systems—all are classic use cases.

---

## Pros & Cons

**Pros:**

- **Decouples** invoker and receiver.
- Store and log operations for undo.
- Supports macros (composite commands) and transactions.
- New commands can be added without changing clients or the invoker.

**Cons:**

- May add extra classes (can be verbose for small/simple uses).

---

## Summary

The **Command pattern** encapsulates a request as an object, letting you parameterize clients with requests, queue or log them, support undo, and decouple invokers from receivers. It's a critical tool in building extensible, modular, and flexible software architectures and is widely used in GUIs, job queues, and transactional systems.

Would you like a quiz or a custom code example next?

[1](https://refactoring.guru/design-patterns/command)
[2](https://www.geeksforgeeks.org/system-design/command-pattern/)
[3](https://en.wikipedia.org/wiki/Command_pattern)
[4](https://gameprogrammingpatterns.com/command.html)
[5](https://www.syncfusion.com/blogs/post/command-design-pattern-tutorial-with-csharp-examples)
[6](https://sourcemaking.com/design_patterns/command)
[7](https://dev.to/aakas/mastering-the-command-design-pattern-in-python-18o3)
[8](https://www.digitalocean.com/community/tutorials/command-design-pattern)
[9](https://www.youtube.com/watch?v=GQzfF5EMD7o)
