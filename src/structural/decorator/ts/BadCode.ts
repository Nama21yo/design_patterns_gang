class PlainPizza {
  getDescription(): string {
    return "Plain pizza";
  }
  getCost(): number {
    return 5;
  }
}

class CheesePizza extends PlainPizza {
  getDescription(): string {
    return super.getDescription() + ", Cheese";
  }
  getCost(): number {
    return super.getCost() + 2;
  }
}

class TomatoPizza extends PlainPizza {
  getDescription(): string {
    return super.getDescription() + ", Tomato";
  }
  getCost(): number {
    return super.getCost() + 1.5;
  }
}

class CheeseTomatoPizza extends PlainPizza {
  getDescription(): string {
    return super.getDescription() + ", Cheese, Tomato";
  }
  getCost(): number {
    return super.getCost() + 3.5;
  }
}

// Usage
const pizza = new CheeseTomatoPizza();
console.log(pizza.getDescription() + " costs $" + pizza.getCost());
