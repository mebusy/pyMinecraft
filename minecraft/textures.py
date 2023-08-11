import pygame as pg
import moderngl as mgl


class Textures:
    def __init__(self, app):
        self.app = app
        self.ctx = app.ctx

        # load textures
        self.texture_0 = self.load("test.png")

        # having loaded the texture we need determine the number of the texture unit to work with it
        # assign texture unit
        self.texture_0.use(location=0)

    def load(self, file_name, is_tex_array=False):
        texture = pg.image.load(f"assets/{file_name}")
        # we should flip them horizontally because OpenGL expects the first pixel to be in the bottom-left corner
        # but, shouldn't it flip vertically?
        texture = pg.transform.flip(texture, flip_x=True, flip_y=False)

        # create texture object on GPU side
        texture = self.ctx.texture(
            size=texture.get_size(),
            components=4,
            data=pg.image.tostring(texture, "RGBA", False),
        )
        # anisotropy filtering value
        texture.anisotropy = 32.0
        # build mipmaps
        texture.build_mipmaps()
        # specify minification and magnification filters
        texture.filter = (mgl.NEAREST, mgl.NEAREST)

        return texture
