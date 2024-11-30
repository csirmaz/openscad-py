
from typing import Union as TUnion
from typing import List
import math

from openscad_py.point import Point
from openscad_py.object_ import Object


class Rotate(Object):
    """Represents a rotation transformation applied to an object"""

    def __init__(self, a, v: TUnion[list, Point], child: Object):
        self.a = a
        self.v = Point.c(v)
        self.child = child

    def render(self) -> str:
        """Render the object into OpenSCAD code"""
        return f"rotate(a={self.a}, v={self.v.render()}){{\n{self.child.render()}\n}}"


