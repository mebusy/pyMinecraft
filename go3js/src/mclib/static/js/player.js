import { Camera } from './camera.js'

class Player extends Camera {
  constructor(fov, aspect, near, far) {
    super(fov, aspect, near, far)

    this.position.z = 5
  }

  update() {
    // console.log("update");
  }
}

export { Player }
