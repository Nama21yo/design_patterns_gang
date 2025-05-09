package basics_1.uml.ClassDiagram

// Realization/Implementation is a r/ship where class implements an interface
// It is a Contractual Relationship
// meaning the class agrees to perform the behaviour defined in the interface

//similar to inheritance but applies to interface, not classes
//"can-do" relationship

// Interface defines what to do and the class defines how to do it

interface Flyable {
    fun fly()
}

class Bird : Flyable {
    override fun fly() {
        println("Bird is Flying using Wings")
    }
}

class Airplane : Flyable {
    override fun fly() {
        println("Airplane is flying using jet Engines")
    }
}

fun main() {
    val bird = Bird()
    val airplane : Flyable = Airplane()

    bird.fly()
    airplane.fly()
}