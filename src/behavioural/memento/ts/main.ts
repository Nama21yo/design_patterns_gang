const editor = new TextEditor();
const caretaker = new CareTaker();

editor.write("Hello Memento");
caretaker.saveState(editor);
editor.write("Hello Undo");
caretaker.saveState(editor);

caretaker.undo(editor);

console.log(editor.getContent()); // Output: Hello Memento
