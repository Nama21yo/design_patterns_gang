package basics_1.uml.ClassDiagram

//Aggregation is weaker association
//One class has a reference to another class
// The whole and the part can exist independently
// EG. Department can exist independently of Student, and vice versa
// Symbol - Shallow Diamond
class Department(val name:String)

class Pupil(val name: String, val department: Department) {
    fun printInfo() {
        println("Pupil Name: $name")
        println("Department : ${department.name}")
    }
}

fun main() {
    val softwareDepartment = Department("Software Engineering")

    val student = Pupil("Natnael Yohanes", softwareDepartment)

    student.printInfo()
}