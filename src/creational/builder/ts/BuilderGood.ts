// Product class
class House {
  walls?: string;
  roof?: string;
  doors?: string;
  windows?: string;
  garage?: boolean;
  swimmingPool?: boolean;

  toString(): string {
    return (
      `House with ${this.walls} walls, ${this.roof} roof, ${this.doors} doors, ${this.windows} windows, ` +
      `garage: ${this.garage}, swimming pool: ${this.swimmingPool}`
    );
  }
}

// Builder interface
interface HouseBuilder {
  setWalls(walls: string): this;
  setRoof(roof: string): this;
  setDoors(doors: string): this;
  setWindows(windows: string): this;
  setGarage(garage: boolean): this;
  setSwimmingPool(swimmingPool: boolean): this;
  build(): House;
}

// Concrete Builder
class ConcreteHouseBuilder implements HouseBuilder {
  private house: House = new House();

  setWalls(walls: string): this {
    this.house.walls = walls;
    return this;
  }
  setRoof(roof: string): this {
    this.house.roof = roof;
    return this;
  }
  setDoors(doors: string): this {
    this.house.doors = doors;
    return this;
  }
  setWindows(windows: string): this {
    this.house.windows = windows;
    return this;
  }
  setGarage(garage: boolean): this {
    this.house.garage = garage;
    return this;
  }
  setSwimmingPool(swimmingPool: boolean): this {
    this.house.swimmingPool = swimmingPool;
    return this;
  }
  build(): House {
    return this.house;
  }
}

// Usage
const builder = new ConcreteHouseBuilder();
const house2 = builder
  .setWalls("Brick")
  .setRoof("Tile")
  .setDoors("Wooden")
  .setWindows("Glass")
  .setGarage(true)
  .setSwimmingPool(false)
  .build();

console.log(house2.toString());
