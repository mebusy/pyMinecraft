from settings import *

# from meshes.quad_mesh import QuadMesh
# from world_objects.chunk import Chunk
from world import World


# for convenience, we will do all the rendering in the scene class
class Scene:
    def __init__(self, app):
        self.app = app
        # self.quad = QuadMesh(self.app)
        # self.chunk = Chunk(self.app)
        self.world = World(self.app)

    def update(self):
        pass

    def render(self):
        # self.quad.render()
        # self.chunk.render()
        self.world.render()
