
from typing import Union as TUnion
from typing import List
import math

from openscad_py.point import Point
from openscad_py.object_ import Object


class Cylinder(Object):
    """A 3D primitive, cylinder.
    Creates a cylinder or cone centered about the z axis. When center is true, it is also centered vertically along the z axis.
    
    See https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/The_OpenSCAD_Language#cylinder
    """

    def __init__(self, h, r=None, r1=None, r2=None, center: bool = False):
        self.height = h
        self.r1 = r if r1 is None else r1
        self.r2 = r if r2 is None else r2
        self.center = center
        # $fa, $fs, $fn

    def render(self):
        return f"cylinder(h={self.height}, r1={self.r1}, r2={self.r2}, center={self._center()});"

    @classmethod
    def from_ends(cls, radius: float, p1: TUnion[list, Point], p2: TUnion[list, Point]) -> Object:
        """Construct a cylinder between two points"""
        p1 = Point.c(p1)
        p2 = Point.c(p2)
        v = p2.sub(p1)
        length = v.length()
        assert length != 0
        z = Point([0, 0, 1])
        r = z.cross(v)
        rangle = v.angle(z)
        if r.length() == 0:
            # The cylinder is in the Z direction
            if abs(abs(rangle) - 180.) < .1:
                p1 = p2
            rangle = 0
            r = z
        else:
            r = r.norm()
        return cls(h=length, r=radius, center=False).rotate(a=rangle, v=r).move(p1)

