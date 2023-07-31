#version 330 core

layout (location = 0) out vec4 fragColor;

// here it is worth remembering that all actions with the texture
// should be carried out in linear color space.
// so we need to make a gamma color correction.
const vec3 gamma = vec3(2.2);
const vec3 inv_gamma = 1/gamma;


uniform sampler2D u_texture_0;

in vec3 voxel_color;
in vec2 uv;

void main() {
    // get the appropriate color from the texture
    vec3 tex_col = texture(u_texture_0, uv).rgb;

    tex_col = pow(tex_col, gamma);
    tex_col *= voxel_color;
    tex_col = pow(tex_col, inv_gamma);

    fragColor = vec4(tex_col, 1);
}

