
from typing import Union as TUnion
from typing import List
import math

from openscad_py.point import Point
from openscad_py.object_ import Object


class RotateExtrude(Object):
    """Represents a rotational extrusion of a (2D) object.
    For all points, x>=0 must hold.

    See https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/2D_to_3D_Extrusion
    """

    def __init__(self, angle, child: Object, convexity: int = 10):
        self.angle = angle
        self.child = child
        self.convexity = convexity
        # $fa, $fs, $fn

    def render(self) -> str:
        return f"rotate_extrude(angle={self.angle}, convexity={self.convexity}) {{\n{self.child.render()}\n}}"
    

