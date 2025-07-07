package main

import (
	"fmt"
	"math"
)

func main() {
	const inflationRate = 2.5
	var investmentAmount float64
	var years float64
	// var years float64 = 10
	// var expectedReturnRate = 5.5
	// better way
	var expectedReturnRate float64

	fmt.Print("Investment Amount: ")
	fmt.Scan(&investmentAmount) // pointer is needed for reference
	
	fmt.Scan("Expected Return Rate: ")
	fmt.Print(&expectedReturnRate)

	fmt.Print("Number of Years: ")
	fmt.Scan(&years)

	var futureValue = (investmentAmount) * math.Pow((1 + (expectedReturnRate) / 100), (years))
	formattedFV := fmt.Sprintf("Future Value: %.1f\n", futureValue)
	futureRealValue := futureValue / math.Pow(1 + inflationRate / 100, years)
	formattedRFV := fmt.Sprintf("Future Real Value: %.1f\n", futureRealValue)

	// fmt.Println("Future Value:",futureValue)
	// fmt.Printf("Future Value: %.2f \nFuture Value (adjusted for inflation): %.2f", futureValue, futureRealValue)
	// fmt.Println((futureRealValue))
	fmt.Print(formattedFV, formattedRFV)
}

