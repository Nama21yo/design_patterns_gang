package basics.oop

class BankAccount(val accountNumber: Int, var balance: Double) {
//    val accountNumber: Number,
//    val balance: Number
//
//    constructor(accountNumber: Number, balance: Number) {
//        this.accountNumber = accountNumber
//        this.balance = balance
//    } this can be done in other way in Kotlin

    fun deposit(amount: Double) {
        if (amount > 0) {
            balance += amount
            println("Deposited $amount. New Balance. $balance")
        } else {
            println("Deposit amount must be Positive")
        }
    }

    fun withdraw(amount: Double) {
        if (amount > 0 && amount <= balance) {
            balance -= amount
            println("Withdrawn $amount. New balance: $balance")
        } else {
            println("Invalid Withdrawal Amount")
        }
    }

    fun get_Balance(): Double {
        return balance
    }

    fun getAccount(): Int {
        return accountNumber
    }
}

fun main() {
    val myAccount = BankAccount(12345, 1000.0) // Create a bank account with an initial balance of 1000

    println("Initial Balance: ${myAccount.get_Balance()}")

    myAccount.deposit(500.0)   // Depositing money
    myAccount.withdraw(200.0)  // Withdrawing money
    myAccount.withdraw(1500.0) // Attempting an invalid withdrawal

    println("Final Balance: ${myAccount.get_Balance()}")
}
