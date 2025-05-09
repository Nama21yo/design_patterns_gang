package basics_1.uml.ClassDiagram

//Dependency is where one class uses another class temporarily to perform a task
// "uses-a" relationship
// weaker than the rest
// One class depends on another clss to complete its function,
// usually via method parameters or local variable
//Symbol - Broken Arrow

//Eg car and Fuel
//ReportGenerator uses a Printer class to print a report, but does not own it or store it as a member.


class Printer {
    fun print(text: String) {
        println("Printing: $text")
    }
}

// ReportGenerator class depends on Printer
class ReportGenerator {
    fun generate(printer: Printer) {
        val report = "Annual Report 2025"
        println("Generating report...")
        printer.print(report)  // Using Printer (temporary)
    }
}

fun main() {
    val printer = Printer()
    val generator = ReportGenerator()

    generator.generate(printer)  // Dependency: ReportGenerator uses Printer
}
