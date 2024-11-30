
from typing import Union as TUnion
from typing import List
import math

from openscad_py.point import Point
from openscad_py.object_ import Object


class LinearExtrude(Object):
    """Represents a linear extrusion applied to an object.
    If center is false the linear extrusion Z range is from 0 to height; if it is true, the range is from -height/2 to height/2.
    """

    def __init__(self, height, child: Object, convexity: int = 10, center: bool = False):
        self.height = height
        self.child = child
        self.convexity = convexity
        self.center = center
        # twist, slices, scale (float/vector), $fn

    def render(self) -> str:
        """Render the object into OpenSCAD code"""
        return f"linear_extrude(height={self.height}, center={self._center()}, convexity={self.convexity}){{\n{self.child.render()}\n}}"


