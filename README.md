# Creating a Voxel Engine (like Minecraft) from Scratch in Python

https://www.youtube.com/watch?v=Ab8TOSFfNp4


## libraries

- numpy 1.24+
- installation
    ```bash
    pip install pygame moderngl PyGLM numba
    ```

library | desc
--- | ---
modergl | a python wrapper over OpenGL 3.3+ core that simplifies the creation of simple graphics applications like scientific simulations, games or user interfaces. 
PyGLM | OpenGL Mathematics (GLM) library for Python, to fill in the programming gaps in writing the basic vector and matrix mathematics for OpenGL applications. <br> https://web.engr.oregonstate.edu/~mjb/cs491/Handouts/GLM.1pp.pdf
numba | JIT compiler that translates a subset of Python and NumPy code into fast machine code.


## branches

1. basicPygameWindow
2. meshRenderAndMoveInWorld
3. renderColorChunk



## concept

### voxel

- unit cube, 0 
- voxel id: 0-255
    - 0 means empty
    - all the rest are different types of voxels.

### chunks

- the space representation unit is a voxel (unit cube), but we will render the whole world using the so-called `chunks`, a 32x32x32 cube-shaped space filled with voxels.
- instead of 3d arrays, for performance purpose we will use 1D array, and we will receive array indices according to the formulat:
    - `idx = X + SIZE * Z + AREA * Y`  (right-hand ?)




