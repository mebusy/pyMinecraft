from settings import *
from settings import glm


class ShaderProgram:
    def __init__(self, app):
        self.app = app
        self.ctx = self.app.ctx

        self.player = self.app.player

        # --------create shader programs -------- #
        self.chunk = self.get_program(shader_name="chunk")

        # ------------------------- #
        self.set_uniforms_on_init()

    def get_program(self, shader_name):
        # load shader
        with open(f"shaders/{shader_name}.vert") as file:
            vertex_shader = file.read()
        with open(f"shaders/{shader_name}.frag") as file:
            fragment_shader = file.read()

        # create shader program
        program = self.ctx.program(
            vertex_shader=vertex_shader, fragment_shader=fragment_shader
        )
        return program

    # set uniform
    def set_uniforms_on_init(self):
        self.chunk["m_proj"].write(self.player.m_proj)
        self.chunk["m_model"].write(glm.mat4())

    # update uniform
    def update(self):
        self.chunk["m_view"].write(self.player.m_view)
