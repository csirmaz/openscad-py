
from typing import Union as TUnion
from typing import List
import math

from openscad_py.point import Point


class Object:
    """Abstract class for an SCAD object"""

    def _center(self) -> str:
        return ('true' if self.center else 'false')

    def _add(self, obj):
        """Add an object, forming a collection"""
        from openscad_py.collection import Collection
        return Collection([self, obj])

    def render(self) -> str:
        """Render the object into OpenSCAD code"""
        raise Exception("abstract method")

    def translate(self, v: TUnion[list, Point]) -> 'Object':
        """Apply a translation"""
        from openscad_py.translate import Translate
        return Translate(v=v, child=self)

    def move(self, v: TUnion[list, Point]) -> 'Object':
        """Apply a translation"""
        from openscad_py.translate import Translate
        return Translate(v=v, child=self)

    def rotate(self, a, v: TUnion[list, Point]) -> 'Object':
        """Apply a rotation"""
        from openscad_py.rotate import Rotate
        return Rotate(a=a, v=v, child=self)

    def scale(self, v: TUnion[list, Point, float]) -> 'Object':
        """Apply scaling. Accepts a single float for uniform scaling"""
        from openscad_py.scale import Scale
        return Scale(v=v, child=self)

    def color(self, r, g, b, a=1.) -> 'Object':
        """Apply a color"""
        from openscad_py.color import Color
        return Color(r=r, g=g, b=b, a=a, child=self)

    def extrude(self, height, convexity = 10, center: bool = False) -> 'Object':
        """Apply a linear extrusion,
        If center is false the linear extrusion Z range is from 0 to height; if it is true, the range is from -height/2 to height/2."""
        from openscad_py.linear_extrude import LinearExtrude
        return LinearExtrude(height=height, child=self, convexity=convexity, center=center)

    def rotate_extrude(self, angle, convexity = 10) -> 'Object':
        """Apply a rotational extrusion. For all points x >= 0 must be true."""
        from openscad_py.rotate_extrude import RotateExtrude
        return RotateExtrude(angle=angle, child=self, convexity=convexity)

    def radial_offset(self, r):
        """A new 2d interior or exterior outline from an existing outline"""
        from openscad_py.radial_offset import RadialOffset
        return RadialOffset(r=r, child=self)

    def delta_offset(self, delta, chamfer=False):
        """A new 2d interior or exterior outline from an existing outline"""
        from openscad_py.delta_offset import DeltaOffset
        return DeltaOffset(delta=delta, child=self, chamfer=chamfer)

    def diff(self, tool: TUnion[list, 'Object']) -> 'Object':
        """Remove from the object using a difference operator"""
        from openscad_py.difference import Difference
        return Difference(subject=self, tool=tool)

    def union(self, objects: TUnion[list, 'Object']) -> 'Object':
        """Form the union of self and an object or list of objects"""
        from openscad_py.union import Union
        from openscad_py.collection import Collection
        return Union(child=Collection.c(objects)._add(self))

    def intersection(self, objects: TUnion[list, 'Object']) -> 'Object':
        """Get the intersection of self and an object of list of objects"""
        from openscad_py.intersection import Intersection
        from openscad_py.collection import Collection
        return Intersection(child=Collection.c(objects)._add(self))

