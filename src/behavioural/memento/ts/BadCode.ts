class TextEditorBad {
  private content: string = "";
  private history: string[] = [];

  write(text: string): void {
    this.history.push(this.content);
    this.content = text;
  }

  undo(): void {
    if (this.history.length > 0) {
      this.content = this.history.pop()!;
    }
  }
}

//  Mixed Responsibilities
//  Limited Undo/Redo Functionality
//  Inefficient State Management
// No Encapsulation of State
