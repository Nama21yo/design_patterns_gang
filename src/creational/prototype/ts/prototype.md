# Prototype Design Pattern Explained

The **Prototype Design Pattern** is a creational pattern that lets you create new objects by _cloning_ existing instances (prototypes), rather than always instantiating fresh objects from scratch. This is especially valuable when:

- Object creation is expensive (due to resource usage or complex initialization).
- You want to build objects with similar properties but minor variations.
- Object structure or concrete classes are determined at runtime, or need to be decoupled from client code.[1][2][6]

## Key Components

- **Prototype Interface**: Declares a method (commonly `clone()`) for copying objects.
- **Concrete Prototype**: Implements cloning logic specific to the object.
- **Client**: Requests clones from existing prototypes, possibly modifying the copies as needed.

---

## Bad Code (Direct Instantiation and Duplication)

Suppose you have a `Document` class and want many similar documents with only minor changes:

```typescript
class Document {
  constructor(
    public title: string,
    public content: string,
    public author: string
  ) {}
}

// Client code creates similar objects manually
const doc1 = new Document(
  "Design Doc",
  "Prototype pattern details...",
  "Alice"
);
const doc2 = new Document(
  doc1.title,
  doc1.content,
  "Bob" // only author differs
);

// Later, if you want to add more properties or logic for duplication, you must update every location that copies
```

### Problems:

- **Error-prone, hard to maintain**—if properties change, you must update all instantiations.
- **Tight coupling**—client needs to know all properties/details for copying.
- **No polymorphic copying**—can't easily clone subclasses without more logic.

---

## Refactored: Prototype Design Pattern

You solve these issues by letting your domain objects support cloning.

```typescript
// Prototype Interface
interface Prototype<T> {
  clone(): T;
}

// Concrete Prototype
class Document implements Prototype<Document> {
  constructor(
    public title: string,
    public content: string,
    public author: string
  ) {}
  clone(): Document {
    // Simple shallow clone (for deep properties, make deep copies!)
    return new Document(this.title, this.content, this.author);
  }
}

// Usage in Client
const doc1 = new Document(
  "Design Doc",
  "Prototype pattern details...",
  "Alice"
);
// Make a variant via cloning, then modifying
const doc2 = doc1.clone();
doc2.author = "Bob"; // Only change what is needed

console.log(doc1); // Document { title: 'Design Doc', content: ..., author: 'Alice' }
console.log(doc2); // Document { title: 'Design Doc', content: ..., author: 'Bob' }
```

### Benefits:

- **Single clone method**: Easily add properties and keep copy logic in one place.
- **Easy variants**: Clone and mutate only needed fields.
- **Polymorphic cloning**: You can work with lists of prototypes and clone them without knowing their exact class.
- **Decoupling**: Client code doesn’t need to know details of construction.

---

## Real-World Scenario

- **Document Templates**: Users create documents based on predefined templates (prototypes). To make a new variation, clone a prototype and tweak certain fields.
- **Game Development**: Clone complex pre-configured characters or terrain for quick instantiation at runtime.[2][1]

---

## When to Use Prototype Pattern

- When object creation is costly or complex.
- When creating objects based on runtime-determined types.
- When you need many similar objects with small differences.

---

## Quick Comparison Table

| Aspect      | Bad Code (Manual Copy) | Prototype Pattern              |
| ----------- | ---------------------- | ------------------------------ |
| Duplication | In many places         | In one clone method            |
| Flexibility | Low                    | High (runtime, polymorphic)    |
| Maintenance | Tedious, error-prone   | Simple, centralized            |
| Performance | Can be inefficient     | Can optimize via smart cloning |

The Prototype Design Pattern is frequently used in systems where variation and performance matter. By delegating cloning responsibility to the objects themselves, you gain clean, flexible, and efficient object creation.
