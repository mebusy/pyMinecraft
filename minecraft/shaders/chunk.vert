#version 330 core

// layout (location = 0) in ivec3 in_position;
// layout (location = 1) in int voxel_id;
// layout (location = 2) in int face_id;
// layout (location = 3) in int ao_id;
// layout (location = 4) in int flip_id;
layout (location = 0) in uint packed_data;  // after packing data

int x,y,z;
int ao_id;
int flip_id;


uniform mat4 m_proj;
uniform mat4 m_view;
uniform mat4 m_model;

// out vec3 voxel_color;
out vec2 uv;
out float shading;

out vec3 frag_world_pos;

// since they are integer, we need flat qualifier
flat out int voxel_id;
flat out int face_id;

const float ao_values[4] = float[4](
    0.1, 0.25, 0.5, 1.0
);

const float face_shading[6] = float[6](
    1.0, 0.5, // top bottom
    0.5, 0.8, // right left
    0.5, 0.8 // front back
);

// (0,1)  (1,1)
// (0,0)  (1,0)
// 1 3
// 0 2
const vec2 uv_coords[4] = vec2[4](
    vec2(0, 0), vec2(0, 1),
    vec2(1, 0), vec2(1, 1)
);


// array of 12 numbers that correspond to the indices from the array of texture coordinates
// this is where our face ID value comes in handy
// and by the way, the face_id attribute will come in handy for lighting later on
// 
// for example, top face (even)vertex index are:
// # v0 v1 (even)
// # v3 v2
//   2 triangles composed by  (v0, v3, v2), (v0, v2, v1) 
//   so the uv indices should be  (1,0,2), (1,2,3)
// the bottom face (odd) triangles: (v0, v2, v3), (v0, v1, v2), but to keep orientation consistant 
//   with the even face, we also want to flip the texture horizontally, to 
//   3 1  (flipped uv_coord index)
//   2 0
//   so the uv indices should be  (3,0,2), (3,1,0)
//
// FLIPPED 
// flipped top face (even): (v1, v0, v3), (v1, v3, v2)
//   uv indices should be 
const int uv_indices[24] = int[24](
    1, 0, 2, 1, 2, 3,  // tex coords indices for vertices of an even face
    3, 0, 2, 3, 1, 0,  // odd face
    // expand our array of texture coordinates to handle flip_id
    3, 1, 0, 3, 0, 2,  // even flipped face
    1, 2, 3, 1, 0, 2   // odd flipped face
);


vec3 hash31(float p) {
    vec3 p3 = fract(vec3(p * 21.2) * vec3(0.1031, 0.1030, 0.0973));
    p3 += dot(p3, p3.yzx + 33.33);
    return fract((p3.xxy + p3.yzz) * p3.zyx) + 0.05;
}

void unpack(uint packed_data) {
    // a, b, c, d, e, f, g = x, y, z, voxel_id, face_id, ao_id, flip_id
    uint b_bit = 6u, c_bit = 6u, d_bit = 8u, e_bit = 3u, f_bit = 2u, g_bit = 1u;
    uint b_mask = 63u, c_mask = 63u, d_mask = 255u, e_mask = 7u, f_mask = 3u, g_mask = 1u;
    //
    uint fg_bit = f_bit + g_bit;
    uint efg_bit = e_bit + fg_bit;
    uint defg_bit = d_bit + efg_bit;
    uint cdefg_bit = c_bit + defg_bit;
    uint bcdefg_bit = b_bit + cdefg_bit;
    // unpacking vertex data
    x = int(packed_data >> bcdefg_bit);
    y = int((packed_data >> cdefg_bit) & b_mask);
    z = int((packed_data >> defg_bit) & c_mask);
    //
    voxel_id = int((packed_data >> efg_bit) & d_mask);
    face_id = int((packed_data >> fg_bit) & e_mask);
    ao_id = int((packed_data >> g_bit) & f_mask);
    flip_id = int(packed_data & g_mask);
}



void main() {
    unpack(packed_data);
    vec3 in_position = vec3(x, y, z);

    // voxel_color = vec3(float(voxel_id)/93.0); // debug
    // voxel_color = hash31(voxel_id);

    // each face has 2 triangles,  
    // `gl_VertexID % 6` always get the ordinal number of the vertex
    // `(face_id & 1)` checking whether the face_id is even or odd
    // to get the necessary index position for vertex in this array of indicies
    int uv_index = gl_VertexID % 6 + ((face_id & 1) + flip_id*2) * 6;
    uv = uv_coords[ uv_indices[uv_index] ];

    shading = face_shading[face_id] * ao_values[ao_id];

    // gl_Position = m_proj * m_view * m_model * vec4(in_position, 1.0);
    frag_world_pos = (m_model * vec4(in_position, 1.0)).xyz;
    gl_Position = m_proj * m_view * vec4(frag_world_pos, 1.0);
}

