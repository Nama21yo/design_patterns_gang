// Component interface
interface FileSystemComponent {
  move(destination: string): void;
  getName(): string;
}

// Leaf
class File implements FileSystemComponent {
  constructor(private name: string) {}
  move(destination: string) {
    console.log(`Moving file ${this.name} to ${destination}`);
  }
  getName(): string {
    return this.name;
  }
}

// Composite
class Directory implements FileSystemComponent {
  private children: FileSystemComponent[] = [];
  constructor(private name: string) {}

  add(component: FileSystemComponent) {
    this.children.push(component);
  }

  move(destination: string) {
    console.log(`Moving directory ${this.name} to ${destination}`);
    for (const child of this.children) {
      child.move(destination + "/" + this.name);
    }
  }

  getName(): string {
    return this.name;
  }
}

// Usage
const file1 = new File("file1.txt");
const file2 = new File("file2.txt");

const dir1 = new Directory("dir1");
dir1.add(file1);
dir1.add(file2);

const dir2 = new Directory("dir2");

dir1.move("/backup");
dir2.move("/backup");
