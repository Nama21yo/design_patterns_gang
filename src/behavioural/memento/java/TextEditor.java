public class TextEditor {
    private String content

    public void write(String text) {
        this.content = text
    }

    public String getContent() {
        return content
    }
    // ? Problem - Undo the last write
        // Solution1 
                // - Use stack but violates single responsibility if implemented here
            
    // save a current state

    public EditorMemento save() {
        return new EditorMemento(content)
    }

    public void restore(EditorMemento memento) {
        content = memento.getContent()
    }
}
// 
