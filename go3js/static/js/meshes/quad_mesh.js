import * as THREE from "three";

class QuadMesh extends THREE.Mesh {
  constructor() {
    const geometry = new THREE.BufferGeometry();
    const vertices = new Float32Array([
      0.5, 0.5, 0.0, -0.5, 0.5, 0.0, -0.5, -0.5, 0.0, 0.5, 0.5, 0.0, -0.5, -0.5,
      0.0, 0.5, -0.5, 0.0,
    ]);

    // const indices = [0, 1, 2, 3, 4, 5];  // non-indexed buffer geometry, not needed

    geometry.setAttribute("position", new THREE.BufferAttribute(vertices, 3));
    // geometry.setIndex(indices);

    const material = new THREE.MeshBasicMaterial({ color: 0xff0000 });

    super(geometry, material);
  }
}

export { QuadMesh };
