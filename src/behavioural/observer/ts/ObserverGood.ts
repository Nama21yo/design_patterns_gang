// this is based on the gang of four book
// observer interface
interface Observer {
  update(temperature: number): void;
}

// subject base class
abstract class Subject {
  private observers: Observer[] = [];

  addObserver(observer: Observer): void {
    this.observers.push(observer);
  }
  removeObserver(observer: Observer): void {
    this.observers = this.observers.filter((o) => o !== observer);
  }
  protected notifyObservers(temp: number): void {
    for (const observer of this.observers) {
      observer.update(temp);
    }
  }
}

// concrete subject
class WeatherStation extends Subject {
  private temperature: number = 0;

  setTemperature(temp: number): void {
    this.temperature = temp;
    this.notifyObservers(temp);
  }
  getTemperature(): number {
    return this.temperature;
  }
}

// concrete observers
class TemperatureDisplay implements Observer {
  private name: string;
  constructor(name: string) {
    this.name = name;
  }
  update(temp: number): void {
    console.log(`${this.name}: Latest temperature is ${temp}°C`);
  }
}

class MobileAppDisplay implements Observer {
  update(temp: number): void {
    console.log(`Mobile App: Weather station reports ${temp}°C`);
  }
}

const station = new WeatherStation();
const d1 = new TemperatureDisplay("Living Room");
const d2 = new TemperatureDisplay("Greenhouse");
const mobileApp = new MobileAppDisplay();

station.addObserver(d1);
station.addObserver(d2);
station.addObserver(mobileApp);

station.setTemperature(27); // All displays will be updated automatically
station.setTemperature(25);
station.removeObserver(d2);
station.setTemperature(22); // Only d1 and mobileApp get the update now
