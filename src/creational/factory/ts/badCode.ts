// // this is interface
// // interface Transport {
// //     deliver(): void
// // }
// type Transport = { deliver(): void };

// class Car implements Transport {
//   deliver(): void {
//     console.log("Deliver by car");b
//   }
// }
// class Bus implements Transport {
//   deliver(): void {
//     console.log("Deliver by Bus");
//   }
// }

// class Bike implements Transport {
//   deliver(): void {
//     console.log("Deliver by bike");
//   }
// }

// // factory deisgn pattern
// function clientCode(transportType: string) {
//   let transport: Transport;

//   if (transportType === "car") {
//     transport = new Car();
//   } else if (transportType === "bike") {
//     transport = new Bike();
//   } else if (transportType === "bus") {
//     transport = new Bus();
//   } else {
//     throw new Error("Unknown transport type");
//   }

//   transport.deliver();
// }

// clientCode("car");
// clientCode("bike");
