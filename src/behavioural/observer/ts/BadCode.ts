class WeatherStationBad {
  private temperature: number = 0;
  private device1: DeviceBad;
  private device2: DeviceBad;
  // ... more devices

  constructor(device1: DeviceBad, device2: DeviceBad) {
    this.device1 = device1;
    this.device2 = device2;
  }
  setTemperature(temp: number): void {
    this.temperature = temp;
    this.notifyDevice(this.device1);
    this.notifyDevice(this.device2);
    // If you add another device, you must write more code here!
  }
  notifyDevice(device: DeviceBad): void {
    device.display(this.temperature);
  }
}

class DeviceBad {
  display(temp: number) {
    console.log(`Temperature is ${temp}°C`);
  }
}
