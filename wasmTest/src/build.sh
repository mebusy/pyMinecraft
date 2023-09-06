#!/bin/sh

set -e

GOARCH=wasm GOOS=wasip1 go build -o test.wasm .

