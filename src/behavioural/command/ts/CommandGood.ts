// Command Interface
interface Command {
  execute(): void;
}

// Receiver: TextEditor with actual logic
class TextEditor {
  toggleBold() {
    console.log("Bold toggled");
  }

  toggleItalic() {
    console.log("Italic toggled");
  }

  toggleUnderline() {
    console.log("Underline toggled");
  }
}

// Concrete Commands
class BoldCommand implements Command {
  constructor(private editor: TextEditor) {}
  execute() {
    this.editor.toggleBold();
  }
}

class ItalicCommand implements Command {
  constructor(private editor: TextEditor) {}
  execute() {
    this.editor.toggleItalic();
  }
}

class UnderlineCommand implements Command {
  constructor(private editor: TextEditor) {}
  execute() {
    this.editor.toggleUnderline();
  }
}

// Invoker: Button executes a command and is independent of receiver
class Button {
  constructor(private command: Command) {}
  click() {
    this.command.execute();
  }
}

// Usage example:
const editor = new TextEditor();

const boldCommand = new BoldCommand(editor);
const italicCommand = new ItalicCommand(editor);
const underlineCommand = new UnderlineCommand(editor);

const boldButton = new Button(boldCommand);
const italicButton = new Button(italicCommand);
const underlineButton = new Button(underlineCommand);

boldButton.click(); // Bold toggled
italicButton.click(); // Italic toggled
underlineButton.click(); // Underline toggled
