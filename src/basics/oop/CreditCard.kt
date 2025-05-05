package basics.oop

class CreditCard(cardNumber: String, expiryDate: String, ownerName : String, private var creditLimit : Double) : Card(cardNumber, expiryDate, ownerName) {
    override fun authorizePayment(amount: Double): Boolean {
        return if (amount <= creditLimit) {
            creditLimit -= amount
            true
        } else {
            false
        }
    }

     override fun pay(amount: Double) {
        println("Processing Payment via CreditCard...")
        super.pay(amount)
    }
}