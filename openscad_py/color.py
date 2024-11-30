
from typing import Union as TUnion
from typing import List
import math

from openscad_py.object_ import Object


class Color(Object):

    def __init__(self, child: Object, r, g, b, a=1.):
        self.color = [r, g, b, a]
        self.child = child

    def render(self) -> str:
        return f"color(c=[{','.join([str(c) for c in self.color])}]){{ {self.child.render()} }}"


