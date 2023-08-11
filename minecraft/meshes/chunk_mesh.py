from meshes.base_mesh import BaseMesh
from meshes.chunk_mesh_builder import build_chunk_mesh


class ChunkMesh(BaseMesh):
    def __init__(self, chunk):
        super().__init__()
        self.app = chunk.app
        self.chunk = chunk
        self.ctx = self.app.ctx
        self.program = self.app.shader_program.chunk

        # self.vbo_format = "3u1 1u1 1u1 1u1 1u1"
        self.vbo_format = "1u4"  # after packing data
        # these is a good idea to parse this format to get its size
        self.format_size = sum(int(fmt[:1]) for fmt in self.vbo_format.split())
        # attributes names passed to the shader
        # self.attrs = ("in_position", "voxel_id", "face_id", "ao_id", "flip_id")
        self.attrs = ("packed_data", )  # after packing data, NOTE it is tuple

        self.vao = self.get_vao()

    def get_vertex_data(self):
        mesh = build_chunk_mesh(
            chunk_voxels=self.chunk.voxels,
            format_size=self.format_size,
            # the voxels faces at the boundaries of the chunk are not need to draw
            # so we need to know the neighbors of each voxel to know if we need to draw a face
            chunk_pos=self.chunk.position,
            world_voxels=self.chunk.world.voxels,
        )
        return mesh

    def rebuild(self):
        self.vao = self.get_vao()