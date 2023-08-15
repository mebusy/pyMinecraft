from noise import noise2, noise3
from random import random
from settings import *
from settings import njit, CENTER_Y, STONE, SNOW, SNOW_LVL

# 2d nose can be used to generate height map
# 3d noise can be used to generate cave system


@njit
def get_height(x, z):
    # get the height map

    # improvment for the world boundary
    # we create a so-called Island mask using the following expression
    # island mask
    island = 1 / (pow(0.0025 * math.hypot(x - CENTER_XZ, z - CENTER_XZ), 20) + 0.0001)
    island = min(island, 1)

    # amplitude
    a1 = CENTER_Y
    # do something like fractional Brownian motion
    a2, a4, a8 = a1 * 0.5, a1 * 0.25, a1 * 0.125

    # frequency
    f1 = 0.005
    f2, f4, f8 = f1 * 2, f1 * 4, f1 * 8

    # create some kind of erosion effect
    if noise2(0.1 * x, 0.1 * z) < 0:
        a1 /= 1.07

    height = 0
    # height += noise2(x * f1, z * f1) * a1 + a1
    # height += noise2(x * f2, z * f2) * a2 - a2
    # height += noise2(x * f4, z * f4) * a4 + a4
    # height += noise2(x * f8, z * f8) * a8 - a8
    a_array = [a1, a2, a4, a8]
    f_array = [f1, f2, f4, f8]
    for i in range(4):
        height += noise2(x * f_array[i], z * f_array[i]) * a_array[i] + (
            a_array[i] if i & 1 == 0 else -a_array[i]
        )

    height = max(height, 1)
    height *= island

    # return int(island)
    return int(height)


@njit
def get_index(x, y, z):
    return x + CHUNK_SIZE * z + CHUNK_AREA * y


@njit
def set_voxel_id(voxels, x, y, z, wx, wy, wz, world_height):
    # takes an array of chunk voxels, local pos, world pos, and world height
    voxel_id = 0

    # let everything that is under the first voxel in height(vertically) always be a stone
    if wy < world_height - 1:
        voxel_id = STONE
    else:
        # and for a natural image let's add some randomness to the current height,
        # and using the given height levels for the textures.
        # we will determine the appropriate voxel id and then add it to the array
        rng = int(7 * random())
        ry = wy - rng
        if SNOW_LVL <= ry < world_height:
            voxel_id = SNOW
        elif STONE_LVL <= ry < SNOW_LVL:
            voxel_id = STONE
        elif DIRT_LVL <= ry < STONE_LVL:
            voxel_id = DIRT
        elif GRASS_LVL <= ry < DIRT_LVL:
            voxel_id = GRASS
        else:
            voxel_id = SAND

    # setting ID
    voxels[get_index(x, y, z)] = voxel_id
