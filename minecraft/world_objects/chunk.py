from settings import *
from settings import np, CHUNK_VOL, CHUNK_SIZE, CHUNK_AREA, glm
from meshes.chunk_mesh import ChunkMesh

# import random

from terrain_gen import get_height


class Chunk:
    def __init__(self, world, position):
        self.app = world.app
        self.world = world
        self.position = position

        # in order to place the chunks in our world we need to
        # write a method to get the model matrix
        self.m_model = self.get_model_matrix()
        self.voxels: np.ndarray = None  # self.build_voxels()

        self.mesh: ChunkMesh = None
        # self.build_mesh()

        # optimization
        self.is_empty = True

        self.center = (glm.vec3(self.position) + 0.5) * CHUNK_SIZE
        # for convinience
        self.is_on_frustum = self.app.player.frustum.is_on_frustum

    def get_model_matrix(self):
        # model matrix of the chunk based on the coordinates of its position
        m_model = glm.translate(glm.mat4(), glm.vec3(self.position) * CHUNK_SIZE)
        return m_model

    def set_uniform(self):
        self.mesh.program["m_model"].write(self.m_model)

    def build_voxels(self):
        # empty chunk
        voxels = np.zeros(CHUNK_VOL, dtype="uint8")

        # now only fill the non-empty voxels
        # do not care about whether those voxels are visible or not
        # the mesh builder will take care of the visibility

        # chunk postion in world
        cx, cy, cz = glm.ivec3(self.position) * CHUNK_SIZE
        # debug
        # rng = random.randrange(1, 100)
        self.generate_terrain(voxels, cx, cy, cz)

        # optimization
        if np.any(voxels):
            self.is_empty = False

        return voxels

    def build_mesh(self):
        # optimization
        if not self.is_empty:
            self.mesh = ChunkMesh(self)

    def render(self):
        # optimization
        if not self.is_empty and self.is_on_frustum(self):
            self.set_uniform()
            self.mesh.render()

    @staticmethod
    @njit
    def generate_terrain(voxels, cx, cy, cz):
        # idx = X + SIZE * Z + AREA * Y
        for x in range(CHUNK_SIZE):
            for z in range(CHUNK_SIZE):
                wx = cx + x  # voxel x in world
                wz = cz + z  # voxel z in world
                # height of terrain , voxels in vertical direction
                # world_height = int(glm.simplex(glm.vec2(wx, wz) * 0.01) * 32 + 32)
                world_height = get_height(wx, wz)
                # local height of chunk
                local_height = min(CHUNK_SIZE, world_height - cy)

                # fill the voxels in vertical direction of the chunk
                for y in range(local_height):
                    wy = cy + y  # voxel y in world
                    # voxels[x + CHUNK_SIZE * z + CHUNK_AREA * y] = x + y + z
                    voxels[x + CHUNK_SIZE * z + CHUNK_AREA * y] = 2  # wy + 1
