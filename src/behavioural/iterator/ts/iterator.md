### Iterator Pattern

The **Iterator Pattern** is a behavioral design pattern that provides a standard way to **traverse the elements of a collection sequentially** without exposing its underlying structure.

---

#### Why is it needed?

- Collections can be implemented using arrays, linked lists, trees, sets, maps, etc.
- Each collection may store data differently and require different traversal methods.
- Without this pattern, client code must know the details of each collection’s structure to iterate over it.
- This leads to **tightly coupled, fragile, and less maintainable code** because changing the collection type breaks client code.

---

#### What does the Iterator Pattern do?

- Introduces an **Iterator interface (or class)** with standard traversal methods like:
  - `hasNext(): boolean` — checks if there are more elements.
  - `next(): T` — retrieves the next element.
- Collections provide a method to create an iterator.
- Client code uses this iterator interface to traverse elements **independent of the underlying collection structure**.
- This pattern **decouples traversal from collection implementation**, enhancing flexibility and maintainability.

---

#### Key benefits:

- Uniform interface for traversing any collection type.
- Enables swapping collection implementations without affecting client code.
- Supports multiple traversal strategies by implementing different iterator types for the same collection.
- Promotes encapsulation by hiding the collection’s internal representation.

---

#### Summary:

The Iterator Pattern **abstracts the complexity of collection traversal**, allowing client code to treat all collections uniformly without knowing their internal data structure. It encourages clean design by **separating the traversal logic from the collection data storage**.

---

This pattern is fundamental in most programming languages and frameworks, often realized as built-in iterator constructs or interfaces (e.g. Java's `Iterator` or Python’s iterators).

[1](https://www.geeksforgeeks.org/system-design/iterator-pattern/)
[2](https://refactoring.guru/design-patterns/iterator)
[3](https://en.wikipedia.org/wiki/Iterator_pattern)
[4](https://codewitharyan.com/tech-blogs/iterator-design-pattern)
[5](https://wikidocs.net/186227)
[6](https://softwareparticles.com/design-patterns-iterator/)
[7](https://www.cs.up.ac.za/cs/lmarshall/TDP/Notes/_Chapter15_Iterator.pdf)
[8](https://plantumleditor.com/blog/patterns_iterator/)
