// Transport Interface
type Transport = { deliver(): void };

// Concrete Products
class Car implements Transport {
  deliver(): void {
    console.log("Deliver by car");
  }
}

class Bike implements Transport {
  deliver(): void {
    console.log("Deliver by bike");
  }
}

// Factory Class
class TransportFactory {
  static createTransport(type: string): Transport {
    switch (type) {
      case 'car':
        return new Car();
      case 'bike':
        return new Bike();
      default:
        throw new Error('Unknown transport type');
    }
  }
}

// Client code
function clientCode(type: string) {
  const transport = TransportFactory.createTransport(type);
  transport.deliver();
}

clientCode('car');  
clientCode('bike');
