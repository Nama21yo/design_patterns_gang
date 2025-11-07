class HouseBad {
  constructor(
    public walls: string,
    public roof: string,
    public doors: string,
    public windows: string,
    public garage: boolean,
    public swimmingPool: boolean
  ) {}

  toString() {
    return (
      `House with ${this.walls} walls, ${this.roof} roof, ${this.doors} doors, ${this.windows} windows, ` +
      `garage: ${this.garage}, swimming pool: ${this.swimmingPool}`
    );
  }
}

// Usage: long and confusing constructor arguments
const house1 = new HouseBad("Brick", "Tile", "Wooden", "Glass", true, false);
console.log(house1.toString());
