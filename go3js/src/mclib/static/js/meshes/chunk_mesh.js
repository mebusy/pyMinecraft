import * as THREE from 'three'

import { getShaderMaterial } from '../utils.js'

class ChunkMesh extends THREE.Mesh {
  constructor(chunk) {
    const geometry = new THREE.BufferGeometry()

    // geometry.setAttribute('position', new THREE.BufferAttribute(vertices, 3))
    // geometry.setAttribute('in_color', new THREE.BufferAttribute(colors, 3)) // does it work ?
    // self.attrs = ("in_position", "voxel_id", "face_id")

    const material = getShaderMaterial('chunk')

    super(geometry, material)
  }
}

export { ChunkMesh }
