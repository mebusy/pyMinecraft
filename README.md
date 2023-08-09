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
4. textureAndNoise
5. removeChunkBoundaryMesh




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




## Misc

### Ambient Occlusion

- visual effect that adds depth to voxels by making the intersections between voxels darker, mimicking how light interacts with corners in the real world.
- minecraft like: https://0fps.net/2013/07/03/ambient-occlusion-for-minecraft-like-worlds/
    - as far as voxels are concerned, there is a fairly way to calculate ambient occlusion. 
    - the general idea is to calculate ambient occlusion for each vertex using only information from adjacent voxels, 
        - and for each vertex depending on these voxels there are only 4 possible variants of ambient occlusion.
        - <img src="https://0fps.files.wordpress.com/2013/07/aovoxel2.png" height=400/>
