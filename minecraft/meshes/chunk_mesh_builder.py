from settings import *
from settings import np, CHUNK_VOL, CHUNK_SIZE, CHUNK_AREA


def is_void(voxel_pos, chunk_voxels):
    x, y, z = voxel_pos
    # if the voxel is outside the chunk, then it is void
    if x < 0 or x >= CHUNK_SIZE or y < 0 or y >= CHUNK_SIZE or z < 0 or z >= CHUNK_SIZE:
        return True

    # if the voxel is inside the chunk, then we check if it is empty or not
    voxel_id = chunk_voxels[x + CHUNK_SIZE * z + CHUNK_AREA * y]
    return voxel_id == 0


# add vertex attributes to the vertex data array
def add_data(vertex_data, index, *vertices):
    for vertex in vertices:
        # vertex_data[index] = vertex
        # index += 1
        for attr in vertex:
            vertex_data[index] = attr
            index += 1
    return index


def build_chunk_mesh(chunk_voxels, format_size):
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
    vertex_data = np.empty(CHUNK_VOL * 18 * format_size, dtype=np.uint8)
    index = 0

    for x in range(CHUNK_SIZE):
        for y in range(CHUNK_SIZE):
            for z in range(CHUNK_SIZE):
                voxel_id = chunk_voxels[x + CHUNK_SIZE * z + CHUNK_AREA * y]

                if not voxel_id:
                    continue

                # since we only render the visible edges of the voxel, now we need
                # implement a function that will check if the edge is visible or not
                # the idea is quite simple,
                # for the top face, we check if the voxel above is empty or not, if it is empty, then the top face is visible
                # and accordingly, we will check the rest of the faces by performing similar check

                # top face
                if is_void((x, y + 1, z), chunk_voxels):
                    # format : x,y,z, voxel_id, face_id  ( clockwise ?)
                    v0 = (x, y + 1, z, voxel_id, 0)
                    v1 = (x + 1, y + 1, z, voxel_id, 0)
                    v2 = (x + 1, y + 1, z + 1, voxel_id, 0)
                    v3 = (x, y + 1, z + 1, voxel_id, 0)

                    index = add_data(vertex_data, index, v0, v3, v2, v0, v2, v1)

                # bottom face
                if is_void((x, y - 1, z), chunk_voxels):
                    v0 = (x, y, z, voxel_id, 1)
                    v1 = (x + 1, y, z, voxel_id, 1)
                    v2 = (x + 1, y, z + 1, voxel_id, 1)
                    v3 = (x, y, z + 1, voxel_id, 1)

                    index = add_data(vertex_data, index, v0, v2, v3, v0, v1, v2)

                # right face
                if is_void((x + 1, y, z), chunk_voxels):
                    v0 = (x + 1, y, z, voxel_id, 2)
                    v1 = (x + 1, y + 1, z, voxel_id, 2)
                    v2 = (x + 1, y + 1, z + 1, voxel_id, 2)
                    v3 = (x + 1, y, z + 1, voxel_id, 2)

                    index = add_data(vertex_data, index, v0, v1, v2, v0, v2, v3)

                # left face
                if is_void((x - 1, y, z), chunk_voxels):
                    v0 = (x, y, z, voxel_id, 3)
                    v1 = (x, y + 1, z, voxel_id, 3)
                    v2 = (x, y + 1, z + 1, voxel_id, 3)
                    v3 = (x, y, z + 1, voxel_id, 3)

                    index = add_data(vertex_data, index, v0, v2, v1, v0, v3, v2)

                # back face
                if is_void((x, y, z - 1), chunk_voxels):
                    v0 = (x, y, z, voxel_id, 4)
                    v1 = (x, y + 1, z, voxel_id, 4)
                    v2 = (x + 1, y + 1, z, voxel_id, 4)
                    v3 = (x + 1, y, z, voxel_id, 4)

                    index = add_data(vertex_data, index, v0, v1, v2, v0, v2, v3)

                # front face
                if is_void((x, y, z + 1), chunk_voxels):
                    v0 = (x, y, z + 1, voxel_id, 5)
                    v1 = (x, y + 1, z + 1, voxel_id, 5)
                    v2 = (x + 1, y + 1, z + 1, voxel_id, 5)
                    v3 = (x + 1, y, z + 1, voxel_id, 5)

                    index = add_data(vertex_data, index, v0, v2, v1, v0, v3, v2)

    # we should take the part of the array that contains only the vertices that we have filled
    return vertex_data[:index]
