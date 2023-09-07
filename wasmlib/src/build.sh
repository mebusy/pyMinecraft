#!/bin/sh

set -e

cp "$(go env GOROOT)/misc/wasm/wasm_exec.js" ../../go3js/src/mclib/static/js/
GOARCH=wasm GOOS=wasip1 go build -o  ../../go3js/src/mclib/static/bin/lib.wasm  .
# GOARCH=wasm GOOS=js go build -o  ../../go3js/src/mclib/static/bin/lib.wasm  .

