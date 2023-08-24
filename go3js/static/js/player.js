import { Camera } from "./camera.js";

class Player extends Camera {
  constructor(fov = 50, aspect = 1, near = 0.1, far = 2000) {
    super(fov, aspect, near, far);

    this.position.z = 5;
  }

  update() {
    // console.log("update");
  }
}

export { Player };
