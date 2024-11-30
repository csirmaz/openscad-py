
from typing import Union as TUnion
from typing import List
import math

from openscad_py.point import Point
from openscad_py.object_ import Object


class DeltaOffset(Object):
    """A new 2d interior or exterior outline from an existing outline
    
    See https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Transformations#offset
    """
    
    def __init__(self, delta, child: Object, chamfer: bool = False):
        self.delta = delta
        self.child = child
        self.chamfer = chamfer
        
    def render(self) -> str:
        """Render the object into OpenSCAD code"""
        return f"offset(delta={delta}, chamfer={'true' if self.chamfer else 'false'}){{\n{self.child.render()}\n}}"

