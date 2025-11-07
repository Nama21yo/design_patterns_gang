// Component interface
interface Pizza {
  getDescription(): string;
  getCost(): number;
}

// Concrete Component
class PlainPizza implements Pizza {
  getDescription(): string {
    return "Plain pizza";
  }
  getCost(): number {
    return 5;
  }
}

// Decorator base class
abstract class ToppingDecorator implements Pizza {
  protected tempPizza: Pizza;

  constructor(pizza: Pizza) {
    this.tempPizza = pizza;
  }

  abstract getDescription(): string;
  abstract getCost(): number;
}

// Concrete Decorators
class Cheese extends ToppingDecorator {
  getDescription(): string {
    return this.tempPizza.getDescription() + ", Cheese";
  }
  getCost(): number {
    return this.tempPizza.getCost() + 2;
  }
}

class Tomato extends ToppingDecorator {
  getDescription(): string {
    return this.tempPizza.getDescription() + ", Tomato";
  }
  getCost(): number {
    return this.tempPizza.getCost() + 1.5;
  }
}

class Olives extends ToppingDecorator {
  getDescription(): string {
    return this.tempPizza.getDescription() + ", Olives";
  }
  getCost(): number {
    return this.tempPizza.getCost() + 2.5;
  }
}

// Usage
let pizza: Pizza = new PlainPizza();
pizza = new Cheese(pizza);
pizza = new Tomato(pizza);
pizza = new Olives(pizza);

console.log(pizza.getDescription() + " costs $" + pizza.getCost());
