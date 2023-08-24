import { PerspectiveCamera } from "three";

class Camera extends PerspectiveCamera {
  constructor(fov = 50, aspect = 1, near = 0.1, far = 2000) {
    super(fov, aspect, near, far);
  }

  update() {
    // console.log("update");
  }
}

export { Camera };
