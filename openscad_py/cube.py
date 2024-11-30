
from typing import Union as TUnion
from typing import List
import math
import numpy as np

from openscad_py.point import Point
from openscad_py.object_ import Object


class Cube(Object):
    """A 3D primitive, cube.
    Creates a cube in the first octant. When center is true, the cube is centered on the origin.
    
    See https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/The_OpenSCAD_Language#cube
    """

    def __init__(self, size: TUnion[list, Point], center: bool = False):
        self.size = Point.c(size)
        self.center = center

    def render(self):
        return f"cube(size={self.size.render()}, center={self._center()});"

