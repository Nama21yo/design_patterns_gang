class PaymentProcessorBad {
  process(amount: number, method: string): void {
    if (method === "paypal") {
      console.log(`Paid ${amount} using PayPal.`);
    } else if (method === "creditcard") {
      console.log(`Paid ${amount} using Credit Card.`);
    } else if (method === "bitcoin") {
      console.log(`Paid ${amount} using Bitcoin.`);
    } else {
      throw new Error("Unsupported payment method");
    }
  }
}

const processor = new PaymentProcessorBad();
processor.process(100, "paypal"); // OK
processor.process(200, "creditcard"); // OK
processor.process(300, "bitcoin"); // OK
