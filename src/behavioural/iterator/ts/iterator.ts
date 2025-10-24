interface BookIteratorInterface<T> {
  hasNext(): boolean;
  next(): T;
}

class Book {
  constructor(public title: string, public author: string) {}
}

class BookCollectionV2 {
  private books: Set<Book> = new Set();

  addBook(book: Book): void {
    this.books.add(book);
  }

//   create a nested class
  private BookIterator = class implements BookIteratorInterface<Book> {
    private position = 0;
    private booksArray: Book[];

    constructor(books: Set<Book>) {
      this.booksArray = Array.from(books);
    }

    hasNext(): boolean {
      return this.position < this.booksArray.length;
    }

    next(): Book {
      if (!this.hasNext()) {
        throw new Error("No more books");
      }
      return this.booksArray[this.position++];
    }
  };

  // Factory method to return BookIteratorInterface<Book>
  createIterator(): BookIteratorInterface<Book> {
    return new this.BookIterator(this.books);
  }
}

const collection = new BookCollectionV2();
collection.addBook(new Book("Book A", "Author A"));
collection.addBook(new Book("Book B", "Author B"));

const iterator = collection.createIterator();
while (iterator.hasNext()) {
  const book = iterator.next();
  console.log(`${book.title} by ${book.author}`);
}
