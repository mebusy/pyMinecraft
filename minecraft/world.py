from settings import *
from settings import WORLD_VOL, CHUNK_VOL, np, WORLD_W, WORLD_H, WORLD_D, WORLD_AREA
from world_objects.chunk import Chunk
from voxel_handler import VoxelHandler


class World:
    def __init__(self, app):
        self.app = app

        # list whose length will be equal to the number of chunks in the world
        self.chunks = [None for _ in range(WORLD_VOL)]
        # for performance purposes, all the voxels of our world divided into chunks
        # will be stored in separate 2d numpy arrays
        self.voxels = np.empty([WORLD_VOL, CHUNK_VOL], dtype="uint8")

        self.build_chunks()
        self.build_chunk_mesh()

        self.voxel_handler = VoxelHandler(self)

    def build_chunks(self):
        for x in range(WORLD_W):
            for y in range(WORLD_H):
                for z in range(WORLD_D):
                    chunk = Chunk(self, position=(x, y, z))

                    chunk_index = x + WORLD_W * z + WORLD_AREA * y
                    self.chunks[chunk_index] = chunk

                    # put the chunk voxels in a separate array
                    self.voxels[chunk_index] = chunk.build_voxels()

                    # get pointer to voxels
                    chunk.voxels = self.voxels[chunk_index]

    def build_chunk_mesh(self):
        for chunk in self.chunks:
            chunk.build_mesh()

    def update(self):
        self.voxel_handler.update()
        pass

    def render(self):
        for chunk in self.chunks:
            chunk.render()
