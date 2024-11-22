import random
import typing


class Tile:
    walk_speed_factor = 1.0


class DirtTile(Tile):
    pass


class SwampTile(Tile):
    walk_speed_factor = 0.6


class Map:
    def __init__(self, size_x: int, size_y: int):
        self.tile_map: list[list[Tile]] = self._generate_tile_map(size_x, size_y)
        self.topography: list[list[float]] = self._generate_topography(size_x, size_y)

    def _generate_tile_map(
        self,
        size_x: int,
        size_y: int,
    ) -> list[list[typing.Any]]:
        tile_generator = lambda: random.choice(Tile.__subclasses__())
        return self._generate_random_grid(tile_generator, size_x, size_y)

    def _generate_topography(
        self,
        size_x: int,
        size_y: int,
        min: float = 0.0,
        max: float = 1.0,
    ) -> list[list[float]]:
        float_generator = lambda: (max - min) * random.random() + min
        return self._generate_random_grid(float_generator, size_x, size_y)

    def _generate_random_grid(
        self, generator_func: callable, size_x: int, size_y: int
    ) -> list[list[typing.Any]]:
        return [[generator_func() for _ in range(size_x)] for _ in range(size_y)]


class World:
    def __init__(self, width: int, length: int):
        self.width = width
        self.length = length
        self.map: Map | None = Map(width, length)
