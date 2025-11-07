The **Proxy design pattern** is a structural pattern that provides a surrogate or placeholder for another object to control access to it. The proxy object implements the same interface as the real object and sits between the client and the real object. This lets the proxy mediate requests, add extra behavior, or restrict direct access, without modifying the real object's code.[1][2][3][4][5]

---

### Key Intent

- **Control and manage access** to a resource or object.
- Add abilities like lazy initialization, caching, access protection, logging, and remote communication.
- Allow client code to interact with a proxy exactly as it would with the real object.

---

### Main Participants

- **Subject:** Defines the common interface—both real object and proxy provide the same methods.
- **RealSubject:** The actual object that does real work (e.g., the expensive resource, remote service, or protected operation).
- **Proxy:** Implements the same interface, keeps a reference to the RealSubject, and forwards requests to it; adds any extra logic as needed.
- **Client:** Uses the proxy instead of the real object, usually unaware of the extra logic or presence of proxy.

---

### Common Uses

- **Virtual Proxy:** Defers expensive object creation to when needed (lazy loading).
- **Protection Proxy:** Checks permissions; restricts access according to rules.
- **Remote Proxy:** Represents an object in a different address space, handling communication.
- **Cache Proxy:** Saves/computes results to avoid repeated expense.
- **Logging Proxy:** Monitors and logs interactions with the real object.

---

### Benefits

- **Encapsulates** complex or expensive logic behind a simple interface.[2]
- **Adds cross-cutting concerns** without modifying real object.
- Enables **lazy initialization**, **security checks**, or **logging** with client code unchanged.[5]

---

### Example Analogy

A company network firewall acts as a proxy: it stands between employees and the outside internet, filtering and logging all traffic. Employees use the internet interface just as they would, but with extra security added by the proxy.

---

### Example Setup

In TypeScript, a proxy might wrap a database connection, file operation, or image loader, controlling when and how resources are used:

```typescript
interface Image {
  display(): void;
}

class RealImage implements Image {
  private filename: string;
  constructor(filename: string) {
    this.filename = filename;
    this.loadFromDisk();
  }
  private loadFromDisk() {
    console.log("Loading " + this.filename);
  }
  display(): void {
    console.log("Displaying " + this.filename);
  }
}

// Virtual Proxy for lazy initialization
class ProxyImage implements Image {
  private realImage: RealImage | null = null;
  constructor(private filename: string) {}
  display() {
    if (!this.realImage) this.realImage = new RealImage(this.filename);
    this.realImage.display();
  }
}

// Usage
const image = new ProxyImage("pic.jpg");
image.display(); // Loads on first use; subsequent calls are fast
```

This type of proxy is ideal for objects that are expensive to create or load.

---

### Summary Table

| Proxy Type       | Purpose/Usage                     |
| ---------------- | --------------------------------- |
| Virtual Proxy    | Lazy load expensive resources     |
| Protection Proxy | Restrict/authorize access         |
| Remote Proxy     | Facilitate remote interactions    |
| Cache Proxy      | Store results for future requests |
| Logging Proxy    | Audit/log interactions            |

---

Would you like a full TypeScript example comparing bad code and good proxy implementation in a particular domain (such as file access, API calls, or authentication)?

[1](https://www.geeksforgeeks.org/system-design/proxy-design-pattern/)
[2](http://www.carloscaballero.io/understanding-the-proxy-design-pattern/)
[3](https://refactoring.guru/design-patterns/proxy)
[4](https://www.digitalocean.com/community/tutorials/proxy-design-pattern)
[5](https://dev.to/srishtikprasad/proxy-design-pattern-4mm)
[6](https://en.wikipedia.org/wiki/Proxy_pattern)
[7](https://www.youtube.com/watch?v=cHg5bWW4nUI)
[8](https://www.linkedin.com/pulse/proxy-design-pattern-right-those-people-who-act-behalf-santilli)
[9](https://endjin.com/blog/2020/12/design-patterns-in-csharp-the-proxy-pattern)
