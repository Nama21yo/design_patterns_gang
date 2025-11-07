# Strategy Pattern Explained

## Intent

The **Strategy** pattern is a behavioral design pattern that enables you to define a family of algorithms, encapsulate each algorithm in a separate class, and make them interchangeable at runtime. The client can choose the algorithm without changing the context in which it is used.

---

## Problem

Suppose you are building a navigation app. Users want to plan routes for driving, walking, cycling, or public transit. If you implement all route-planning logic in a single class, you end up with a huge, hard-to-maintain block of code. Every time you add or modify a routing mode, you must touch the main navigator class, risking errors and merge conflicts.

_Example problem symptoms:_

- The context (Navigator) class grows each time a new algorithm is added.
- Making changes to one algorithm can break others.
- It's hard for multiple people to work on different routing behaviors (merge conflicts).

---

## Solution

The Strategy pattern solves this by:

- Extracting each route-planning algorithm into its own class (a _strategy_).
- The main context class holds a reference to one strategy and delegates the work to it.
- The context (e.g., Navigator) is agnostic to the details of the algorithm—it only knows how to call the strategy’s generic interface.
- The client (e.g., UI) chooses and assigns the strategy at runtime, so algorithms can be swapped while running the app.
- If new strategies are needed, existing code does not break—just add a new class that implements the same interface.

---

## Real-World Analogy

Imagine trying to get to the airport. Your strategies could be “drive,” “take a bus,” or “bike.” Depending on cost, weather, or time, you can swap strategies without changing yourself—just the travel plan.

---

## Structure

- **Strategy Interface:** Declares the method that all concrete strategies must implement (e.g., `buildRoute`).
- **Concrete Strategies:** Implement specific behaviors/algorithms (like routing by car, walking, transit, etc.)
- **Context:** Holds a reference to a Strategy and delegates logic to it. Has a setter to replace the strategy.
- **Client:** Assigns a specific strategy to the context.

---

## Example (Pseudocode)

```typescript
// Strategy Interface
interface RouteStrategy {
  buildRoute(start: string, end: string): string[];
}

// Concrete Strategies
class DrivingStrategy implements RouteStrategy {
  buildRoute(start: string, end: string): string[] {
    return [`Driving from ${start} to ${end} using roads`];
  }
}

class WalkingStrategy implements RouteStrategy {
  buildRoute(start: string, end: string): string[] {
    return [`Walking from ${start} to ${end} using sidewalks`];
  }
}

class TransitStrategy implements RouteStrategy {
  buildRoute(start: string, end: string): string[] {
    return [`Transit from ${start} to ${end} using public transport`];
  }
}

// Context
class Navigator {
  private strategy: RouteStrategy;
  constructor(strategy: RouteStrategy) {
    this.strategy = strategy;
  }
  setStrategy(strategy: RouteStrategy) {
    this.strategy = strategy;
  }
  planRoute(start: string, end: string): string[] {
    return this.strategy.buildRoute(start, end);
  }
}

// Usage
const navigator = new Navigator(new DrivingStrategy());
console.log(navigator.planRoute("Central Park", "Brooklyn")); // Driving

navigator.setStrategy(new WalkingStrategy());
console.log(navigator.planRoute("Central Park", "Brooklyn")); // Walking

navigator.setStrategy(new TransitStrategy());
console.log(navigator.planRoute("Central Park", "Brooklyn")); // Transit
```

---

## When To Use

- When your class should be able to switch between different algorithms at runtime.
- When you have many similar classes, each differing in just one behavior.
- When business logic and algorithm implementation should be separated.
- When you have "conditional logic hell" (giant switch/case or if/else blocks that choose among behaviors).

---

## Pros & Cons

**Pros:**

- Algorithms can be swapped at runtime.
- New behaviors can be added without changing context.
- Improves code maintainability and teamwork (less merge conflicts).
- Follows the Open/Closed principle.
- No need for deep inheritance trees.

**Cons:**

- More classes and interfaces (can seem bulky for simple tasks).
- Clients must know about strategies and pick the right one.
- Sometimes function objects (lambdas) are sufficient if the algorithm is simple (see functional programming patterns).

---

## Summary

The **Strategy pattern** is ideal when you need to support a family of algorithms and want to cleanly allow the user or system to select or swap them at runtime without cluttering your main logic.

Would you like to try a quiz or see how this pattern relates to others (like State or Template Method)? If you want an example in another domain or language, just ask!

[1](https://refactoring.guru/design-patterns/strategy/typescript/example)
[2](https://blog.bitsrc.io/a-beautiful-design-pattern-strategy-pattern-62afe44886fc)
[3](https://dev.to/daniyarotynshin/design-pattern-strategy-ts-3e55)
[4](https://volosoft.com/blog/strategy-pattern-implementation-with-typescript-and-angular)
[5](https://codesignal.com/learn/courses/behavioral-design-patterns-3/lessons/strategy-pattern-in-typescript)
[6](https://sbcode.net/typescript/strategy/)
[7](https://stackoverflow.com/questions/60107761/how-to-correctly-implement-strategy-design-pattern)
