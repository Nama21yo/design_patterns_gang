// //  BAD: Machine interface with too many responsibilities

// class Machine {
//   print(doc) {
//     throw new Error("Not implemented");
//   }

//   scan(doc) {
//     throw new Error("Not implemented");
//   }

//   copy(doc) {
//     throw new Error("Not implemented");
//   }
// }

// //  Violates ISP — SimplePrinter shouldn't be forced to implement scan/copy
// class SimplePrinter extends Machine {
//   print(doc) {
//     console.log(`Printing: ${doc}`);
//   }

//   scan(doc) {
//     throw new Error("Scan not supported");
//   }

//   copy(doc) {
//     throw new Error("Copy not supported");
//   }
// }

// const simplePrinter = new SimplePrinter();
// simplePrinter.print("Hello World");
// simplePrinter.scan("Hello World");   // Error - violates ISP

//  Segregated interfaces (abstract base classes)

class Printer {
  print(doc) {
    throw new Error("Method 'print()' must be implemented.");
  }
}

class Scanner {
  scan(doc) {
    throw new Error("Method 'scan()' must be implemented.");
  }
}

class Copier {
  copy(doc) {
    throw new Error("Method 'copy()' must be implemented.");
  }
}

// SimplePrinter only implements what it needs
class SimplePrinter extends Printer {
  print(doc) {
    console.log(`SimplePrinter printing: ${doc}`);
  }
}

//  MultiPurposeMachine implements all interfaces
class MultiPurposeMachine extends Printer {
  constructor() {
    super();
  }

  print(doc) {
    console.log(`MultiPurposeMachine printing: ${doc}`);
  }

  scan(doc) {
    console.log(`MultiPurposeMachine scanning: ${doc}`);
  }

  copy(doc) {
    console.log(`MultiPurposeMachine copying: ${doc}`);
  }
}

// Usage

const simple = new SimplePrinter();
simple.print("Document A"); //  Works
// simple.scan("Document A"); //  Not available

const mpm = new MultiPurposeMachine();
mpm.print("Doc 1");
mpm.scan("Doc 2");
mpm.copy("Doc 3");
