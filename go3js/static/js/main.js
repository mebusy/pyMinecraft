import * as THREE from "three";
import * as SETTINGS from "./settings.js";

import { Scene } from "./scene.js";

import Stats from "./libs/Stats.js";

// show fps
const stats = new Stats();
stats.showPanel(0);
document.body.appendChild(stats.dom);

// control
import { OrbitControls } from "three/addons/controls/OrbitControls.js";

const scene = new Scene();

const camera = new THREE.PerspectiveCamera(
  75,
  window.innerWidth / window.innerHeight,
  0.1,
  1000
);

const renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

const geometry = new THREE.BoxGeometry(1, 1, 1);
const material = new THREE.MeshBasicMaterial({ color: 0x00ff00 });
const cube = new THREE.Mesh(geometry, material);
scene.add(cube);

camera.position.z = 5;

const clock = new THREE.Clock();

scene.background = new THREE.Color(...SETTINGS.BG_COLOR);

function update() {
  // const elapsed = clock.getElapsedTime();
  const delta = clock.getDelta();

  // console.log(delta);
  cube.rotation.x += delta;
  cube.rotation.y += delta;
}

function mainLoop() {
  requestAnimationFrame(mainLoop);

  stats.begin();

  // ! update
  update();

  // ! render
  renderer.render(scene, camera);

  stats.end();
}

// control
const controls = new OrbitControls(camera, renderer.domElement);

mainLoop();
