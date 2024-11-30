
from typing import Union as TUnion
from typing import List
import math

from openscad_py.point import Point
from openscad_py.object_ import Object
from openscad_py.collection import Collection


class Union(Object):
    """Represents a union applied to an object (usually a collection of objects)"""

    def __init__(self, child: TUnion[Object, list]):
        self.child = Collection.c(child)

    def render(self) -> str:
        """Render the object into OpenSCAD code"""
        return f"union(){{ {self.child.render()} }}"

    def union(self, objects: TUnion[list, Object]) -> Object:
        return self.__class__(self.child._add(objects))


