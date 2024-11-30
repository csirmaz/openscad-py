
from typing import Union as TUnion
from typing import List
import math

from openscad_py.point import Point
from openscad_py.object_ import Object


class RadialOffset(Object):
    """A new 2d interior or exterior outline from an existing outline
    
    See https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Transformations#offset
    """

    def __init__(self, r, child: Object):
        self.r = r
        self.child = child
        # $fa, $fs, and $fn

    def render(self) -> str:
        return f"offset(r={self.r}){{\n{self.child.render()}\n}}"


