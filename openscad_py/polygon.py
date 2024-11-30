
from typing import Union as TUnion
from typing import List
import math

from openscad_py.point import Point
from openscad_py.object_ import Object


class Polygon(Object):
    """A 2D primitive, polygon. Use points/lists with 2 coordinates."""

    def __init__(self, points, paths=None, convexity=10):
        assert paths is None  # not implemented yet
        self.points = [Point.c(p) for p in points]
        self.convexity = convexity

    def render(self) -> str:
        return f"polygon(points=[{','.join([p.render() for p in self.points])}], convexity={self.convexity});"

