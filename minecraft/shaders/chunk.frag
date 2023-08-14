#version 330 core

layout (location = 0) out vec4 fragColor;

// here it is worth remembering that all actions with the texture
// should be carried out in linear color space.
// so we need to make a gamma color correction.
const vec3 gamma = vec3(2.2);
const vec3 inv_gamma = 1/gamma;


// uniform sampler2D u_texture_0;
uniform sampler2DArray u_texture_array_0;

in vec3 voxel_color;
in vec2 uv;
in float shading;

flat in int voxel_id;
flat in int face_id;


void main() {
    // we need to remember, when loading the texture, we flip it horizontally,
    // so for texture coordinates it is also directed to the left ( 0,0 is at right bottom )
    vec2 face_uv = uv;
    face_uv.x = uv.x / 3.0 - min(face_id, 2) / 3.0;

    // get the appropriate color from the texture
    // vec3 tex_col = texture(u_texture_0, uv).rgb;
    vec3 tex_col = texture(u_texture_array_0, vec3(face_uv, voxel_id)).rgb;

    tex_col = pow(tex_col, gamma);

    // tex_col.rgb *= voxel_color;
    // tex_col = tex_col * 0.001 + vec3(1);

    tex_col *= shading;

    tex_col = pow(tex_col, inv_gamma);

    fragColor = vec4(tex_col, 1);
}

