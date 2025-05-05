package basics.oop

abstract class Card (val cardNumber: String, val expiryDate: String, val ownerName: String) : PaymentMethod {
    abstract fun authorizePayment(amount: Double) : Boolean

    override fun pay(amount: Double) { // it was final that why it becomes open
        if (authorizePayment(amount)) {
            println("Payment of $$amount auhtorized for card: $cardNumber")
        } else {
            println("Payment is Failed")
        }
    }

}