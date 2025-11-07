class Database {
  private static instance: Database;
  private connection: string;

  // Private constructor prevents direct instantiation
  private constructor() {
    this.connection = `Connection@${Math.random()}`;
    console.log("New DB connection created:", this.connection);
  }

  // Static method to get the one instance
  public static getInstance(): Database {
    if (!Database.instance) {
      Database.instance = new Database();
    }
    return Database.instance;
  }

  query(sql: string): void {
    console.log(`Executing: ${sql} on ${this.connection}`);
  }
}

// Usage:
const db1 = Database.getInstance();
db1.query("SELECT * FROM users");

const db2 = Database.getInstance();
db2.query("SELECT * FROM products");

console.log(db1 === db2); // true — same instance, same connection
