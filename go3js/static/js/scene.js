import { Scene as THREE_Scene, Color as THREE_Color } from "three";
import * as SETTINGS from "./settings.js";

class Scene extends THREE_Scene {
  constructor() {
    super();

    this.background = new THREE_Color(...SETTINGS.BG_COLOR);
  }

  update() {
    // console.log("update");
  }
}

export { Scene };
