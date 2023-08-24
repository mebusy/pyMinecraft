import * as THREE from "three";
import * as SETTINGS from "./settings.js";

import { Scene } from "./scene.js";
import { Player } from "./player.js";

import Stats from "./libs/Stats.js";

// show fps
const stats = new Stats();
stats.showPanel(0);
document.body.appendChild(stats.dom);

// render
const renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// ! init
const scene = new Scene();
const player = new Player(
  75,
  window.innerWidth / window.innerHeight,
  0.1,
  1000
);
// player.position.z = 5;

const geometry = new THREE.BoxGeometry(1, 1, 1);
const material = new THREE.MeshBasicMaterial({ color: 0x00ff00 });
const cube = new THREE.Mesh(geometry, material);
scene.add(cube);

const clock = new THREE.Clock();

scene.background = new THREE.Color(...SETTINGS.BG_COLOR);

// ! update
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

  update();

  // ! render
  renderer.render(scene, player);

  stats.end();
}

// control
import { OrbitControls } from "three/addons/controls/OrbitControls.js";
const controls = new OrbitControls(player, renderer.domElement);

mainLoop();
