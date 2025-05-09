package basics_1.oop

class DebitCard (cardNumber: String, expiryDate : String, ownerName : String, private var balance : Double) : Card(cardNumber, expiryDate, ownerName){
    override fun authorizePayment(amount: Double): Boolean {
        return if (amount <= balance) {
            balance -= amount
            true
        } else {
            false
        }
    }
    override fun pay(amount: Double) {
        println("Processing via Debit Card...")
        super.pay(amount)
    }
}