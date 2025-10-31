# Abstract Factory Design Pattern

## Concept

The **Abstract Factory Pattern** is a creational design pattern that provides an interface for creating **families of related or dependent objects** without specifying their concrete classes. Think of it as a "factory of factories": it lets you switch between whole sets of products or configurations easily, keeping code organized and decoupled.[1][7]

- The client uses an abstract factory, which in turn produces other factories. These factories then create products in their category.
- It’s useful when your system needs to be independent of how its objects are created, composed, or represented; especially when you need to support multiple families of related objects (for example, UI kits for Windows, Mac, Linux; or engines for different cloud providers).

## Key Components

| Component        | Role                                                                          |
| ---------------- | ----------------------------------------------------------------------------- |
| Abstract Factory | Interface defining creation methods for all families of products.             |
| Concrete Factory | Actual implementation of Abstract Factory, creates specific product families. |
| Abstract Product | Interface or abstract class for products — defines shared behaviors.          |
| Concrete Product | Implements Abstract Product — e.g. MacButton, WinButton, MacMenu.             |
| Client           | Uses the factory and products via abstract/interfaces only.                   |

## Example: UI Components for OS

Suppose you want an app that works on both Windows and Mac, with different buttons and menus for each OS.

### 1. Abstract Products

```typescript
// Abstract products
interface Button {
  paint(): void;
}
interface Menu {
  paint(): void;
}
```

### 2. Concrete Products

```typescript
// Win family
class WinButton implements Button {
  paint() {
    console.log("Painting Windows-style button");
  }
}
class WinMenu implements Menu {
  paint() {
    console.log("Painting Windows-style menu");
  }
}

// Mac family
class MacButton implements Button {
  paint() {
    console.log("Painting Mac-style button");
  }
}
class MacMenu implements Menu {
  paint() {
    console.log("Painting Mac-style menu");
  }
}
```

### 3. Abstract Factory and Concrete Factories

```typescript
// Abstract factory
interface GUIFactory {
  createButton(): Button;
  createMenu(): Menu;
}

// Concrete factories
class WinFactory implements GUIFactory {
  createButton() {
    return new WinButton();
  }
  createMenu() {
    return new WinMenu();
  }
}
class MacFactory implements GUIFactory {
  createButton() {
    return new MacButton();
  }
  createMenu() {
    return new MacMenu();
  }
}
```

### 4. Client Code

```typescript
function renderApp(factory: GUIFactory) {
  const button = factory.createButton();
  const menu = factory.createMenu();
  button.paint();
  menu.paint();
}

const factory = new WinFactory();
renderApp(factory); // Output: Windows-style components

const macFactory = new MacFactory();
renderApp(macFactory); // Output: Mac-style components
```

## Real World Use Cases

- Switching UI elements for different operating systems or themes
- Supporting multiple product families (e.g. cloud provider SDKs, database connectors, device drivers)
- Abstracting external services or APIs behind a common interface for easier swapping and expansion

## Advantages

- **Loose coupling**: the client code is not tied to concrete classes
- **Scalability**: new product families can be added with minimal changes to existing code
- **Consistency**: ensures all products from the same family are compatible with each other[7][1]

## When to Use

Use Abstract Factory when:

- Your code needs to work with multiple families of related products
- You want to switch product families at runtime
- You want to enforce compatibility between products within the same family
