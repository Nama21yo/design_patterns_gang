package main

import "fmt"

// ! OCP Violation
// function calculatePrice(price: number, discountType: string): number {
// 	if (discountType === "10%") return price * 0.9;
// 	else if (discountType === "20%") return price * 0.8;
// 	else if (discountType === "30%") return price * 0.7;
// 	else throw new Error("Invalid discount");
//   }

var discounts = map[string]float64 {
	"10%": 0.9,
	"20%": 0.8,
	"30%": 0.7,
}
  

func calculatePrice(price float64, discountType string) (float64, error) {
	rate , exists := discounts[discountType]

	if !exists {
		return 0, fmt.Errorf("Invalid discount Type")
	}
	return price * rate , nil
}


func main() {
	price, err := calculatePrice(100, "20%")
	if err != nil {
		fmt.Println(err)
		return
	}
	fmt.Printf("Discounted price: $%.2f \n", price)
}
