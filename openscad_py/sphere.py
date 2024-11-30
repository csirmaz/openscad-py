
from typing import Union as TUnion
from typing import List
import math

from openscad_py.point import Point
from openscad_py.object_ import Object


class Sphere(Object):
    """A 3D primitive, sphere.
    Creates a sphere at the origin of the coordinate system.
    
    See https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/The_OpenSCAD_Language#sphere
    """

    def __init__(self, r):
        self.r = r
        # $fa, $fs, $fn

    def render(self):
        """Render the object into OpenSCAD code"""
        return f"sphere(r={self.r});"


