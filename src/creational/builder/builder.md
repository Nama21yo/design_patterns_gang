The **Builder design pattern** is a creational pattern that helps construct complex objects step by step. It is especially useful when the object creation process involves several optional or mandatory parameters, and where the same construction process can build different representations.

---

## Intent

- Separate the construction of a complex object from its representation.
- Allow the same creation process to construct different products (representations).
- Simplify object creation, particularly for objects with many parameters, some of which may be optional.

---
t
## Problem

When creating complex objects (e.g., configuration objects, UI widgets, or documents), you might face long constructors with many parameters, which leads to:

- Poor readability and maintainability.
- Constructor parameter confusion (which goes where?).
- Hard to support alternative representations or versions.

For example, constructing a `Car` object with multiple optional features (color, sunroof, wheels, GPS, etc.) becomes unwieldy if you use a single constructor with many parameters.

---

## Solution

Builder pattern solves this by:

- Moving object creation logic out of the product itself.
- Creating a separate **Builder** class with methods to set each property or subsystem.
- The Builder provides a **step-by-step construction process**, enabling method chaining.
- Typically, the Builder has a `build()` method that returns the finished product.
- Supports having different Concrete Builders for alternative representations.

---

## Structure

- **Product:** The complex object being built.
- **Builder:** Abstract interface with methods for configuring the product.
- **ConcreteBuilder:** Implements Builder interface, handles the actual construction and state.
- **Director:** Optional. Encapsulates _how_ to construct the object using steps in the Builder.
- **Client:** Uses the Director and/or Builder to create the object.

---

## Example Use Case

Suppose you want to build a customizable house object with options such as windows, doors, garage, swimming pool, etc.

**Product:** House  
**Builder:** HouseBuilder interface  
**ConcreteBuilder:** ModernHouseBuilder, TraditionalHouseBuilder  
**Director:** ConstructionManager (optional)

---

## Pseudocode Example

```typescript
// Product
class House {
  windows: number = 0;
  doors: number = 0;
  hasGarage: boolean = false;
  hasSwimmingPool: boolean = false;
}

// Builder Interface
interface HouseBuilder {
  setWindows(number: number): this;
  setDoors(number: number): this;
  setGarage(hasGarage: boolean): this;
  setSwimmingPool(hasPool: boolean): this;
  build(): House;
}

// Concrete Builder
class ConcreteHouseBuilder implements HouseBuilder {
  private house: House = new House();

  setWindows(number: number): this {
    this.house.windows = number;
    return this;
  }
  setDoors(number: number): this {
    this.house.doors = number;
    return this;
  }
  setGarage(hasGarage: boolean): this {
    this.house.hasGarage = hasGarage;
    return this;
  }
  setSwimmingPool(hasPool: boolean): this {
    this.house.hasSwimmingPool = hasPool;
    return this;
  }
  build(): House {
    return this.house;
  }
}

// Usage
const builder = new ConcreteHouseBuilder();
const customHouse = builder
  .setWindows(10)
  .setDoors(2)
  .setGarage(true)
  .setSwimmingPool(false)
  .build();
// customHouse: { windows: 10, doors: 2, hasGarage: true, hasSwimmingPool: false }
```

---

## Pros & Cons

**Pros:**

- Cleaner, step-by-step construction.
- Reduces telescoping constructors.
- Supports different representations of the product.
- Increases readability and maintainability.

**Cons:**

- More classes introduced.
- May be overkill for simple objects.

---

## When to Use

- When objects require many construction steps or parameters.
- When there are variations of a product with similar construction logic.
- When you want cleaner, more maintainable object creation workflows.

Would you like to see an example with optional and mandatory parameters, method chaining, or with a director managing the building steps?

[1](https://dev.to/pratikparvati/design-pattern-builder-jcj)
[2](https://www.geeksforgeeks.org/system-design/builder-design-pattern/)
[3](https://en.wikipedia.org/wiki/Builder_pattern)
[4](https://www.scaler.com/topics/design-patterns/builder-design-pattern/)
[5](https://refactoring.guru/design-patterns/builder)
[6](https://www.cs.up.ac.za/cs/lmarshall/TDP/2014/Notes/L27_Builder.pdf)
[7](https://www.baeldung.com/java-builder-pattern)
[8](https://www.youtube.com/watch?v=iyEeXMgSPdY)
[9](https://algomaster.io/learn/lld/builder)
