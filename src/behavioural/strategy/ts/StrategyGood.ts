interface PaymentStrategy {
  processPayment(amount: number): void;
}
// concrete starategies
class PayPalStrategy implements PaymentStrategy {
  processPayment(amount: number): void {
    console.log(`Paid ${amount} using PayPal.`);
  }
}

class CreditCardStrategy implements PaymentStrategy {
  processPayment(amount: number): void {
    console.log(`Paid ${amount} using Credit Card.`);
  }
}

class BitcoinStrategy implements PaymentStrategy {
  processPayment(amount: number): void {
    console.log(`Paid ${amount} using Bitcoin.`);
  }
}

// context
class OnlineStore {
  private paymentStrategy: PaymentStrategy;
  constructor(paymentStrategy: PaymentStrategy) {
    this.paymentStrategy = paymentStrategy;
  }
  setPaymentStrategy(strategy: PaymentStrategy): void {
    // allows runtime switching
    this.paymentStrategy = strategy;
  }
  checkout(amount: number): void {
    this.paymentStrategy.processPayment(amount);
  }
}

const store = new OnlineStore(new PayPalStrategy());
store.checkout(100); // Paid 100 using PayPal.

store.setPaymentStrategy(new CreditCardStrategy());
store.checkout(200); // Paid 200 using Credit Card.

store.setPaymentStrategy(new BitcoinStrategy());
store.checkout(300); // Paid 300 using Bitcoin.
