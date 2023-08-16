#version 330 core

layout (location = 0) in vec2 in_tex_coord;
layout (location = 1) in vec3 in_position;

uniform mat4 m_proj;
uniform mat4 m_view;

uniform int water_area;
uniform float water_line;

out vec2 uv;


void main() {
    // in_position is always 2 fixed trangles on xz plane
    //   [(0, 0, 0), (1, 0, 1), (1, 0, 0), (0, 0, 0), (0, 0, 1), (1, 0, 1)],
    vec3 pos = in_position;
    pos.xz *= water_area;  // expand to whole world
    // pos.xz -= 0.5 * water_area;   // origin fix

    pos.y += water_line;
    uv = in_tex_coord * water_area;
    gl_Position = m_proj * m_view * vec4(pos, 1.0);
}