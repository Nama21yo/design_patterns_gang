// Mediator interface
interface ChatMediator {
  send(message: string, from: User, to?: User): void;
  register(user: User): void;
}

// Mediator implementation
class ChatRoom implements ChatMediator {
  private users: Set<User> = new Set();

  register(user: User): void {
    this.users.add(user);
    user.setMediator(this);
  }

  send(message: string, from: User, to?: User): void {
    if (to) {
      to.receive(message, from);
    } else {
      // Broadcast to all except sender
      this.users.forEach(user => {
        if (user !== from) user.receive(message, from);
      });
    }
  }
}

class User {
  private mediator!: ChatMediator;
  constructor(public name: string) {}

  setMediator(mediator: ChatMediator) {
    this.mediator = mediator;
  }

  send(message: string, to?: User) {
    this.mediator.send(message, this, to);
  }

  receive(message: string, from: User) {
    console.log(`${this.name} receives message from ${from.name}: ${message}`);
  }
}

// Usage:
const chat = new ChatRoom();
const alice = new User('Alice');
const bob = new User('Bob');
const charlie = new User('Charlie');

chat.register(alice);
chat.register(bob);
chat.register(charlie);

alice.send('Hello everyone!');      // Broadcast to Bob, Charlie
bob.send('Hi Alice!', alice);       // Private message to Alice
charlie.send('How are you, Bob?', bob); // Private message to Bob
