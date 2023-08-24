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
const clock = new THREE.Clock();

// ! update
function update() {
  // const elapsed = clock.getElapsedTime();
  const delta = clock.getDelta();

  // console.log(delta);
  // cube.rotation.x += delta;
  // cube.rotation.y += delta;

  // uniformData.u_time.value = clock.getElapsedTime();
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
