class Books {
  constructor(public title: string, public author: string) {}
}

class BookCollectionV1 {
  private books: Book[] = [];

  addBook(book: Book): void {
    this.books.push(book);
  }

  getBooks(): Book[] {
    return this.books;
  }
}

// Client code tightly coupled
const collection = new BookCollectionV1();
collection.addBook(new Books("Book A", "Author A"));
collection.addBook(new Books("Book B", "Author B"));

// Client must know how collection is structured
const books = collection.getBooks();
for (let i = 0; i < books.length; i++) {
  console.log(`${books[i].title} by ${books[i].author}`);
}

// Problem: If BookCollection changes internal data from array to Set, client code breaks since Set isn't indexed

export {};
