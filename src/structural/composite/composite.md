The **Composite pattern** is a structural design pattern that enables you to treat individual objects and compositions (groups of objects) uniformly by representing part-whole hierarchies. It is especially valuable for tree-like structures—such as file systems, UI components, or organizational charts—where both leaves (individual objects) and composites (groups/containers) must be handled the same way.[2][3][5]

---

## Key Concepts

- **Component:** Defines a common interface for both leaf and composite objects.
- **Leaf:** Represents individual objects—a basic unit with no children.
- **Composite:** Represents containers with children; it can hold and manage leaf and other composite objects, allowing the client to interact with everything via the same interface.
- **Uniformity:** You can call operations like `render`, `display`, `getSize`, or `showDetails` on both a single object (leaf) or a composite without caring about which type it is.

---

## Example: File System

Think of a directory tree:

- **File:** Is a leaf—no children, just some data.
- **Folder/Directory:** Is a composite—can contain files and/or other folders.
- You can call `.getSize()` or `.display()` on a file or directory, and a directory delegates work to its children recursively.[3][6]

---

## Benefits

- Makes client code simpler—it doesn’t need different logic for single objects vs. collections.
- Enables elegant recursive structures and operations.
- Easily extensible: new types of components can be added with minimal changes.

---

## Typical Use Cases

- Graphics editors (grouping shapes)
- Files and folders in OS
- Organization structures (employees, managers, departments)
- Nested UI components

---

## Structure Overview

```
Component
 |--- Leaf              // End nodes
 |--- Composite         // Nodes containing more Components
         |--- can have Leafs or Composites as children
```

---

## Basic Example in TypeScript

```typescript
// Component interface
interface FileSystemComponent {
  getName(): string;
  display(indent: string): void;
}

// Leaf
class File implements FileSystemComponent {
  constructor(private name: string) {}
  getName(): string {
    return this.name;
  }
  display(indent: string = ""): void {
    console.log(indent + this.name);
  }
}

// Composite
class Directory implements FileSystemComponent {
  constructor(
    private name: string,
    private children: FileSystemComponent[] = []
  ) {}
  getName(): string {
    return this.name;
  }
  add(child: FileSystemComponent): void {
    this.children.push(child);
  }
  display(indent: string = ""): void {
    console.log(indent + this.name + "/");
    this.children.forEach((child) => child.display(indent + "  "));
  }
}

// Example usage
const root = new Directory("root");
const fileA = new File("A.txt");
const fileB = new File("B.txt");
const subDir = new Directory("subfolder");

subDir.add(new File("C.txt"));
root.add(fileA);
root.add(fileB);
root.add(subDir);

root.display("");
// Output:
// root/
//   A.txt
//   B.txt
//   subfolder/
//     C.txt
```

---

The Composite pattern simplifies recursive structures and lets you build part-whole hierarchies while treating all objects as components, regardless of their complexity. Would you like a more complex example or a specialized use case?[5][2][3]

[1](https://softwarepatterns.com/typescript/composite-software-pattern-typescript-example)
[2](https://dev.to/jmalvarez/composite-pattern-in-typescript-19ij)
[3](https://cloudaffle.com/series/structural-design-patterns/composite-pattern-implementation/)
[4](https://codesignal.com/learn/courses/structural-patterns-in-typescript/lessons/composite-pattern-in-typescript)
[5](https://refactoring.guru/design-patterns/composite/typescript/example)
[6](https://sbcode.net/typescript/composite/)
[7](https://www.typescriptlang.org/tsconfig/composite.html)
[8](http://www.carloscaballero.io/understanding-the-composite-design-pattern/)
