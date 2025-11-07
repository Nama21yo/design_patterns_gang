interface Image {
  display(): void;
}

class RealImage implements Image {
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

class ProxyImage implements Image {
  private realImage: RealImage | null = null;

  constructor(private filename: string) {}

  display(): void {
    if (!this.realImage) {
      this.realImage = new RealImage(this.filename); // Loads only once
    }
    this.realImage.display();
  }
}

// Usage
const imgProxy = new ProxyImage("large_photo.jpg"); // No disk load yet
console.log("Created proxy image; not loaded from disk yet");
imgProxy.display();  // Loads image from disk now, then displays
imgProxy.display();  // Instantly displays, no re-load
