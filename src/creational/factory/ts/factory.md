# Factory Design Pattern — Detailed Explanation

## What Is the Factory Design Pattern?

The **Factory Design Pattern** is a **creational** pattern that provides a way to create objects **without specifying their concrete classes** in client code. In other words, you delegate object creation to a factory method or class, which abstracts away the details of which subclass actually gets instantiated.[1][2][4][5][6]

### Key Goals

- **Decouple object creation** from usage
- Provide **flexibility** to add new types (products) without changing client code
- Centralize and organize complex construction logic

---

## How Does the Factory Pattern Work?

1. **Define a common interface or abstract class** for products (e.g., `Car`, `Chair`, `Computer`).
2. **Implement concrete product classes** that follow the product interface (e.g., `Tesla`, `Mercedes`).
3. **Implement a Factory class or method** responsible for creating instances based on input (like a type or config).
4. **Client code** uses the factory, so it never directly instantiates concrete product classes.[2][4][5]

---

## Real-World Example: Car Factory (TypeScript)

Let's say you want to create various car classes, but the client code should remain unaware of the specific classes used.

```typescript
// 1. Product Interface
interface Car {
  model: string;
  drive(): void;
}

// 2. Concrete Products
class Tesla implements Car {
  model = "Tesla Model S";
  drive() {
    console.log(`You are driving a ${this.model}`);
  }
}

class Mercedes implements Car {
  model = "Mercedes-Benz C-Class";
  drive() {
    console.log(`You are driving a ${this.model}`);
  }
}

// 3. Factory Class
class CarFactory {
  createCar(type: string): Car {
    switch (type) {
      case "Tesla":
        return new Tesla();
      case "Mercedes":
        return new Mercedes();
      default:
        throw new Error("Unknown car type");
    }
  }
}

// 4. Client Usage Example
const factory = new CarFactory();
const tesla = factory.createCar("Tesla");
tesla.drive(); // Output: You are driving a Tesla Model S
const mercedes = factory.createCar("Mercedes");
mercedes.drive(); // Output: You are driving a Mercedes-Benz C-Class
```

---

## Why Use the Factory Pattern?

- **Encapsulation:** Keeps creation logic separate from usage, making code easier to maintain and update.[4]
- **Extensibility:** New product types can be added just by extending the factory, not by changing client code.[5][1][2]
- **Single Responsibility:** Centralizes how objects are created, so changes only need to be made in the factory.

---

## More Real-World Application Ideas

- **UI Components:** Creating different widgets (buttons, text fields) via a widget factory.
- **Database Connections:** DB connection factory decides which connection object (MySQL, PostgreSQL) to return based on configuration.
- **Game Development:** Factory method to spawn different enemy types or weapons.
- **Banking App:** Using a factory to create different bank account types (savings, business) depending on user choice.[8]
- **Furniture Store:** `ChairFactory` returns different chairs depending on style or size ([SmallChair], [MediumChair], [BigChair]).[4]

---

## Key Takeaways

- The Factory Pattern helps you build flexible and scalable systems by hiding the details of object creation.
- Client code depends on interfaces rather than specific classes, making it easier to add or change products.
- Use the Factory Pattern whenever you need to manage the creation of objects with complex initialization, or when future types may need to be added without rewriting major parts of your code.
