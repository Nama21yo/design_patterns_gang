# Observer Pattern Explained

## Intent

**Observer** is a behavioral design pattern that creates a subscription mechanism, allowing multiple other objects to be notified automatically whenever an important event occurs in the observed object (the "subject" or "publisher").[1][2][3]

## Problem

Suppose you have two entities: a **Customer** and a **Store**. Customers want to know if a specific product becomes available, but:

- If the customer constantly checks the store, they waste time (polling).
- If the store sends notifications to _all_ customers whenever any product comes in, people get spammed who don't care.

How can you let _interested_ customers find out _immediately_ and automatically without polling or spamming everyone?

## Solution

The solution is the Observer pattern:

- Have the publisher (e.g., the Store) maintain a list of subscribers (e.g., Customers) who are interested in specific events.
- When an event happens, the publisher notifies **all** its subscribers via a common interface (e.g., a method like `update`).
- Subscribers can register/unregister dynamically, even at runtime.
- The publisher doesn't need to know anything about what the subscribers do with the event—it just calls their notification method.

## Key Concepts

- **Publisher (Subject):** Has state/events and notifies subscribers when changes occur.
- **Subscribers (Observers):** Interested in certain events. Implement a common notification interface.
- **Loose coupling:** Publisher and subscribers interact only through interfaces, not concrete types. The publisher doesn't care what subscribers do, only that they have a way (`update`) to notify them.

## Real-World Analogy

Magazine subscriptions:

- You subscribe to news or magazines. When a new edition is released (published), only subscribers receive it in their mailbox.
- You can unsubscribe any time. The publisher doesn't deliver unsubscribed customers anymore.

## Structure (UML-style)

- Publisher holds a list of subscribers.
- Subscribers implement a common interface (e.g., `EventListener`, with an `update(data)` method).
- On an event, publisher calls `update()` on all subscribers.

## Pseudocode Example

Imagine a text editor that lets listeners react to file events:

```typescript
// Subscriber interface
interface EventListener {
  update(filename: string): void;
}

// Publisher holding and notifying subscribers
class EventManager {
  private listeners: { [eventType: string]: EventListener[] } = {};

  subscribe(eventType: string, listener: EventListener) {
    if (!this.listeners[eventType]) this.listeners[eventType] = [];
    this.listeners[eventType].push(listener);
  }
  unsubscribe(eventType: string, listener: EventListener) {
    this.listeners[eventType] = (this.listeners[eventType] || []).filter(
      (l) => l !== listener
    );
  }
  notify(eventType: string, data: string) {
    (this.listeners[eventType] || []).forEach((l) => l.update(data));
  }
}

// Concrete Subscribers
class LoggingListener implements EventListener {
  constructor(private logFile: string, private msgTemplate: string) {}
  update(filename: string) {
    // Log message using the template and filename
  }
}

class EmailAlertsListener implements EventListener {
  constructor(private email: string, private msgTemplate: string) {}
  update(filename: string) {
    // Send email with message and filename
  }
}

// Usage
const publisher = new EventManager();
const logger = new LoggingListener("log.txt", "Opened file: %s");
publisher.subscribe("open", logger);
const mailer = new EmailAlertsListener("admin@example.com", "Changed file: %s");
publisher.subscribe("save", mailer);

// When editor opens/saves, fires events
publisher.notify("open", "chapter1.txt"); // Logger reacts
publisher.notify("save", "chapter1.txt"); // Email alerts react
```

## When to Use the Pattern

- When some objects should be able to react to the state/event changes of another object, and you don't know (or don't want to hard-code) who those objects will be ahead of time.
- Whenever you need **decoupled event notification**, such as in graphical user interfaces, stock tickers, or any publish/subscribe architecture.[2][4]

## Key Benefits

- **Loose coupling:** Publisher and subscribers are not tightly linked.
- **Flexible:** Subscribers can be added/removed at runtime, and you can add new subscriber types without modifying the publisher.
- **Open/Closed Principle:** Observers can react to changes in new ways, and you can introduce new subscriber behavior without changing the publisher.

## Downsides

- Notification order of subscribers is not guaranteed.
- May be complex if there are lots of publishers/subscribers or high event frequency.

---

Would you like to see a real-world example in your preferred language, or a quick quiz to help you test your understanding next?

If you have any particular use case in mind (like event-driven UI, or backend notifications), let me know and I can tailor the next explanation for that!

[1](https://www.geeksforgeeks.org/system-design/observer-pattern-set-1-introduction/)
[2](https://refactoring.guru/design-patterns/observer)
[3](https://www.baeldung.com/java-observer-pattern)
[4](https://learn.microsoft.com/en-us/dotnet/standard/events/observer-design-pattern)
[5](https://www.linkedin.com/pulse/implementing-observer-pattern-real-world-example-predrag-nasti%C4%87-7lnif)
[6](https://www.patterns.dev/vanilla/observer-pattern/)
[7](https://www.digitalocean.com/community/tutorials/observer-design-pattern-in-java)
[8](https://www.reddit.com/r/gamedev/comments/y8dac1/various_implementations_of_the_observer_pattern/)
[9](https://www.tutorialspoint.com/design_pattern/observer_pattern.htm)
