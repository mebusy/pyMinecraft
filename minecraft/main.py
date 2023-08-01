#!python3

from settings import *
import moderngl as mgl
import pygame as pg
import sys

from shader_program import ShaderProgram
from scene import Scene

from player import Player

from textures import Textures


class VoxelEngine:
    def __init__(self):
        # initialize pygame
        pg.init()
        # use opengl 3.3
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(
            pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE
        )
        pg.display.gl_set_attribute(pg.GL_DEPTH_SIZE, 24)
        # pg.display.gl_set_attribute(pg.GL_MULTISAMPLESAMPLES, 1)  # antialiasing

        # set window resolution
        pg.display.set_mode(WIN_RES, flags=pg.DOUBLEBUF | pg.OPENGL)

        # create the openGL context itself
        self.ctx = mgl.create_context()
        # active fragment depth testing, culling and blending
        self.ctx.enable(mgl.DEPTH_TEST | mgl.CULL_FACE | mgl.BLEND)
        # enable automatic garbage collection of unused opengl objects (thx to mgl)
        self.ctx.gc_mode = "auto"

        # keep track of time
        self.clock = pg.time.Clock()
        self.delta_time: float = 0.0
        self.time: float = 0.0

        # lock mouse control inside the window
        pg.event.set_grab(True)
        # pg.mouse.set_visible(False)

        # a flag to check if the game is running
        self.is_running: bool = True

        self.on_init()

    def on_init(self):
        self.textures = Textures(self)
        self.player = Player(self)

        # create shader program
        self.shader_program = ShaderProgram(self)
        # create scene
        self.scene = Scene(self)

    # updating the state of objects
    def update(self):
        self.player.update()

        self.shader_program.update()
        self.scene.update()

        # update delta time
        # clock.tick() should be called once per frame. It will compute how many milliseconds have passed since the previous call.
        self.delta_time = self.clock.tick()
        # time.get_ticks() returns the number of milliseconds since pygame.init()
        self.time = pg.time.get_ticks() * 0.001

        # display fps in title
        pg.display.set_caption(f"FPS: {self.clock.get_fps():.0f}")

    # render game objects
    def render(self):
        # clear the frame and depth buffers
        self.ctx.clear(color=BG_COLOR)

        # new frame
        self.scene.render()

        # display new frame
        pg.display.flip()

    # handle events
    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (
                event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE
            ):
                self.is_running = False

    def run(self):
        # main loop
        while self.is_running:
            self.handle_events()
            self.update()
            self.render()

        # quit pygame
        pg.quit()
        # quit the program
        sys.exit()


if __name__ == "__main__":
    app = VoxelEngine()
    app.run()
