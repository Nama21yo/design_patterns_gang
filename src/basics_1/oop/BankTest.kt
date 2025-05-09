package basics_1.oop

fun main() {
    // Step 1: Create a user with a bank account
    val bankAccount = BankAccount(12345, 1000.0)
    val paymentService = PaymentService()
    val user = User("John Doe", bankAccount, paymentService)

    println("\n--- User & Bank Account Created ---")
    println("${user.name} has been set up with account ${bankAccount.accountNumber} and an initial balance of ${bankAccount.get_Balance()}.")

    // Step 2: Add Payment Methods (Credit & Debit Cards)
    val creditCard = CreditCard("1234-5678-9012-3456", "12/27", "John Doe", 500.0)
    val debitCard = DebitCard("9876-5432-1098-7654", "11/26", "John Doe", 300.0)

    paymentService.addPaymentMethod(creditCard)
    paymentService.addPaymentMethod(debitCard)

    println("\n--- Payment Methods Added ---")
    paymentService.listPaymentMethods()

    // Step 3: Deposit & Withdraw Money
    println("\n--- Bank Transactions ---")
    user.makeDeposit(200.0) // Successful deposit
    user.makeWithdrawal(150.0) // Successful withdrawal
    user.makeWithdrawal(1200.0) // Failed withdrawal (insufficient funds)

    // Step 4: Make Payments Using Payment Methods
    println("\n--- Making Payments ---")
    user.pay(250.0, creditCard)  // Successful payment with credit card
    user.pay(600.0, debitCard)   // Failed payment (insufficient balance)
}
