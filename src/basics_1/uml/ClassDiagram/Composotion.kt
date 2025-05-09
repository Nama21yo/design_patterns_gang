package basics_1.uml.ClassDiagram

//Composition is stronger association
// one class owns another class
// The part can't exist independently of the whole
// Eg. whole - House ,part - Rooms
// Filled Diamond

class Book(val title: String, val author: String) {
    fun printDetails() {
        println("Book: $title by $author")
    }

}

class Library {
    private  val books = mutableListOf<Book>()

    fun addBook(title: String, author: String) {
        val book = Book(title, author)
        books.add(book)
    }

    fun showBooks() {
        for (book in books) {
            book.printDetails()
        }
    }
}

fun main() {
    val library = Library()
    // NB: Book Objects are created and managed inside library class
    // The library is gone, The book will also be lost
    library.addBook("Clean Code", "Robert C. Martin")
    library.addBook("Effective Kotlin", "Marcin Moskala")

    library.showBooks()
}