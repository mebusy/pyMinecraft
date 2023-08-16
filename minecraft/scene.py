# from settings import *

import moderngl as mgl

# from meshes.quad_mesh import QuadMesh
# from world_objects.chunk import Chunk
from world import World

from world_objects.voxel_marker import VoxelMarker
from world_objects.water import Water
from world_objects.clouds import Clouds


# for convenience, we will do all the rendering in the scene class
class Scene:
    def __init__(self, app):
        self.app = app
        # self.quad = QuadMesh(self.app)
        # self.chunk = Chunk(self.app)
        self.world = World(self.app)
        self.voxel_marker = VoxelMarker(self.world.voxel_handler)
        self.water = Water(app)
        self.clouds = Clouds(app)

    def update(self):
        self.world.update()
        self.voxel_marker.update()
        # self.water.update()  # no update
        self.clouds.update()

    def render(self):
        # self.quad.render()
        # self.chunk.render()
        self.world.render()

        self.app.ctx.disable(mgl.CULL_FACE)
        self.clouds.render()
        self.water.render()
        self.app.ctx.enable(mgl.CULL_FACE)

        # render last
        self.voxel_marker.render()
