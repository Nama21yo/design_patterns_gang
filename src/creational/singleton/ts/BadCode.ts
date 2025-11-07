// Each time you use Database, a new instance (and connection) is created.
class DatabaseBad {
  private connection: string;

  constructor() {
    // Here we'd establish a new connection
    this.connection = `Connection@${Math.random()}`;
    console.log('New DB connection created:', this.connection);
  }

  query(sql: string): void {
    // Simulate DB query
    console.log(`Executing: ${sql} on ${this.connection}`);
  }
}

// Usage:
const db1 = new DatabaseBad();
db1.query('SELECT * FROM users');

const db2 = new DatabaseBad(); // New connection, possibly wasteful and dangerous
db2.query('SELECT * FROM products');
