// Violating SRP
//! Bad Implementation
// class EmployeeManager {
//     fun calculateSalary() { /* ... */ }
//     fun saveToFile() { /* ... */ }
//     fun printReport() { /* ... */ }
// }

// the class does too much — 3 responsibilities:

// Business logic (salary)

// Persistence (file saving)

// Presentation (report printing)

// only for creating an EMployee
class Employee {
  constructor(name, salary) {
    this.name = name;
    this.salary = salary;
  }
}

// For calculating the salary of the Employee
class SalaryCalculator {
  calculate(employee) {
    return employee.salary * 1.1;
  }
}

// for saving mostly related to database
class EmployeeRepository {
  save(employee) {
    console.log(`Saving ${employee.name} to file...`);
  }
}

// Display the Employee Information
class ReportPrinter {
  print(employee) {
    console.log(`Employee ${employee.name}, Salary: ${employee.salary}`);
  }
}

const employee = new Employee("Natnael Yo", 5000);
const calculator = new SalaryCalculator();
const repository = new EmployeeRepository();
const printer = new ReportPrinter();

employee.salary = calculator.calculate(employee);
repository.save(employee);
printer.print(employee);
