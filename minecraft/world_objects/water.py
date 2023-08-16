from meshes.quad_mesh_water import QuadMeshWater
from settings import *


class Water:
    def __init__(self, app):
        self.app = app
        self.mesh = QuadMeshWater(app)

    def render(self):
        self.mesh.render()
