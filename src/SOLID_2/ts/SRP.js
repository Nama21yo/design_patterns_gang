// Violating SRP
// class EmployeeManager {
//     fun calculateSalary() { /* ... */ }
//     fun saveToFile() { /* ... */ }
//     fun printReport() { /* ... */ }
// }
// the class does too much — 3 responsibilities:
// Business logic (salary)
// Persistence (file saving)
// Presentation (report printing)
var Employee = /** @class */ (function () {
    function Employee(name, salary) {
        this.name = name;
        this.salary = salary;
    }
    return Employee;
}());
var SalaryCalculator = /** @class */ (function () {
    function SalaryCalculator() {
    }
    SalaryCalculator.prototype.calculate = function (employee) {
        return employee.salary * 1.1;
    };
    return SalaryCalculator;
}());
var EmployeeRepository = /** @class */ (function () {
    function EmployeeRepository() {
    }
    EmployeeRepository.prototype.save = function (employee) {
        console.log("Saving ".concat(employee.name, " to file..."));
    };
    return EmployeeRepository;
}());
var ReportPrinter = /** @class */ (function () {
    function ReportPrinter() {
    }
    ReportPrinter.prototype.print = function (employee) {
        console.log("Employee ".concat(employee.name, ", Salary: ").concat(employee.salary));
    };
    return ReportPrinter;
}());
var employee = new Employee("Natnael Yo", 5000);
var calculator = new SalaryCalculator();
var repository = new EmployeeRepository();
var printer = new ReportPrinter();
employee.salary = calculator.calculate(employee);
repository.save(employee);
printer.print(employee);
