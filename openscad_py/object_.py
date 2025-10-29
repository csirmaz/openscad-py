
from typing import Union as TUnion
from typing import List
import math

from openscad_py.point import Point


class Object:
    """Base class for an SCAD object. Defines convenience methods to apply transformations."""

    def _center(self) -> str:
        """Render the `center` flag into string"""
        return ('true' if self.center else 'false')

    def _add(self, obj: 'Object'):
        """Add an object, forming a Collection"""
        from openscad_py.collection import Collection
        return Collection([self, obj])

    def render(self) -> str:
        """Render the object into OpenSCAD code"""
        raise Exception("abstract method")

    def translate(self, v: TUnion[list, Point]) -> 'Object':
        """Apply a translation and return a new object.
        See https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Transformations#translate
        """
        from openscad_py.translate import Translate
        return Translate(v=v, child=self)

    def move(self, v: TUnion[list, Point]) -> 'Object':
        """Apply a translation and return a new object. Synonym of `translate()`"""
        from openscad_py.translate import Translate
        return Translate(v=v, child=self)

    def rotate(self, a, v: TUnion[list, Point]) -> 'Object':
        """Apply a rotation and return a new object.
        See https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Transformations#rotate
        """
        from openscad_py.rotate import Rotate
        return Rotate(a=a, v=v, child=self)

    def scale(self, v: TUnion[list, Point, float]) -> 'Object':
        """Apply scaling and return a new object. Accepts a vector (a Point object or a list of floats)
         or a single float for uniform scaling.
         See https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Transformations#scale
         """
        from openscad_py.scale import Scale
        return Scale(v=v, child=self)

    def color(self, r, g, b, a=1.) -> 'Object':
        """Apply a color and return a new object.
        See https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Transformations#color
        """
        from openscad_py.color import Color
        return Color(r=r, g=g, b=b, a=a, child=self)

    def extrude(self, height, convexity = 10, center: bool = False) -> 'Object':
        """Apply a linear extrusion and return a new object.
        If `center` is false, the linear extrusion Z range is from 0 to height;
        if it is true, the range is from -height/2 to height/2.
        See https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/2D_to_3D_Extrusion
        """
        from openscad_py.linear_extrude import LinearExtrude
        return LinearExtrude(height=height, child=self, convexity=convexity, center=center)

    def rotate_extrude(self, angle, convexity = 10) -> 'Object':
        """Apply a rotational extrusion and return a new object. For all points x >= 0 must be true.
        See https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/2D_to_3D_Extrusion
        """
        from openscad_py.rotate_extrude import RotateExtrude
        return RotateExtrude(angle=angle, child=self, convexity=convexity)

    def radial_offset(self, r):
        """Return a new 2D interior or exterior outline from an existing outline.
        See https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Transformations#offset
        """
        from openscad_py.radial_offset import RadialOffset
        return RadialOffset(r=r, child=self)

    def delta_offset(self, delta, chamfer=False):
        """Return a new 2D interior or exterior outline from an existing outline.
        See https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Transformations#offset
        """
        from openscad_py.delta_offset import DeltaOffset
        return DeltaOffset(delta=delta, child=self, chamfer=chamfer)

    def diff(self, tool: TUnion[list, 'Object']) -> 'Object':
        """Remove from the object using a difference operator, and return a new object.
        See https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/CSG_Modelling#difference
        """
        from openscad_py.difference import Difference
        return Difference(subject=self, tool=tool)

    def union(self, objects: TUnion[list, 'Object', None] = None) -> 'Object':
        """Form the union of self and an optional object or list of objects, and return a new object.
        See https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/CSG_Modelling#union
        """
        from openscad_py.union import Union
        from openscad_py.collection import Collection
        return Union(child=Collection.c(objects)._add(self))

    def intersection(self, objects: TUnion[list, 'Object']) -> 'Object':
        """Get the intersection of self and an object of list of objects, and return a new object.
        See https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/CSG_Modelling#intersection
        """
        from openscad_py.intersection import Intersection
        from openscad_py.collection import Collection
        return Intersection(child=Collection.c(objects)._add(self))
    
    def hull(self, objects: TUnion[list, 'Object', None] = None) -> 'Object':
        """Get the convex hull of self and an optional object or list of objects, and return a new object.
        See https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Transformations#hull
        """
        from openscad_py.hull import Hull
        from openscad_py.collection import Collection
        return Hull(child=Collection.c(objects)._add(self))

