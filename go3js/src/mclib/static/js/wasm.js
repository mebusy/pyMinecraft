// https://xebia.com/blog/golang-webassembly/

function load(pathWasm) {
  const go = new Go()
  console.log(go)
  const importObject = { wasi_snapshot_preview1: go.importObject }
  // https://young.github.io/intro-to-web-assembly/assembly-script/imports
  // const importObject = go.importObject
  WebAssembly.instantiateStreaming(fetch(pathWasm), importObject).then((obj) => {
    // Call an exported function:
    obj.instance.exports.hello('wasm')

    // or access the buffer contents of an exported memory:
    // const i32 = new Uint32Array(obj.instance.exports.memory.buffer)

    // or access the elements of an exported table:
    const table = obj.instance.exports.table
    // console.log(table.get(0)())
    console.log(obj.instance)
  })
}

export { load }
