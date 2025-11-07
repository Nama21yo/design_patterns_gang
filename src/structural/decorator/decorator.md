The **Decorator pattern** is a **structural design pattern** that allows you to **dynamically add new behaviors or responsibilities to an object at runtime** without altering the original object's class. This helps avoid subclassing, which can lead to an explosion of classes and rigid inheritance structures when you want to combine different functionalities.

---

### Why Use Decorator?

- Subclassing to add features can create many redundant classes for every combination of features (combinatorial explosion).
- You want to add or remove responsibilities to objects on the fly.
- You want to keep classes simple and focused by delegating optional features to decorators.

---

### How It Works

- The **Component** defines the interface for objects that can have responsibilities added to them.
- The **ConcreteComponent** is the original object to which new functionality can be added.
- A **Decorator** class implements the Component interface and contains a reference to a Component instance.
- One or more **ConcreteDecorators** extend the Decorator and add behavior before or after delegating to the wrapped Component.

---

### Benefits

- Provides greater flexibility than static inheritance.
- Adheres to the Single Responsibility Principle by dividing functionality between classes.
- Responsibilities can be added and removed at runtime.
- Supports mixing and matching of behaviors by stacking decorators.

---

### Example Analogy

Think of ordering a coffee and adding extras: milk, sugar, whipped cream. Instead of creating separate subclasses like `CoffeeWithMilkAndSugar`, you wrap the coffee dynamically with decorators that add these features.

---

Would you like a practical TypeScript example illustrating the Decorator pattern, such as a coffee order system?

[1](https://dev.to/jmalvarez/decorator-pattern-in-typescript-na5)
[2](https://www.convex.dev/typescript/core-concepts/object-oriented-programming/typescript-decorators)
[3](https://codesignal.com/learn/courses/structural-patterns-in-typescript/lessons/decorator-pattern-in-typescript)
[4](https://blog.bitsrc.io/decorator-design-pattern-in-typescript-701dfbf24420)
[5](https://www.typescriptlang.org/docs/handbook/decorators.html)
[6](https://refactoring.guru/design-patterns/decorator/typescript/example)
[7](https://mimo.org/glossary/typescript/decorators)
[8](https://leapcell.io/blog/understanding-and-implementing-typescript-decorators-for-enhanced-code-patterns)
[9](https://javascript.plainenglish.io/javascript-design-pattern-decorator-15-examples-25914855f1df)
