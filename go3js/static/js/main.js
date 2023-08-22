import * as THREE from "three";
import * as SETTINGS from "./settings.js";

// control
import { OrbitControls } from "three/addons/controls/OrbitControls.js";

const scene = new THREE.Scene();

const camera = new THREE.PerspectiveCamera(
  75,
  window.innerWidth / window.innerHeight,
  0.1,
  1000,
);

const renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// control
const controls = new OrbitControls(camera, renderer.domElement);

const geometry = new THREE.BoxGeometry(1, 1, 1);
const material = new THREE.MeshBasicMaterial({ color: 0x00ff00 });
const cube = new THREE.Mesh(geometry, material);
scene.add(cube);

camera.position.z = 5;

const clock = new THREE.Clock();

scene.background = new THREE.Color(...SETTINGS.BG_COLOR);

function animate() {
  requestAnimationFrame(animate);

  // const elapsed = clock.getElapsedTime();
  const delta = clock.getDelta();

  // console.log(delta);

  cube.rotation.x += delta;
  cube.rotation.y += delta;

  renderer.render(scene, camera);
}

animate();
