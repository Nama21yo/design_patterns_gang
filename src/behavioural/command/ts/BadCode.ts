class TextEditor {
  private content: string = "";

  toggleBold() {
    console.log("Bold toggled");
    // logic to toggle bold on selected text
  }

  toggleItalic() {
    console.log("Italic toggled");
    // logic to toggle italic on selected text
  }

  toggleUnderline() {
    console.log("Underline toggled");
    // logic to toggle underline on selected text
  }
}

// Buttons directly call editor methods (tightly coupled)
class BoldButton {
  constructor(private editor: TextEditor) {}

  click() {
    this.editor.toggleBold();
  }
}

class ItalicButton {
  constructor(private editor: TextEditor) {}

  click() {
    this.editor.toggleItalic();
  }
}

class UnderlineButton {
  constructor(private editor: TextEditor) {}

  click() {
    this.editor.toggleUnderline();
  }
}

// Usage:
const editor = new TextEditor();
const boldButton = new BoldButton(editor);
const italicButton = new ItalicButton(editor);
const underlineButton = new UnderlineButton(editor);

boldButton.click(); // Bold toggled
italicButton.click(); // Italic toggled
underlineButton.click(); // Underline toggled
