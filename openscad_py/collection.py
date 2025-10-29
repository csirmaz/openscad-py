
from typing import Union as TUnion
from typing import List

from openscad_py.object_ import Object


class Collection(Object):
    """Represents a collection of objects"""

    def __init__(self, coll: list):
        self.collection = coll

    @classmethod
    def c(cls, coll: TUnion[list, Object, None]) -> Object:
        """Ensure the list of objects is a Collection (idempotent). If coll is None, return an empty collection."""
        if coll is None:
            return cls([])
        if isinstance(coll, Object):
            return coll
        return cls(coll)

    def _add(self, obj):
        return self.__class__(self.collection + [obj])

    def render(self) -> str:
        """Render the object into OpenSCAD code"""
        return "\n".join([o.render() for o in self.collection])

