from settings import *
from settings import np, CHUNK_VOL, CHUNK_SIZE, CHUNK_AREA
from meshes.chunk_mesh import ChunkMesh


class Chunk:
    def __init__(self, app):
        self.app = app
        self.voxels: np.ndarray = self.build_voxels()
        self.mesh: ChunkMesh = None

        self.build_mesh()

    def build_voxels(self):
        # empty chunk
        voxels = np.zeros(CHUNK_VOL, dtype=np.uint8)

        # fill chunk
        # idx = X + SIZE * Z + AREA * Y
        for x in range(CHUNK_SIZE):
            for z in range(CHUNK_SIZE):
                for y in range(CHUNK_SIZE):
                    voxels[x + CHUNK_SIZE * z + CHUNK_AREA * y] = 1

        return voxels

    def build_mesh(self):
        self.mesh = ChunkMesh(self)

    def render(self):
        self.mesh.render()
