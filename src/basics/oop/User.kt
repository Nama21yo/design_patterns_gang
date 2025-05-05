package basics.oop

import java.lang.reflect.Method

class User(val name: String, val bankAccount: BankAccount, val paymentService: PaymentService) {
    fun makeDeposit(amount: Double) {
        bankAccount.deposit(amount)
        println("$name deposited $$amount. New balance ${bankAccount.get_Balance()}")
    }

    fun makeWithdrawal(amount: Double) {
        bankAccount.withdraw(amount)
        println("$name withdraw $$amount. New Balance: ${bankAccount.get_Balance()}")
    }

    fun pay(amount: Double, paymentMethod: Card) {
        println("$name is attempting to pay $$amount using ${paymentMethod.javaClass.simpleName}...")
        paymentService.makePayment(amount, paymentMethod) // Runtime Polymorphism
    }

}