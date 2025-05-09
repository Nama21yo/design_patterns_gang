package main

import "fmt"

// Employee represents basic Employee Structure
// has responsibility of creating Employee
type Employee struct {
	Name string
	salary float64
}

// has responsibility of calculating Employee salary
type SalaryCalculator struct {}

func (sc SalaryCalculator) Calculate(e *Employee) float64 {
	return e.salary * 1.1
}


// saving employee file to the database
type EmployeeRepository struct {}

func (er EmployeeRepository) Save(e Employee) {
	fmt.Printf("Saving %s to file \n", e.Name)
}

// Display the Employee Info
type ReportPrinter struct{}

func (rp ReportPrinter) Print(e Employee) {
	fmt.Printf("Employee: %s, Salary: %.2f \n", e.Name, e.salary)
}

// func main() {
//     employee := Employee{Name: "Natnael Yohanes", salary: 5000}
// 	calculator := SalaryCalculator{}
// 	repository := EmployeeRepository{}
// 	printer := ReportPrinter{}

// 	employee.salary = calculator.Calculate(&employee)
// 	repository.Save(employee)
// 	printer.Print(employee)
// }

