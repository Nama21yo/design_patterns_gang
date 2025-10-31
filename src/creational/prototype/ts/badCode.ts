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
