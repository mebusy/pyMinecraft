from meshes.quad_mesh_water import QuadMeshWater
from settings import *


class Water:
    # use one quad mesh, be enlage to the size of whole world, and
    # render upon the world
    def __init__(self, app):
        self.app = app
        self.mesh = QuadMeshWater(app)

    def render(self):
        self.mesh.render()
