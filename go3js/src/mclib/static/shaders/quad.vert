// For 3js built-in uniform & attributes
// check : https://threejs.org/docs/#api/en/renderers/webgl/WebGLProgram

/* attribute vec3 position;  // `position, normal, uv` can not use other name */
in vec3 in_color;  // attribute in 1.0

out vec3 color;  // varying in 1.0

void main() {
    color = in_color;
    // projectionMatrix, modelViewMatrix, position -> passed in from Three.js
    gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
    /* gl_Position = vec4(position, 1.0) ; */
}

