import * as THREE from 'three'

class QuadMesh extends THREE.Mesh {
  constructor() {
    const geometry = new THREE.BufferGeometry()

    // prettier-ignore
    const vertices = new Float32Array([
      0.5, 0.5, 0.0, 
      -0.5, 0.5, 0.0, 
      -0.5, -0.5, 0.0, 
      0.5, 0.5, 0.0, 
      -0.5, -0.5, 0.0,
      0.5, -0.5, 0.0,
    ])
    // const indices = [0, 1, 2, 3, 4, 5];  // non-indexed buffer geometry, not needed
    const colors = new Float32Array([0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1])

    geometry.setAttribute('position', new THREE.BufferAttribute(vertices, 3))
    // geometry.setIndex(indices);
    geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3)) // does it work ?

    const material = new THREE.MeshBasicMaterial({ color: 0xff0000 })

    super(geometry, material)
  }
}

export { QuadMesh }
