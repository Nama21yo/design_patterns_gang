// Momento class that stores the internal state of the TextEditor

public class EditorMemento {
    private final String content

    public EditorMemento(String content) {
        this.content = content
    }

    public String getContent() {
        return content
    }
}
