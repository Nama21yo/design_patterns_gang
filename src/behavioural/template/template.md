# Template Method Pattern Explained in Detail

## Intent

The **Template Method** pattern is a behavioral design pattern that defines the skeleton of an algorithm in a base (abstract) class but defers some steps of the algorithm to subclasses. This lets subclasses redefine certain steps of the algorithm without changing its overall structure.

## Problem

Imagine you have multiple classes that share a similar algorithm but differ only in parts of their process. For example, consider software that processes different file formats: both read a file, parse its content, and write some result, but the parsing and formatting steps differ.

If you write separate classes with the full process, you end up duplicating the shared structure code (like reading and writing), which is inefficient and error-prone.

## Solution

The Template Method pattern suggests that you factor out the common algorithm skeleton into an abstract base class as a **template method**. The template method calls a series of abstract or overridable methods representing the varying parts.

Subclasses implement or override these methods to provide behavior specific to the subclass, without changing the overall algorithm’s flow.

## Real-World Analogy

Making a cup of tea or coffee:

- Steps like boiling water and pouring are common (template).
- Each drink has its own way to brew or add ingredients (overridable steps).

## Structure

- **Abstract Class (Template):** Contains the template method defining the algorithm skeleton and abstract/optional steps.
- **Concrete Subclasses:** Override the abstract steps to provide particular implementations.
- The client calls the template method on concrete subclasses to execute the algorithm.

## Pseudocode Example

```typescript
abstract class DocumentProcessor {
  // Template method
  processDocument(): void {
    this.openFile();
    this.parseContent();
    this.generateReport();
    this.closeFile();
  }

  openFile(): void {
    console.log("Opening file in a generic way");
  }

  abstract parseContent(): void; // step to be supplied by subclass

  generateReport(): void {
    console.log("Generating standard report");
  }

  closeFile(): void {
    console.log("Closing file");
  }
}

class PdfProcessor extends DocumentProcessor {
  parseContent(): void {
    console.log("Parsing PDF content");
  }
}

class WordProcessor extends DocumentProcessor {
  parseContent(): void {
    console.log("Parsing Word content");
  }
}

// Usage
const pdfProcessor = new PdfProcessor();
pdfProcessor.processDocument();
// Output:
// Opening file in a generic way
// Parsing PDF content
// Generating standard report
// Closing file

const wordProcessor = new WordProcessor();
wordProcessor.processDocument();
// Output:
// Opening file in a generic way
// Parsing Word content
// Generating standard report
// Closing file
```

## When to Use

- When multiple classes have similar algorithms with variations on certain steps.
- To avoid code duplication by putting the common behavior into a base class and just overriding specific steps.
- When you want to control the invariant parts of an algorithm while letting subclasses refine certain behaviors.

## Pros and Cons

**Pros:**

- Promotes code reuse and reduces duplication.
- Ensures consistent algorithm structure.
- Easy to extend behavior by subclassing.

**Cons:**

- Sometimes subclassing can lead to deeper inheritance hierarchies.
- Subclasses tightly coupled to abstract class.
- Less flexible than composition-based patterns (e.g., Strategy).

## Summary

The Template Method pattern is an excellent way to enforce an algorithm’s structure while letting subclasses customize specific parts, leading to elegant, maintainable, and reusable code.

Would you like a TypeScript code example implementing this or a comparison to closely related patterns like Strategy or Command?

[1](https://www.codefixeshub.com/typescript/typing-the-template-method-pattern-in-typescript-p)
[2](https://www.linkedin.com/learning/typescript-design-patterns/implement-a-template-method-pattern)
[3](https://sbcode.net/typescript/template/)
[4](https://refactoring.guru/design-patterns/template-method/typescript/example)
[5](https://softwarepatterns.com/typescript/template-method-software-pattern-typescript-example)
[6](https://www.typescriptlang.org/docs/handbook/2/template-literal-types.html)
[7](https://www.youtube.com/watch?v=ZpTbpu1cT_g)
[8](https://dev.to/carlillo/design-patterns---template-method-180k)
