
from typing import Union as TUnion
from typing import List
import math

from openscad_py.point import Point
from openscad_py.object_ import Object


class Scale(Object):

    def __init__(self, v: TUnion[list, Point, float, int], child: Object):
        if isinstance(v, float) or isinstance(v, int):
            v = [v, v, v]
        self.v = Point.c(v)
        self.child = child

    def render(self) -> str:
        return f"scale(v={self.v.render()}){{\n{self.child.render()}\n}}"


