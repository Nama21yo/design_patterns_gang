public class CareTaker {
    private final Stack<EditorMemento> history = new Stack<>();

    public void saveState(TextEditor editor) {
        // save the state
        history.push(editor.save())
    }

    public void undo(TextEditor editor) {
        if(!history.empty()) {
            history.pop()
            editor.restore(history.peek())
        }
    }
}
// 
