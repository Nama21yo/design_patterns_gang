package basics_1.uml.ClassDiagram

//Inheritance is "is-a" relationship

// Open Keyword allows class to be inherited by default class are final
// Symbol - arrow
open class Animal(val name: String) {
    fun eat() {
        println("$name is eating")
    }

    fun sleep() {
        println("$name is sleeping")
    }
}

// DOg inherits Animal
class Dog(name: String) : Animal(name) {
    fun bark() {
        println("$name is barking")
    }
}

fun main() {
    val dog = Dog("Puppy")

    dog.eat() // inherited from Animal
    dog.sleep() // inherited from Animal
    dog.bark() // innate
}