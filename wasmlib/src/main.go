package main

import (
	"fmt"
)

//go:wasmexport
func hello(name string) {
	fmt.Println("Hello", name)
}

func main() {}
