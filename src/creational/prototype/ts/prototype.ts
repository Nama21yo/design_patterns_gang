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
