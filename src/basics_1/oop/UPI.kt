package basics_1.oop

class UPI(val upiId : String) : PaymentMethod {
    override fun pay(amount: Double) {
        println("Making payment via UPI: $upiId")
    }
}