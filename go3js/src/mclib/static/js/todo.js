// very basic
// const geometry = new THREE.BoxGeometry(1, 1, 1);
// const material = new THREE.MeshBasicMaterial({ color: 0x00ff00 });
// const cube = new THREE.Mesh(geometry, material);
// scene.add(cube);

/*
// use shader
const boxGeometry = new THREE.BoxGeometry(16, 16, 16, 16, 16, 16);
const boxMaterial = new THREE.ShaderMaterial({
  wireframe: true,
  vertexShader: `
      void main()	{
        // projectionMatrix, modelViewMatrix, position -> passed in from Three.js
        gl_Position = projectionMatrix
          * modelViewMatrix
          * vec4(position.x, position.y, position.z, 1.0);
      }
      `,
  fragmentShader: `
      void main() {
        gl_FragColor = vec4(1.0, 0.0, 0.0, 1.0);
      }
      `,
});
const boxMesh = new THREE.Mesh(boxGeometry, boxMaterial);
scene.add(boxMesh);
//*/

// shader + uniform
const uniformData = {
  u_time: {
    type: "f",
    value: clock.getElapsedTime(),
  },
};
// varying variables
const boxGeometry = new THREE.BoxGeometry(24, 4, 24, 24, 4, 24);
const boxMaterial = new THREE.ShaderMaterial({
  wireframe: true,
  uniforms: uniformData,
  vertexShader: `
      varying vec3 pos;
      uniform float u_time;

      void main()	{
        vec4 result;
        pos = position;

        result = vec4(
          position.x,
          4.0*sin(position.z/4.0 + u_time) + position.y,
          position.z,
          1.0
        );

        gl_Position = projectionMatrix
          * modelViewMatrix
          * result;
      }
      `,
  fragmentShader: `
      varying vec3 pos;
      uniform float u_time;
      void main() {
        if (pos.x >= 0.0) {
          // gl_FragColor = vec4(1.0, 0.0, 0.0, 1.0);
          gl_FragColor = vec4(abs(sin(u_time)), 0.0, 0.0, 1.0);
        } else {
          // gl_FragColor = vec4(0.0, 1.0, 0.0, 1.0);
          gl_FragColor = vec4(0.0, abs(cos(u_time)), 0.0, 1.0);
        }
      }
      `,
});
const boxMesh = new THREE.Mesh(boxGeometry, boxMaterial);
scene.add(boxMesh);
