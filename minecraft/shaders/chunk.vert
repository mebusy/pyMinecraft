#version 330 core

layout (location = 0) in ivec3 in_position;
layout (location = 1) in int voxel_id;
layout (location = 2) in int face_id;

uniform mat4 m_proj;
uniform mat4 m_view;
uniform mat4 m_model;

out vec3 voxel_color;
out vec2 uv;

// (0,0) is bottom left
const vec2 uv_coords[4] = vec2[4](
    vec2(0, 0), vec2(0, 1),
    vec2(1, 0), vec2(1, 1)
);

// array of 12 numbers that correspond to the indices from the array of texture coordinates
// this is where our face ID value comes in handy
const int uv_indices[12] = int[12](
    1, 0, 2, 1, 2, 3,  // tex coords indices for vertices of an even face
    3, 0, 2, 3, 1, 0  // odd face
);


vec3 hash31(float p) {
    vec3 p3 = fract(vec3(p * 21.2) * vec3(0.1031, 0.1030, 0.0973));
    p3 += dot(p3, p3.yzx + 33.33);
    return fract((p3.xxy + p3.yzz) * p3.zyx) + 0.05;
}

void main() {
    // debug
    // voxel_color = vec3(float(voxel_id)/93.0);
    // voxel_color = hash31(voxel_id);

    // each face has 2 triangles,  
    // `gl_VertexID % 6` always get the ordinal number of the vertex
    // `(face_id & 1)` checking whether the face_id is even or odd
    // to get the necessary index position for vertex in this array of indicies
    int uv_index = gl_VertexID % 6 + (face_id & 1) * 6;
    uv = uv_coords[ uv_indices[uv_index] ];

    gl_Position = m_proj * m_view * m_model * vec4(in_position, 1.0);
}

