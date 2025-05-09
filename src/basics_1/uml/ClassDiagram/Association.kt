package basics_1.uml.ClassDiagram

//Association is a relationship where one class uses another.
// It is a "has-a" relation-ship
//Each object in on class is associated with one or more object of another class
//Symbol - Just a line
class School(val name: String, val address: String)

class Student(val name: String, val age: Int, val school: School) {
    fun printDetails() {
        println("Student Name: $name")
        println("Age: $age")
        println("School: ${school.name}")
        println("Address: ${school.address}")
    }
}

fun main() {
    val school = School("AAU", "Addis Ababa")
    val student = Student("Natnael Yohanes", 20, school)

    student.printDetails()
}