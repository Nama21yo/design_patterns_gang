
public class TextEditorMain {

    public static void main(String[] args) {
        TextEditor editor = new TextEditor();
        CareTaker caretaker = new CareTaker();

        editor.write("Hello Momento");
        caretaker.saveState(editor);
        editor.write("Hello Undo");
        caretaker.saveState(editor);

        // undo it
        caretaker.undo(editor);

        System.out.println(editor.getContent())
   }
}
// 
