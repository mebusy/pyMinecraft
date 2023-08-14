from settings import *
from settings import (
    glm,
    MAX_RAY_DIST,
    WORLD_D,
    WORLD_H,
    WORLD_W,
    WORLD_AREA,
    CHUNK_SIZE,
    CHUNK_AREA,
)
from meshes.chunk_mesh_builder import get_chunk_index


class VoxelHandler:
    def __init__(self, world):
        self.app = world.app
        self.chunks = world.chunks

        # ray casting result
        self.chunk = None
        self.voxel_id = None
        self.voxel_index = None
        self.voxel_local_pos = None
        self.voxel_world_pos = None
        self.voxel_normal = None
        # [A Fast Voxel Traversal Algorithm for Ray Tracing](http://www.cse.yorku.ca/~amana/research/grid.pdf)

        # we need an attribute that will determine the mode of interaction with voxel
        # that is we need switch between adding and removing voxel
        self.interaction_mode = 0  # 0: remove voxel   1: add voxel

        # to add a voxel, we will define an attribute with a non-zero value
        self.new_voxel_id = 1

    def add_voxel(self):
        if self.voxel_id:
            # check voxel id along the normal
            result = self.get_voxel_id(self.voxel_world_pos + self.voxel_normal)

            # is the new place empty ?
            if not result[0]:
                _, voxel_index, _, chunk = result

                # here you should pay attention to whether the chunk was empty
                if chunk.is_empty:
                    chunk.is_empty = False

                chunk.voxels[voxel_index] = self.new_voxel_id
                chunk.mesh.rebuild()

    # so far, we don't handle the case when the voxel is on the boundary of the chunk
    # we need a method to rebuild an adjacent chunk defined by the adjacent voxel in relation to our voxel being removed
    def rebuild_adjacent_chunk(self, adj_voxel_pos):
        index = get_chunk_index(adj_voxel_pos)  # get the index of the adjacent chunk
        if index != -1:
            self.chunks[index].mesh.rebuild()

    # we have 6 adjacent voxels, we need to check them all
    def rebuild_adjacent_chunks(self):
        lx, ly, lz = self.voxel_local_pos
        wx, wy, wz = self.voxel_world_pos

        # we will determine whether the voxel is on the border of the current chunk
        if lx == 0:
            self.rebuild_adjacent_chunk((wx - 1, wy, wz))
        elif lx == CHUNK_SIZE - 1:
            self.rebuild_adjacent_chunk((wx + 1, wy, wz))

        if ly == 0:
            self.rebuild_adjacent_chunk((wx, wy - 1, wz))
        elif ly == CHUNK_SIZE - 1:
            self.rebuild_adjacent_chunk((wx, wy + 1, wz))

        if lz == 0:
            self.rebuild_adjacent_chunk((wx, wy, wz - 1))
        elif lz == CHUNK_SIZE - 1:
            self.rebuild_adjacent_chunk((wx, wy, wz + 1))

    def remove_voxel(self):
        # print(f"remove_voxel {self.voxel_id} !!")
        if self.voxel_id:
            self.chunk.voxels[self.voxel_index] = 0

            # this is why we make the world with chunks.
            # use chunks we can only rebuild only the affected chunks, not the whole world.
            self.chunk.mesh.rebuild()
            # also we need to rebuild the adjacent chunks
            self.rebuild_adjacent_chunks()

    def set_voxel(self):
        if self.interaction_mode:
            self.add_voxel()
        else:
            self.remove_voxel()

    def switch_mode(self):
        self.interaction_mode = not self.interaction_mode
        # print(f'cur mode: {self.interaction_mode}')

    def update(self):
        self.ray_cast()

    def ray_cast(self):
        # start point
        x1, y1, z1 = self.app.player.position
        # end point
        x2, y2, z2 = self.app.player.position + self.app.player.forward * MAX_RAY_DIST

        current_voxel_pos = glm.ivec3(x1, y1, z1)
        self.voxel_id = 0
        self.voxel_normal = glm.ivec3(0)
        step_dir = -1

        dx = glm.sign(x2 - x1)
        delta_x = min(dx / (x2 - x1), 10000000.0) if dx != 0 else 10000000.0
        max_x = delta_x * (1.0 - glm.fract(x1)) if dx > 0 else delta_x * glm.fract(x1)

        dy = glm.sign(y2 - y1)
        delta_y = min(dy / (y2 - y1), 10000000.0) if dy != 0 else 10000000.0
        max_y = delta_y * (1.0 - glm.fract(y1)) if dy > 0 else delta_y * glm.fract(y1)

        dz = glm.sign(z2 - z1)
        delta_z = min(dz / (z2 - z1), 10000000.0) if dz != 0 else 10000000.0
        max_z = delta_z * (1.0 - glm.fract(z1)) if dz > 0 else delta_z * glm.fract(z1)

        while not (max_x > 1.0 and max_y > 1.0 and max_z > 1.0):
            # on each iteraction of the ray casting, we check if the current voxel
            result = self.get_voxel_id(voxel_world_pos=current_voxel_pos)
            # if the result voxel is not empty, when we will update the value of all attributes defined
            # to obtain the results of  the ray casting for the current voxel
            if result[0]:
                (
                    self.voxel_id,
                    self.voxel_index,
                    self.voxel_local_pos,
                    self.chunk,
                ) = result
                self.voxel_world_pos = current_voxel_pos

                # to calculate the normal to the voxel, we will use the step_dir as an identifier,
                # this normal will be needed to correctly implement the choice of position for setting new voxel when they are added
                if step_dir == 0:
                    self.voxel_normal.x = -dx
                elif step_dir == 1:
                    self.voxel_normal.y = -dy
                else:
                    self.voxel_normal.z = -dz
                return True

            if max_x < max_y:
                if max_x < max_z:
                    current_voxel_pos.x += dx
                    max_x += delta_x
                    step_dir = 0
                else:
                    current_voxel_pos.z += dz
                    max_z += delta_z
                    step_dir = 2
            else:
                if max_y < max_z:
                    current_voxel_pos.y += dy
                    max_y += delta_y
                    step_dir = 1
                else:
                    current_voxel_pos.z += dz
                    max_z += delta_z
                    step_dir = 2
        return False

    def get_voxel_id(self, voxel_world_pos):
        cx, cy, cz = chunk_pos = voxel_world_pos / CHUNK_SIZE

        if 0 <= cx < WORLD_W and 0 <= cy < WORLD_H and 0 <= cz < WORLD_D:
            chunk_index = cx + WORLD_W * cz + WORLD_AREA * cy
            chunk = self.chunks[chunk_index]

            lx, ly, lz = voxel_local_pos = voxel_world_pos - chunk_pos * CHUNK_SIZE

            voxel_index = lx + CHUNK_SIZE * lz + CHUNK_AREA * ly
            voxel_id = chunk.voxels[voxel_index]

            return voxel_id, voxel_index, voxel_local_pos, chunk
        return 0, 0, 0, 0
