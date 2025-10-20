class CareTaker {
  private history: EditorMemento[] = [];

  saveState(editor: TextEditor): void {
    this.history.push(editor.save());
  }

  undo(editor: TextEditor): void {
    if (this.history.length > 1) {
      this.history.pop();
      editor.restore(this.history[this.history.length - 1]);
    }
  }
}
