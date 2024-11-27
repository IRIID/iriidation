# /// script
# dependencies = [
#  "glcontext",
#  "moderngl",
# ]
# ///
import asyncio
import ctypes
import sys

import moderngl
import pygame as pg
from game_objects.player import Player
from game_objects.world import World

pg.init()
pg.display.set_caption("IRIID")
window = pg.display.set_mode((640, 640), pg.OPENGL | pg.DOUBLEBUF)

gl_context = moderngl.create_context()
gl_context.enable(moderngl.BLEND)

clock = pg.time.Clock()

vertex_shader_sprite = """
#version 330

in vec2 in_position;
in vec2 in_uv;
out vec2 v_uv;

void main() {
    v_uv = in_uv;
    gl_Position = vec4(in_position, 0.0, 1.0);
}
"""

fragment_shader_1 = """
#version 330

uniform sampler2D u_texture;

in vec2 v_uv;
out vec4 fragColour;

void main() {
    fragColour = vec4(texture(u_texture, v_uv).rg, texture(u_texture, v_uv).b * 0.5, 1.0);
}
"""

fragment_shader_2 = """
#version 330

uniform sampler2D u_texture;

in vec2 v_uv;
out vec4 fragColour;

void main() {
    fragColour = vec4(texture(u_texture, v_uv).r * 0.5, texture(u_texture, v_uv).gb, 1.0);
}
"""


class MGLGroup(pg.sprite.Group):
    def __init__(self, context, fragment_shader, sprites=None):
        if sprites is None:
            super().__init__()
        else:
            super().__init__(sprites)

        self.fragment_shader = fragment_shader
        self.gl_context = context
        self.gl_program = None
        self.gl_buffer = None
        self.gl_vao = None
        self.gl_textures = {}

    def get_program(self):
        if self.gl_program is None:
            self.gl_program = self.gl_context.program(
                vertex_shader=vertex_shader_sprite,
                fragment_shader=self.fragment_shader,
            )
        return self.gl_program

    def get_buffer(self):
        if self.gl_buffer is None:
            self.gl_buffer = self.gl_context.buffer(None, reserve=6 * 4 * 4)
        return self.gl_buffer

    def get_vao(self):
        if self.gl_vao is None:
            self.gl_vao = self.gl_context.vertex_array(
                self.get_program(),
                [(self.get_buffer(), "2f4 2f4", "in_position", "in_uv")],
            )
        return self.gl_vao

    def get_texture(self, image):
        if image not in self.gl_textures:
            rgba_image = image.convert_alpha()
            texture = self.gl_context.texture(
                rgba_image.get_size(), 4, rgba_image.get_buffer()
            )
            texture.swizzle = "BGRA"
            self.gl_textures[image] = texture
        return self.gl_textures[image]

    def _convert_vertex(pt, surface):
        return pt[0] / surface.get_width() * 2 - 1, 1 - pt[1] / surface.get_height() * 2

    def render(self, sprite, surface):
        corners = [
            MGLGroup._convert_vertex(sprite.rect.bottomleft, surface),
            MGLGroup._convert_vertex(sprite.rect.bottomright, surface),
            MGLGroup._convert_vertex(sprite.rect.topright, surface),
            MGLGroup._convert_vertex(sprite.rect.topleft, surface),
        ]
        vertices_quad_2d = (ctypes.c_float * (6 * 4))(
            *corners[0],
            0.0,
            1.0,
            *corners[1],
            1.0,
            1.0,
            *corners[2],
            1.0,
            0.0,
            *corners[0],
            0.0,
            1.0,
            *corners[2],
            1.0,
            0.0,
            *corners[3],
            0.0,
            0.0
        )
        self.get_buffer().write(vertices_quad_2d)
        self.get_texture(sprite.image).use(0)
        self.get_vao().render()

    def draw(self, surface):
        for sprite in self:
            self.render(sprite, surface)


async def main():
    world = World(tiles_x=100, tiles_y=100)
    player = Player()

    group_1 = MGLGroup(
        context=gl_context,
        fragment_shader=fragment_shader_1,
        sprites=world,
    )
    group_2 = MGLGroup(
        context=gl_context,
        fragment_shader=fragment_shader_2,
        sprites=player,
    )

    while True:
        await asyncio.sleep(0)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        group_1.update()
        group_2.update()

        gl_context.clear()
        group_1.draw(window)
        group_2.draw(window)

        pg.display.flip()

        clock.tick(60)


asyncio.run(main())
