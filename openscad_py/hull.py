
from typing import Union as TUnion
from typing import List

from openscad_py.object_ import Object
from openscad_py.collection import Collection


class Hull(Object):
    """Represents the convex hull of an object (usually a collection of objects).
    See https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Transformations#hull
    """

    def __init__(self, child: TUnion[Object, list]):
        self.child = Collection.c(child)

    def render(self) -> str:
        """Render the object into OpenSCAD code"""
        return f"hull(){{ {self.child.render()} }}"


