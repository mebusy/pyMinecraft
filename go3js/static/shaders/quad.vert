// For 3js built-in uniform & attributes
// check : https://threejs.org/docs/#api/en/renderers/webgl/WebGLProgram

/* attribute vec3 position;  // `position, normal, uv` can not use other name */
attribute vec3 in_color;

varying vec3 color;

void main() {
    color = in_color;
    // projectionMatrix, modelViewMatrix, position -> passed in from Three.js
    gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
    /* gl_Position = vec4(position, 1.0) ; */
}

