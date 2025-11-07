The State design pattern allows an object to alter its behavior when its internal state changes, encapsulating state-specific behaviors into separate classes and promoting cleaner, more maintainable code that avoids large conditional logic.

### Explanation

**Problem:**  
Imagine an object, like a media player or vending machine, whose behavior changes significantly depending on its internal state. For instance, a vending machine behaves differently when waiting for coin insertion, dispensing a product, or getting refilled. Without the State pattern, you'd have large conditional blocks (`if-else` or `switch`) scattered throughout the code, making it complicated and error-prone.

**Solution:**  
The State pattern extracts each distinct behavior into its own state class implementing a common interface. The main context object stores a reference to a state object, delegating behavior calls to it. By changing the current state object, the overall behavior changes effortlessly. This isolates state-specific code, adheres to open/closed principle, and simplifies adding new states.

### When to Use

- Your object has multiple states with different behavior.
- You want to avoid complex conditional logic spread across methods.
- You want to encapsulate state-specific logic into isolated classes.
- You want to support dynamic behavior changes at runtime.

### Structure

- **Context:** The main object holding a reference to a State object representing its current state.
- **State Interface:** Declares methods corresponding to behaviors that vary with state.
- **Concrete States:** Classes implementing State interface, each representing a specific state and its behavior.

### Real-world Example

A vending machine with states like NoCoin, HasCoin, Dispensing can be modeled so that the machine (‘context’) delegates actions like insertCoin, ejectCoin, pressButton to its current state object, and the state object transitions machine's current state as needed.

---

Would you like a detailed code example like the vending machine showing these concepts in action?

[1](https://www.geeksforgeeks.org/system-design/state-design-pattern/)
[2](https://java-design-patterns.com/patterns/state/)
[3](https://dotnettutorials.net/lesson/state-design-pattern/)
[4](https://www.tutorialspoint.com/design_pattern/state_pattern.htm)
[5](https://www.javacodegeeks.com/2015/09/state-design-pattern.html)
[6](https://www.baeldung.com/java-state-design-pattern)
[7](https://dev.to/mspilari/state-design-pattern-in-java-1elp)
[8](https://refactoring.guru/design-patterns/state/cpp/example)
