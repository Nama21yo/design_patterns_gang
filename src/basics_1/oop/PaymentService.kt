package basics_1.oop

//It manages multiple PaymentMethods/Cards
class PaymentService {
    private val paymentMethods = mutableListOf<Card>()

    fun addPaymentMethod(paymentMethod: Card) {
        paymentMethods.add(paymentMethod)
        println("${paymentMethod.ownerName}'s payment method added successfully.")
    }
    fun makePayment(amount: Double, paymentMethod: Card) {
        println("Attempting payment of $$amount using ${paymentMethod.ownerName}'s ${paymentMethod.javaClass.simpleName}...")
        paymentMethod.pay(amount)
    }
    fun listPaymentMethods() {
        if (paymentMethods.isEmpty()) {
            println("No Payment Methods Available")
        } else {
            println("Available payment methods:")
            paymentMethods.forEach { method -> println("- ${method.ownerName}'s ${method.javaClass.simpleName} (Card: ${method.cardNumber})") }
        }
    }
}

