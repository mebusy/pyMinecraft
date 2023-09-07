import { ShaderMaterial as THREE_ShaderMaterial } from 'three'

function fetchData(url) {
  const request = new XMLHttpRequest()
  request.open('GET', url, false) // `false` makes the request synchronous
  request.send(null)

  if (request.status === 200) {
    return request.responseText
  }
}

function getShaderMaterial(shaderName) {
  const vert = fetchData(`/static/shaders/${shaderName}.vert`)
  // console.log(vert)
  const frag = fetchData(`/static/shaders/${shaderName}.frag`)

  const shaderMaterial = new THREE_ShaderMaterial({
    // wireframe: true,
    // uniforms: uniformData,
    vertexShader: vert,
    fragmentShader: frag,
  })

  return shaderMaterial
}

export { fetchData, getShaderMaterial }
