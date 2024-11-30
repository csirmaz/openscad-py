
from typing import Union as TUnion
from typing import List
import math

from openscad_py.object_ import Object


class Circle(Object):
    """A 2D primitive, circle.
    Creates a circle (or regular polygon) at the origin.
    
    See https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/The_OpenSCAD_Language#circle
    """

    def __init__(self, r: float, fn: TUnion[int, None] = None):
        self.r = r
        self.fn = fn
        # $fa, $fs, $fn

    @classmethod
    def triangle(cls, r):
        """Create a regular triangle"""
        return cls(r=r, fn=3)

    @classmethod
    def regular_polygon(cls, r, sides: int):
        """Create a regular polygon"""
        return cls(r=r, fn=sides)

    def render(self) -> str:
        fnstr = '' if self.fn is None else f", $fn={self.fn}"
        return f"circle(r={self.r}{fnstr});"


