package main

import (
	"fmt"
)

// CAUTION: wasmexport is not implemented yet.

//go:wasmexport
func hello(name string) {
	fmt.Println("Hello", name)
}

func main() {
	fmt.Println("wasm main")
}
