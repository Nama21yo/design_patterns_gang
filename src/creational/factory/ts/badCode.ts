// type Transport = { deliver(): void };

// class Car implements Transport {
//   deliver(): void {
//     console.log("Deliver by car");
//   }
// }

// class Bike implements Transport {
//   deliver(): void {
//     console.log("Deliver by bike");
//   }
// }

// function clientCode(transportType: string) {
//   let transport: Transport;

//   if (transportType === "car") {
//     transport = new Car();
//   } else if (transportType === "bike") {
//     transport = new Bike();
//   } else {
//     throw new Error("Unknown transport type");
//   }

//   transport.deliver();
// }

// clientCode("car"); // Output: Deliver by car
// clientCode("bike"); // Output: Deliver by bike
