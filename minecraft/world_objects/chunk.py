from settings import *
from settings import np, CHUNK_VOL, CHUNK_SIZE, CHUNK_AREA, glm
from meshes.chunk_mesh import ChunkMesh


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

    def get_model_matrix(self):
        # model matrix of the chunk based on the coordinates of its position
        m_model = glm.translate(glm.mat4(), glm.vec3(self.position) * CHUNK_SIZE)
        return m_model

    def set_uniform(self):
        self.mesh.program["m_model"].write(self.m_model)

    def build_voxels(self):
        # empty chunk
        voxels = np.zeros(CHUNK_VOL, dtype="uint8")

        # fill chunk
        # idx = X + SIZE * Z + AREA * Y
        for x in range(CHUNK_SIZE):
            for z in range(CHUNK_SIZE):
                for y in range(CHUNK_SIZE):
                    # voxels[x + CHUNK_SIZE * z + CHUNK_AREA * y] = x + y + z
                    voxels[x + CHUNK_SIZE * z + CHUNK_AREA * y] = (
                        x + y + z
                        if int(glm.simplex(glm.vec3(x, y, z) * 0.1) + 1)
                        else 0
                    )

        return voxels

    def build_mesh(self):
        self.mesh = ChunkMesh(self)

    def render(self):
        self.set_uniform()
        self.mesh.render()
