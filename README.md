# Creating a Voxel Engine (like Minecraft) from Scratch in Python

https://www.youtube.com/watch?v=Ab8TOSFfNp4


## libraries

- numpy 1.24+
- installation
    ```bash
    pip install pygame moderngl PyGLM numba 
    ```
    - install opensimplex to allow numba compile world generation code
        ```bash
        pip install opensimplex
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
6. shading
7. packData
8. voxelMarker
9. frustumCulling


## TODO 

- occlusion culling
- use of appropriate data structures for efficient organization and rendering of chunks


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


### Anisotropy

- when applied Ambient Occlusion, since each face consists of two triangles, the interpolation of non-linear value along the face leads to an undesirable effect.
- to fix this, we need to choose a consistent orientation for the faces , when some condition is met, we flip the order of triangle vertices for each face, that is, choose another diagonal to split the sqaure into triangles.
    - but it will also cause our texture changing its orientation due to flipped faces.
    - if we want to continue using textures , then should eliminate this draw back, also apply flip on our texture uv map.


### interaction

- the main idea is that we emit Ray from the camera at a given distance, and if a voxel is found along the path of Ray, then we can remove it or add a new one.
- and with such action we have to rebuild the entire chunk mesh. 
- [A Fast Voxel Traversal Algorithm for Ray Tracing](http://www.cse.yorku.ca/~amana/research/grid.pdf)
    - a special case of the DDA algorithm, but only in relation to voxels.


### Frustum Culling

- is about reducing chunk draw calls, meaning we'll only render those chunks that are inside the player's View Frustum. 
- the most efficient way is for our chunk to create a bounding volume in the form of sphere.


### Texture Array

- a texture array is a kind of large texture that contains other textures of the same size.
    - each such texture is accessed by its layer number, and in our case, we will use the voxel id as an access.
- and the simplest thing you can think of is that each such texture will consist 3 parts (tiles)
    - the first part will apply to bottom face texturing,  the middle part will apply to the sides of voxel, and the last part will apply to top face.
- NOTE: the first row tiles are transparent ones
- <img src="minecraft/assets/tex_array_0.png" height=600 />


### Terrain Generation

- as with mesh creation, our world generation methods will also be compilable (numba ?)
- and therefore using noise function from the glm module is not suitable for us
    ```python
    # not suitable for us
    world_height = int(glm.simplex(glm.vec2(wx, wz) * 0.01) * 32 + 32)
    ```
    - since the numba compiler can only work with pure python or numpy.
- and in this case, we will use the OpenSimplex Noise module which is just written using python, and has the noise functions we need.


### Fog

- the fog effect is easy to implement in the fragment shader by calculating the approximate depth, using the `gl_FragCoord` variable.
    - and using this distance exponentially in the mix function for our sky color
    ```gsgl
    // .frag
    //fog
    float fog_dist = gl_FragCoord.z / gl_FragCoord.w;
    tex_col = mix(tex_col, bg_color, (1.0 - exp2(-0.00001 * fog_dist * fog_dist)));    
    ```

### Water

- in a very simple way in our world, we can create a water surface.
    - for this we use one quad but enlarge to the size of our world,
    - that is , all water has 2 polygons with a tiled water texture in a translucent color.
- in addition to water, we can implement an underwater effect
    - for this we need to know the world position of the fragment,  which we will calculate in the vertex shader
        ```gsgl
        // .vert
        frag_world_pos = (m_model * vec4(in_position, 1.0)).xyz; 
        ```
    - and in fragment shader, we will compare its y component with the value of the water line, and chage the color with watercolor
        ```gsgl
        // .frag
        // underwater effect
        if (frag_world_pos.y < water_line) tex_col *= vec3(0.0, 0.3, 1.0);
        ```

### Cloud

- not everything is so simple here
- to create them we form an array of 0s and 1s using 2D simplex noise for some Criterion and then create a polygonal mesh based on it
    - but with a naive approach , we will get inefficient clouds with a huge number of polygons, which can cause a drop in the performance of our engine, 
    - and so we have to come up with an algorithm to optimize this mesh it will turn out to be a kind of greedy mesh algorithm where we minimize the number of polygons in this mesh by merging them.

