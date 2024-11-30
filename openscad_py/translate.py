
from typing import Union as TUnion
from typing import List
import math

from openscad_py.point import Point
from openscad_py.object_ import Object


class Translate(Object):
    """Represents a translation transformation applied to an object"""

    def __init__(self, v: TUnion[list, Point], child: Object):
        self.v = Point.c(v)
        self.child = child

    def render(self) -> str:
        return f"translate(v={self.v.render()}){{\n{self.child.render()}\n}}"
    