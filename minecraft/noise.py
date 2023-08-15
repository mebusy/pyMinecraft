from settings import SEED
from numba import njit
from opensimplex.internals import (
    _noise2,
    _noise3,
    _init,
)  # 2d noise, 3d noise, initialization function


# according to the seed value, the necessary variables for the noise function are initialized
perm, perm_grad_index3 = _init(seed=SEED)


# we will re-define these noise function to make them compilable with numba,
# this approach was chosen to directly use the noise function, and not create an instance of the opensimplex class


@njit(cache=True)
def noise2(x, y):
    return _noise2(x, y, perm)


@njit(cache=True)
def noise3(x, y, z):
    return _noise3(x, y, z, perm, perm_grad_index3)
