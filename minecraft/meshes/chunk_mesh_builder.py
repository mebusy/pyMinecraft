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


# get the ambient occlusion value of the vertices of the faces that we are rendering
@njit
def get_ao(local_pos, world_pos, world_voxels, plane):
    x, y, z = local_pos
    wx, wy, wz = world_pos

    # for example, if we are rendering the top face, then we need to check the ambient occlusion of the vertices of the top face
    # then first we need to determine the presense of 8 voxels located in the same plane (note: this plane is not the same plane of the testing voxel).

    # for this, we will use the `plane` flag,  and the further code will be valid for the top and bottom faces since they belongs to the Y plane
    if plane == "Y":
        a = is_void((x, y, z - 1), (wx, wy, wz - 1), world_voxels)
        b = is_void((x - 1, y, z - 1), (wx - 1, wy, wz - 1), world_voxels)
        c = is_void((x - 1, y, z), (wx - 1, wy, wz), world_voxels)
        d = is_void((x - 1, y, z + 1), (wx - 1, wy, wz + 1), world_voxels)
        e = is_void((x, y, z + 1), (wx, wy, wz + 1), world_voxels)
        f = is_void((x + 1, y, z + 1), (wx + 1, wy, wz + 1), world_voxels)
        g = is_void((x + 1, y, z), (wx + 1, wy, wz), world_voxels)
        h = is_void((x + 1, y, z - 1), (wx + 1, wy, wz - 1), world_voxels)
    elif plane == "X":
        a = is_void((x, y, z - 1), (wx, wy, wz - 1), world_voxels)
        b = is_void((x, y - 1, z - 1), (wx, wy - 1, wz - 1), world_voxels)
        c = is_void((x, y - 1, z), (wx, wy - 1, wz), world_voxels)
        d = is_void((x, y - 1, z + 1), (wx, wy - 1, wz + 1), world_voxels)
        e = is_void((x, y, z + 1), (wx, wy, wz + 1), world_voxels)
        f = is_void((x, y + 1, z + 1), (wx, wy + 1, wz + 1), world_voxels)
        g = is_void((x, y + 1, z), (wx, wy + 1, wz), world_voxels)
        h = is_void((x, y + 1, z - 1), (wx, wy + 1, wz - 1), world_voxels)
    else:  # Z plane
        a = is_void((x - 1, y, z), (wx - 1, wy, wz), world_voxels)
        b = is_void((x - 1, y - 1, z), (wx - 1, wy - 1, wz), world_voxels)
        c = is_void((x, y - 1, z), (wx, wy - 1, wz), world_voxels)
        d = is_void((x + 1, y - 1, z), (wx + 1, wy - 1, wz), world_voxels)
        e = is_void((x + 1, y, z), (wx + 1, wy, wz), world_voxels)
        f = is_void((x + 1, y + 1, z), (wx + 1, wy + 1, wz), world_voxels)
        g = is_void((x, y + 1, z), (wx, wy + 1, wz), world_voxels)
        h = is_void((x - 1, y + 1, z), (wx - 1, wy + 1, wz), world_voxels)

    """
    ⎡_b_|_a__|_h_⎤
    ⎢ c |0  1| g ⎥
    ⎢___|3__2|___⎥
    ⎣ d | e  | f ⎦
    """

    ao = (a + b + c), (g + h + a), (e + f + g), (c + d + e)
    return ao


@njit
def pack_data(x, y, z, voxel_id, face_id, ao_id, flip_id):
    # x,y,z 6 bits each, voxel_id 8 bits, face_id 3 bits, ao_id 2 bits, flip_id 1 bit
    vars = [x, y, z, voxel_id, face_id, ao_id, flip_id]
    bits = [6, 6, 6, 8, 3, 2, 1]

    # pack all data into a single 32 bit integer, from right to left
    data = 0
    for i in range(len(vars)):
        data |= vars[i] << sum(bits[i + 1 :])

    return data




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
        vertex_data[index] = vertex
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
    # each vertex has 7 attributes: (= format_zize)
    # - x,y,z
    # - voxel_id
    # - face_id
    # - ao_id
    # - flip_id
    vertex_data = np.empty(CHUNK_VOL * 18 * format_size, dtype="uint32")
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
                    # get ao value
                    ao = get_ao(
                        (x, y + 1, z), (wx, wy + 1, wz), world_voxels, plane="Y"
                    )
                    # fix anisotropy, just choose a consistent direction for the faces
                    flip_id = ao[1] + ao[3] > ao[0] + ao[2]

                    # format : x,y,z, voxel_id, face_id  ( clockwise ?), ao_id, flip_id
                    v0 = pack_data(x, y + 1, z, voxel_id, 0, ao[0], flip_id)
                    v1 = pack_data(x + 1, y + 1, z, voxel_id, 0, ao[1], flip_id)
                    v2 = pack_data(x + 1, y + 1, z + 1, voxel_id, 0, ao[2], flip_id)
                    v3 = pack_data(x, y + 1, z + 1, voxel_id, 0, ao[3], flip_id)

                    # 0 1
                    # 3 2

                    if flip_id:
                        # flip the order of triangles vertices for each face, / diagonal
                        index = add_data(vertex_data, index, v1, v0, v3, v1, v3, v2)
                    else:
                        # start from vertex index 0   \ diagonal
                        index = add_data(vertex_data, index, v0, v3, v2, v0, v2, v1)
                        pass

                # continue # DEBUG

                # bottom face
                if is_void((x, y - 1, z), (wx, wy - 1, wz), world_voxels):
                    ao = get_ao(
                        (x, y - 1, z), (wx, wy - 1, wz), world_voxels, plane="Y"
                    )

                    flip_id = ao[1] + ao[3] > ao[0] + ao[2]

                    # odd face, because the visible face is from downside, so the triangle made by clockwise
                    # 0 1
                    # 3 2

                    v0 = pack_data(x, y, z, voxel_id, 1, ao[0], flip_id)
                    v1 = pack_data(x + 1, y, z, voxel_id, 1, ao[1], flip_id)
                    v2 = pack_data(x + 1, y, z + 1, voxel_id, 1, ao[2], flip_id)
                    v3 = pack_data(x, y, z + 1, voxel_id, 1, ao[3], flip_id)

                    if flip_id:
                        index = add_data(vertex_data, index, v1, v3, v0, v1, v2, v3)
                    else:
                        index = add_data(vertex_data, index, v0, v2, v3, v0, v1, v2)

                # right face
                if is_void((x + 1, y, z), (wx + 1, wy, wz), world_voxels):
                    ao = get_ao(
                        (x + 1, y, z), (wx + 1, wy, wz), world_voxels, plane="X"
                    )

                    flip_id = ao[1] + ao[3] > ao[0] + ao[2]

                    v0 = pack_data(x + 1, y, z, voxel_id, 2, ao[0], flip_id)
                    v1 = pack_data(x + 1, y + 1, z, voxel_id, 2, ao[1], flip_id)
                    v2 = pack_data(x + 1, y + 1, z + 1, voxel_id, 2, ao[2], flip_id)
                    v3 = pack_data(x + 1, y, z + 1, voxel_id, 2, ao[3], flip_id)

                    # 2 1
                    # 3 0

                    if flip_id:
                        index = add_data(vertex_data, index, v3, v0, v1, v3, v1, v2)
                    else:
                        index = add_data(vertex_data, index, v0, v1, v2, v0, v2, v3)

                # left face
                if is_void((x - 1, y, z), (wx - 1, wy, wz), world_voxels):
                    ao = get_ao(
                        (x - 1, y, z), (wx - 1, wy, wz), world_voxels, plane="X"
                    )

                    flip_id = ao[1] + ao[3] > ao[0] + ao[2]

                    v0 = pack_data(x, y, z, voxel_id, 3, ao[0], flip_id)
                    v1 = pack_data(x, y + 1, z, voxel_id, 3, ao[1], flip_id)
                    v2 = pack_data(x, y + 1, z + 1, voxel_id, 3, ao[2], flip_id)
                    v3 = pack_data(x, y, z + 1, voxel_id, 3, ao[3], flip_id)

                    # right face, the triangle made by clockwise
                    # 2 1
                    # 3 0

                    if flip_id:
                        index = add_data(vertex_data, index, v3, v1, v0, v3, v2, v1)
                    else:
                        index = add_data(vertex_data, index, v0, v2, v1, v0, v3, v2)

                # back face
                if is_void((x, y, z - 1), (wx, wy, wz - 1), world_voxels):
                    ao = get_ao(
                        (x, y, z - 1), (wx, wy, wz - 1), world_voxels, plane="Z"
                    )

                    flip_id = ao[1] + ao[3] > ao[0] + ao[2]

                    v0 = pack_data(x, y, z, voxel_id, 4, ao[0], flip_id)
                    v1 = pack_data(x, y + 1, z, voxel_id, 4, ao[1], flip_id)
                    v2 = pack_data(x + 1, y + 1, z, voxel_id, 4, ao[2], flip_id)
                    v3 = pack_data(x + 1, y, z, voxel_id, 4, ao[3], flip_id)

                    # 1 2
                    # 0 3
                    # made by clockwise

                    if flip_id:
                        index = add_data(vertex_data, index, v3, v0, v1, v3, v1, v2)
                    else:
                        index = add_data(vertex_data, index, v0, v1, v2, v0, v2, v3)

                # front face
                if is_void((x, y, z + 1), (wx, wy, wz + 1), world_voxels):
                    ao = get_ao(
                        (x, y, z + 1), (wx, wy, wz + 1), world_voxels, plane="Z"
                    )

                    flip_id = ao[1] + ao[3] > ao[0] + ao[2]

                    v0 = pack_data(x, y, z + 1, voxel_id, 5, ao[0], flip_id)
                    v1 = pack_data(x, y + 1, z + 1, voxel_id, 5, ao[1], flip_id)
                    v2 = pack_data(x + 1, y + 1, z + 1, voxel_id, 5, ao[2], flip_id)
                    v3 = pack_data(x + 1, y, z + 1, voxel_id, 5, ao[3], flip_id)

                    # 1 2
                    # 0 3

                    if flip_id:
                        index = add_data(vertex_data, index, v3, v1, v0, v3, v2, v1)
                    else:
                        index = add_data(vertex_data, index, v0, v2, v1, v0, v3, v2)

    # we should take the part of the array that contains only the vertices that we have filled
    return vertex_data[: index + 1]
