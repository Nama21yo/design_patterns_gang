The **Singleton pattern** is a creational design pattern that ensures a class has **only one instance** across the entire application and provides a **global point of access** to that instance.

---

## Intent

- Guarantee that a class has exactly one instance.
- Prevent creation of multiple instances, intentionally restricting instantiation.
- Provide a way to access the single instance from anywhere in your codebase.

---

## Problem

Consider resources such as configuration managers, database connection pools, loggers, or other objects that must be shared to avoid duplication, resource wastage, or conflicting state. Allowing multiple instantiations can cause inconsistent state, excessive resource usage, or bugs.

For example, if an application logger can be instantiated more than once, logs may end up scattered or duplicated, making troubleshooting difficult.

---

## Solution

Singleton works by:

- Making the class’s constructor **private or protected** (not public).
- Providing a **static method** (commonly `getInstance()`) to obtain the instance. This method creates the instance if it doesn’t exist and always returns the same object otherwise.

This ensures only one instance is ever created. Any part of the program retrieves the global singleton by calling the static accessor.

---

## How It Works (Diagram)

- The client cannot use `new` to make instances.
- The static `getInstance` returns the one and only object.

---

## Real-World Analogies

- **Government**: In a country, there is only one formal government at a time—a singleton entity accessible by all citizens.
- **Print Spooler**: In operating systems, the print manager is usually a singleton to prevent conflicting jobs for the same printer.

---

## Example Use Cases

- Logger objects
- Configuration managers
- Database connection managers
- Thread pools
- Application-wide caches

---

## Implementation (Pseudocode)

**Typical Singleton skeleton in TypeScript:**

```typescript
class Singleton {
  private static instance: Singleton;

  // Private constructor prevents direct instantiation
  private constructor() {}

  // Static method to provide global access
  public static getInstance(): Singleton {
    if (!Singleton.instance) {
      Singleton.instance = new Singleton();
    }
    return Singleton.instance;
  }

  public doSomething(): void {
    console.log("Doing something with the single instance.");
  }
}

// Usage:
const s1 = Singleton.getInstance();
const s2 = Singleton.getInstance();
console.log(s1 === s2); // true: both variables refer to the same object
```

---

## Pros and Cons

**Pros:**

- Ensures a single instance; useful for shared resources.
- Easy global access.
- Lazily instantiated if needed.

**Cons:**

- Often called an “anti-pattern” if overused, can hide dependencies.
- Makes testing and refactoring harder (code becomes tightly coupled to the singleton).
- Not always thread-safe in multithreaded environments unless extra care is taken.

---

## When To Use Singleton

- Exactly one instance must be shared across the application.
- The instance holds state that must be consistent globally.

**Avoid** using Singleton if you just want global state; consider dependency injection or modular systems for better testability.

---

If you’d like to see real-world singleton code or alternative safe instantiations (such as eager vs. lazy initialization, thread safety, etc.), just ask!

[1](https://www.geeksforgeeks.org/system-design/singleton-design-pattern/)
[2](https://blog.algomaster.io/p/singleton-design-pattern)
[3](https://stackoverflow.com/questions/2475380/example-for-singleton-pattern)
[4](https://refactoring.guru/design-patterns/singleton)
[5](https://www.digitalocean.com/community/tutorials/java-singleton-design-pattern-best-practices-examples)
[6](https://www.reddit.com/r/learnprogramming/comments/raecp9/what_is_an_example_of_the_singleton_design_pattern/)
[7](https://csharpindepth.com/articles/singleton)
[8](https://itnext.io/7-ways-to-create-singleton-in-javascript-db95a75fbb76)
[9](https://www.baeldung.com/java-bill-pugh-singleton-implementation)
