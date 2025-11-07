class DocumentBad {
  private state: string = "draft";

  publish(): void {
    if (this.state === "draft") {
      console.log("Publishing document...");
      this.state = "published";
    } else if (this.state === "published") {
      console.log("DocumentBad already published.");
    } else if (this.state === "moderation") {
      console.log("Cannot publish: DocumentBad in moderation.");
    }
  }

  moderate(): void {
    if (this.state === "draft") {
      console.log("DocumentBad sent for moderation.");
      this.state = "moderation";
    } else if (this.state === "moderation") {
      console.log("DocumentBad already in moderation.");
    } else if (this.state === "published") {
      console.log("Published document cannot be moderated.");
    }
  }

  getState(): string {
    return this.state;
  }
}

// Usage
const doc = new DocumentBad();
doc.publish(); // Publishing document...
doc.moderate(); // Published document cannot be moderated.
doc.publish(); // DocumentBad already published.
