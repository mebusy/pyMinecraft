from settings import *


class ShaderProgram:
    def __init__(self, app):
        self.app = app
        self.ctx = app.ctx

        # --------create shader programs -------- #
        self.quad = self.get_program(shader_name="quad")

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
        pass

    # update uniform
    def update(self):
        pass
