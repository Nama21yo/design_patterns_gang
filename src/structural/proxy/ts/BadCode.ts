class RealImageBad {
  constructor(private filename: string) {
    this.loadFromDisk();
  }

  private loadFromDisk() {
    console.log("Loading image from disk:", this.filename);
  }

  display() {
    console.log("Displaying", this.filename);
  }
}

// The application loads from disk every time, even if not displayed
const img1 = new RealImageBad("large_photo.jpg"); // Loads from disk
img1.display();

const img2 = new RealImageBad("large_photo.jpg"); // Loads again from disk
img2.display();
