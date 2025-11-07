
class User {
  private friends: User[] = [];
  constructor(public name: string) {}

  addFriend(user: User) {
    this.friends.push(user);
  }

  send(message: string, to: User): void {
    console.log(`${this.name} sends message to ${to.name}: ${message}`);
    to.receive(message, this);
  }

  receive(message: string, from: User): void {
    console.log(`${this.name} receives message from ${from.name}: ${message}`);
  }
}

// Usage
const alice = new User('Alice');
const bob = new User('Bob');
const charlie = new User('Charlie');

alice.addFriend(bob);
alice.addFriend(charlie);

alice.send('Hey Bob!', bob);
bob.send('Hi Alice!', alice);
charlie.send('Hello Bob!', bob);
