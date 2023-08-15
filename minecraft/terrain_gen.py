from noise import noise2, noise3
from random import random
from settings import *
from settings import njit, CENTER_Y

# 2d nose can be used to generate height map
# 3d noise can be used to generate cave system


@njit
def get_height(x, z):
    # get the height map

    # amplitude
    a1 = CENTER_Y
    # do something like fractional Brownian motion
    a2, a4, a8 = a1 * 0.5, a1 * 0.25, a1 * 0.125

    # frequency
    f1 = 0.005
    f2, f4, f8 = f1 * 2, f1 * 4, f1 * 8

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

    return int(height)
