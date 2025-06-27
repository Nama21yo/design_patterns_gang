// // Violates Liskov Substitution Principle (LSP)

// class File {
//   write(content) {
//     console.log(`Writing content: ${content}`);
//   }

//   read() {
//     console.log("Reading content");
//     return "file content";
//   }
// }

// class ReadOnlyFile extends File {
//   //  This is BAD: We're breaking the expected behavior of File
//   write(content) {
//     throw new Error("Cannot write to a read-only file");
//   }
// }

// const file = new File();
// file.write("Hello");
// file.read();

// const readonly = new ReadOnlyFile();
// // This will throw, violating substitutability
// readonly.write("Trying to write"); // BAD: breaks LSP

// Interface-like abstract classes

class Readable {
  read() {
    throw new Error("Method 'read()' must be implemented.");
  }
}

class Writable {
  write(content) {
    throw new Error("Method 'write()' must be implemented.");
  }
}

//  Concrete class for readable files
class ReadableFile extends Readable {
  constructor(content) {
    super();
    this.content = content;
  }

  read() {
    console.log("Reading content");
    return this.content;
  }
}

// Concrete class for writable files (inherits readable behavior)
class WritableFile extends ReadableFile {
  write(content) {
    this.content = content;
    console.log(`Writing content: ${content}`);
  }
}

// Usage

const readable = new ReadableFile("Initial read-only data");
console.log(readable.read());
const writable = new WritableFile("Initial writable data");
console.log(writable.read());
writable.write("New content");
console.log(writable.read());
