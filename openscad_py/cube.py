
from typing import Union as TUnion
from typing import List
import math
import numpy as np

from openscad_py.point import Point
from openscad_py.object_ import Object


class Cube(Object):
    """A 3D primitive, cube.

    See https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/The_OpenSCAD_Language#cube
    """

    def __init__(self, size: TUnion[list, Point], center: bool = False):
        """
        Creates a cube in the first octant. When `center` is True, the cube is centered on the origin.

        Arguments:
            - size: a Point object or a list of `x, y, z` sizes
            - center: if True, the cube is centered on the origin
        """
        self.size = Point.c(size)
        self.center = center

    def render(self):
        """Render the object into OpenSCAD code"""
        return f"cube(size={self.size.render()}, center={self._center()});"

