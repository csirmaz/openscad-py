
from typing import Union as TUnion
from typing import List
import math

from openscad_py.object_ import Object
from openscad_py.collection import Collection


class Difference(Object):
    """Represents a difference"""

    def __init__(self, subject: Object, tool: TUnion[list, Object]):
        self.subject = subject
        self.tool = Collection.c(tool)  # what to remove

    def render(self) -> str:
        """Render the object into OpenSCAD code"""
        return f"difference(){{ {self.subject.render()}\n{self.tool.render()} }}"

