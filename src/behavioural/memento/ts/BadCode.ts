class TextEditorBad {

  private content: string = "";
  private history: string[] = []; //stack

  write(text: string): void {
    //  INSIDE the Class
  // The undo/history logic directly copies and restores every single private field.
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
