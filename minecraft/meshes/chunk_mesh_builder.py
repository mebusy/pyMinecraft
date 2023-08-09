from settings import *
from settings import (
    np,
    CHUNK_VOL,
    CHUNK_SIZE,
    CHUNK_AREA,
    WORLD_W,
    WORLD_H,
    WORLD_D,
    WORLD_AREA,
    njit,
)
from numba import uint8


@njit
def to_uint8(x, y, z, voxel_id, face_id):
    return uint8(x), uint8(y), uint8(z), uint8(voxel_id), uint8(face_id)


# determine the index of its chunk by the world coordinates of the voxel
@njit
def get_chunk_index(world_voxel_pos):
    wx, wy, wz = world_voxel_pos
    cx = wx // CHUNK_SIZE
    cy = wy // CHUNK_SIZE
    cz = wz // CHUNK_SIZE
    if not (0 <= cx < WORLD_W and 0 <= cy < WORLD_H and 0 <= cz < WORLD_D):
        return -1
    index = cx + WORLD_W * cz + WORLD_AREA * cy
    return index


@njit
def is_void(local_voxel_pos, world_voxel_pos, world_voxels):
    chunk_index = get_chunk_index(world_voxel_pos)
    if chunk_index == -1:
        # not in chunk
        return False

    chunk_voxels = world_voxels[chunk_index]

    x, y, z = local_voxel_pos

    # Caution: x,y,z may be negative or greater than CHUNK_SIZE
    # that is , -1 is equivalent to CHUNK_SIZE - 1
    voxel_index = (
        x % CHUNK_SIZE + (z % CHUNK_SIZE) * CHUNK_SIZE + (y % CHUNK_SIZE) * CHUNK_AREA
    )

    # if the voxel is inside the chunk, then we check if it is empty or not
    voxel_id = chunk_voxels[voxel_index]
    return voxel_id == 0


# add vertex attributes to the vertex data array
@njit
def add_data(vertex_data, index, *vertices):
    for vertex in vertices:
        # vertex_data[index] = vertex
        # index += 1
        for attr in vertex:
            vertex_data[index] = attr
            index += 1
    return index


@njit
def build_chunk_mesh(chunk_voxels, format_size, chunk_pos, world_voxels):
    # the main idea of this function is that we need to form a chunk mesh
    # only from the voxel `faces` that are visible to the player

    # for voxels, we will only render their visible faces,
    # the maximum number of visible faces is 3.
    # but each face has 2 triangles, so we need 6 vertices per voxel,
    # so the maximum possible number of visible vertices for each voxel is 18.
    #
    # each vertex has 5 attributes: (= format_zize)
    # - x,y,z
    # - voxel_id
    # - face_id
    assert format_size == 5
    vertex_data = np.empty(CHUNK_VOL * 18 * format_size, dtype="uint8")
    index = 0

    for x in range(CHUNK_SIZE):
        for y in range(CHUNK_SIZE):
            for z in range(CHUNK_SIZE):
                voxel_id = chunk_voxels[x + CHUNK_SIZE * z + CHUNK_AREA * y]

                if not voxel_id:
                    continue

                # voxel world position
                cx, cy, cz = chunk_pos
                wx = cx * CHUNK_SIZE + x
                wy = cy * CHUNK_SIZE + y
                wz = cz * CHUNK_SIZE + z

                # since we only render the visible edges of the voxel, now we need
                # implement a function that will check if the edge is visible or not
                # the idea is quite simple,
                # for the top face, we check if the voxel above is empty or not, if it is empty, then the top face is visible
                # and accordingly, we will check the rest of the faces by performing similar check

                # top face
                if is_void((x, y + 1, z), (wx, wy + 1, wz), world_voxels):
                    # format : x,y,z, voxel_id, face_id  ( clockwise ?)
                    v0 = to_uint8(x, y + 1, z, voxel_id, 0)
                    v1 = to_uint8(x + 1, y + 1, z, voxel_id, 0)
                    v2 = to_uint8(x + 1, y + 1, z + 1, voxel_id, 0)
                    v3 = to_uint8(x, y + 1, z + 1, voxel_id, 0)

                    index = add_data(vertex_data, index, v0, v3, v2, v0, v2, v1)

                # bottom face
                if is_void((x, y - 1, z), (wx, wy - 1, wz), world_voxels):
                    v0 = to_uint8(x, y, z, voxel_id, 1)
                    v1 = to_uint8(x + 1, y, z, voxel_id, 1)
                    v2 = to_uint8(x + 1, y, z + 1, voxel_id, 1)
                    v3 = to_uint8(x, y, z + 1, voxel_id, 1)

                    index = add_data(vertex_data, index, v0, v2, v3, v0, v1, v2)

                # right face
                if is_void((x + 1, y, z), (wx + 1, wy, wz), world_voxels):
                    v0 = to_uint8(x + 1, y, z, voxel_id, 2)
                    v1 = to_uint8(x + 1, y + 1, z, voxel_id, 2)
                    v2 = to_uint8(x + 1, y + 1, z + 1, voxel_id, 2)
                    v3 = to_uint8(x + 1, y, z + 1, voxel_id, 2)

                    index = add_data(vertex_data, index, v0, v1, v2, v0, v2, v3)

                # left face
                if is_void((x - 1, y, z), (wx - 1, wy, wz), world_voxels):
                    v0 = to_uint8(x, y, z, voxel_id, 3)
                    v1 = to_uint8(x, y + 1, z, voxel_id, 3)
                    v2 = to_uint8(x, y + 1, z + 1, voxel_id, 3)
                    v3 = to_uint8(x, y, z + 1, voxel_id, 3)

                    index = add_data(vertex_data, index, v0, v2, v1, v0, v3, v2)

                # back face
                if is_void((x, y, z - 1), (wx, wy, wz - 1), world_voxels):
                    v0 = to_uint8(x, y, z, voxel_id, 4)
                    v1 = to_uint8(x, y + 1, z, voxel_id, 4)
                    v2 = to_uint8(x + 1, y + 1, z, voxel_id, 4)
                    v3 = to_uint8(x + 1, y, z, voxel_id, 4)

                    index = add_data(vertex_data, index, v0, v1, v2, v0, v2, v3)

                # front face
                if is_void((x, y, z + 1), (wx, wy, wz + 1), world_voxels):
                    v0 = to_uint8(x, y, z + 1, voxel_id, 5)
                    v1 = to_uint8(x, y + 1, z + 1, voxel_id, 5)
                    v2 = to_uint8(x + 1, y + 1, z + 1, voxel_id, 5)
                    v3 = to_uint8(x + 1, y, z + 1, voxel_id, 5)

                    index = add_data(vertex_data, index, v0, v2, v1, v0, v3, v2)

    # we should take the part of the array that contains only the vertices that we have filled
    return vertex_data[: index + 1]
