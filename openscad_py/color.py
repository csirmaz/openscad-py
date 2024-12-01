
from typing import Union as TUnion
from typing import List
import math

from openscad_py.object_ import Object


class Color(Object):
    """Represents a color applied to an object.
    See https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Transformations#color
    """

    def __init__(self, child: Object, r: float, g: float, b: float, a: float = 1.):
        self.color = [r, g, b, a]
        self.child = child

    def render(self) -> str:
        """Render the object into OpenSCAD code"""
        return f"color(c=[{','.join([str(c) for c in self.color])}]){{ {self.child.render()} }}"

