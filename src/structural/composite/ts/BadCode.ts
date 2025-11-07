class File {
  constructor(public name: string) {}
  move(destination: string) {
    console.log(`Moving file ${this.name} to ${destination}`);
  }
}

class Directory {
  private files: File[] = [];
  private directories: Directory[] = [];
  constructor(public name: string) {}

  addFile(file: File) {
    this.files.push(file);
  }

  addDirectory(dir: Directory) {
    this.directories.push(dir);
  }

  move(destination: string) {
    console.log(`Moving directory ${this.name} to ${destination}`);
    for (const file of this.files) {
      file.move(destination + "/" + this.name);
    }
    for (const dir of this.directories) {
      dir.move(destination + "/" + this.name);
    }
  }
}

// Usage
const file1 = new File("file1.txt");
const file2 = new File("file2.txt");

const dir1 = new Directory("dir1");
dir1.addFile(file1);
dir1.addFile(file2);

const dir2 = new Directory("dir2");

dir1.move("/backup");
dir2.move("/backup");
