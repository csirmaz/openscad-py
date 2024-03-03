
from typing import Union as TUnion
import math
import numpy as np

EPSILON = 1e-7
NP_TYPE = np.float_


class Point:
    """Represents a point of vector in arbitrary dimensions"""
    
    def __init__(self, coords):
        self.c = np.array(coords, dtype=NP_TYPE)
        
    @classmethod
    def c(cls, coords: TUnion[list, 'Point']) -> 'Point':
        """Ensure coords is an instance of Point"""
        if isinstance(coords, Point):
            return coords
        return Point(coords)

    def render(self) -> str:
        """Render the point into a SCAD script"""
        return "[" + (",".join([str(c) for c in self.c])) + "]"

    def scale(self, x: float) -> 'Point':
        """Scale the current vector/point by a scalar"""
        return self.__class__(self.c * x)
     
    def add(self, p: 'Point') -> 'Point':
        assert isinstance(p, Point)
        assert self.dim() == p.dim()
        return self.__class__(self.c + p.c)
    
    def sub(self, p: 'Point') -> 'Point':
        assert isinstance(p, Point)
        assert self.dim() == p.dim()
        return self.__class__(self.c - p.c)
    
    def dim(self) -> int:
        """Return the number of dimensions"""
        return self.c.shape[0]

    def is_zero(self) -> bool:
        """Return whether all coordinates are very close to 0"""
        return np.all(np.abs(self.c) < EPSILON)

    def length(self) -> float:
        """Return the length of the vector"""
        return np.sqrt(np.square(self.c).sum())
    
    def norm(self) -> 'Point':
        l = self.length()
        if l == 0:
            raise Exception("normalising 0 vector")
        return self.__class__(self.c / self.length())
    
    def dot(self, p: 'Point') -> float:
        """Return the dot product"""
        return np.dot(self.c, p.c)
    
    def cross(self, p: 'Point') -> 'Point':
        """Return the cross product"""
        assert self.dim() == 3
        assert p.dim() == 3
        return Point([
            self.c[1]*p.c[2] - self.c[2]*p.c[1],
            self.c[2]*p.c[0] - self.c[0]*p.c[2],
            self.c[0]*p.c[1] - self.c[1]*p.c[0]
            
        ])

    def eq(self, p: 'Point') -> bool:
        return (self.c == p.c).all()
    
    def lt(self, p: 'Point') -> bool:
        return (self.c < p.c).all()

    def le(self, p: 'Point') -> bool:
        return (self.c <= p.c).all()

    def gt(self, p: 'Point') -> bool:
        return (self.c > p.c).all()

    def ge(self, p: 'Point') -> bool:
        return (self.c >= p.c).all()

    def allclose(self, p: 'Point') -> bool:
        return self.c.shape == p.c.shape and np.allclose(self.c, p.c)
    
    def angle(self, p: 'Point') -> float:
        """Return the angle between two vectors, in degrees"""
        r = self.dot(p)
        r = r / self.length() / p.length()
        r = math.acos(r)
        return r / math.pi * 180.        

    def rotate(self, coords, angle: float) -> 'Point':
        """Rotate. coords is a list of 2 coordinate indices that we rotate"""
        assert len(coords) == 2
        ca, cb = coords
        s = np.sin(angle / 180. * np.pi)
        c = np.cos(angle / 180. * np.pi)
        r = self.clone().reset_cache()
        r.c[ca] = c * self.c[ca] + s * self.c[cb]
        r.c[cb] = -s * self.c[ca] + c * self.c[cb]
        return r
    
    # Operator overloading

    def __add__(self, other):
        return self.add(other)

    def __radd__(self, other):
        assert isinstance(other, Point)
        return other.add(self)

    def __sub__(self, other):
        return self.sub(other)

    def __rsub__(self, other):
        assert isinstance(other, Point)
        return other.sub(self)

    def __mul__(self, other):
        return self.scale(other)
    
    def __rmul__(self, other):
        return self.scale(other)
    

class Object:
    """Abstract class for an SCAD object"""
    
    def _center(self) -> str:
        return ('true' if self.center else 'false')
    
    def _add(self, obj):
        """Add an object, forming a collection"""
        return Collection([self, obj])
    
    def render(self) -> str:
        raise Exception("abstract method")
    
    def translate(self, v: TUnion[list, Point]) -> 'Object':
        """Apply a translation"""
        return Translate(v=v, child=self)

    def move(self, v: TUnion[list, Point]) -> 'Object':
        """Apply a translation"""
        return Translate(v=v, child=self)

    def rotate(self, a, v: TUnion[list, Point]) -> 'Object':
        """Apply a rotation"""
        return Rotate(a=a, v=v, child=self)

    def scale(self, v: TUnion[list, Point, float]) -> 'Object':
        """Apply scaling. Accepts a single float for uniform scaling"""
        return Scale(v=v, child=self)

    def color(self, r, g, b, a=1.) -> 'Object':
        """Apply a color"""
        return Color(r=r, g=g, b=b, a=a, child=self)

    def extrude(self, height, convexity = 10, center: bool = False) -> 'Object':
        """Apply a linear extrusion"""
        return LinearExtrude(height=height, child=self, convexity=convexity, center=center)

    def diff(self, tool: TUnion[list, 'Object']) -> 'Object':
        """Remove from the object using a difference operator"""
        return Difference(subject=self, tool=tool)

    def union(self, objects: TUnion[list, 'Object']) -> 'Object':
        return Union(child=Collection.c(objects)._add(self))


class Header:
    
    def __init__(self, draft: bool = True):
        self.draft = draft
        
    def render(self):
        return "" if self.draft else "$fa=6;$fs=0.1;"


class Cube(Object):
    """A 3D primitive, cube"""
    
    def __init__(self, size: TUnion[list, Point], center: bool = False):
        self.size = Point.c(size)
        self.center = center
        
    def render(self):
        return f"cube(size={self.size.render()}, center={self._center()});"


class Sphere(Object):
    """A 3D primitive, sphere"""
    
    def __init__(self, r):
        self.r = r
        # $fa, $fs, $fn
        
    def render(self):
        return f"sphere(r={self.r});"


class Cylinder(Object):
    """A 3D primitive, cylinder"""
    
    def __init__(self, h, r=None, r1=None, r2=None, center: bool = False):
        self.height = h
        self.r1 = r if r1 is None else r1
        self.r2 = r if r2 is None else r2
        self.center = center
        # $fa, $fs, $fn
        
    def render(self):
        return f"cylinder(h={self.height}, r1={self.r1}, r2={self.r2}, center={self._center()});"
    
    @classmethod
    def from_ends(cls, radius: float, p1: TUnion[list, Point], p2: TUnion[list, Point]) -> Object:
        """Construct a cylinder between two points"""
        p1 = Point.c(p1)
        p2 = Point.c(p2)
        v = p2.sub(p1)
        length = v.length()
        assert length != 0
        z = Point([0, 0, 1])
        r = z.cross(v).norm()
        rangle = v.angle(z)
        if r.length() == 0:
            # The cylinder is in the Z direction
            if abs(abs(rangle) - 180.) < .1:
                p1 = p2
            rangle = 0
            r = z
        return cls(h=length, r=radius, center=False).rotate(a=rangle, v=r).move(p1)


class Circle(Object):
    """A 2D primitive, circle"""

    def __init__(self, r, fn=None):
        self.r = r
        self.fn = fn
        # $fa, $fs, $fn

    @classmethod
    def triangle(cls, r):
        """Create a regular triangle"""
        return cls(r=r, fn=3)

    @classmethod
    def regular_polygon(cls, r, sides: int):
        """Create a regular polygon"""
        return cls(r=r, fn=sides)

    def render(self) -> str:
        fnstr = '' if self.fn is None else f", $fn={self.fn}"
        return f"circle(r={self.r}{fnstr});"


class Polygon(Object):
    """A 2D primitive, polygon"""

    def __init__(self, points, paths=None, convexity=1):
        assert paths is None  # not implemented yet
        self.points = [Point.c(p) for p in points]
        self.convexity = convexity

    def render(self) -> str:
        return f"polygon(points=[{','.join([p.render() for p in self.points])}], convexity={self.convexity});"

# TODO polyhedron(points=[[],], faces[[p,],], convexity=)
# TODO https://docs.python.org/3/reference/datamodel.html#emulating-numeric-types


class Collection(Object):
    
    def __init__(self, coll: list):
        self.collection = coll

    @classmethod
    def c(cls, coll: TUnion[list, Object]) -> Object:
        """Cast lists to collections"""
        if isinstance(coll, Object):
            return coll
        return cls(coll)
    
    def _add(self, obj):
        return self.__class__(self.collection + [obj])

    def render(self) -> str:
        return "\n".join([o.render() for o in self.collection])


class Translate(Object):
    """Represents a translation transformation applied to an object"""
    
    def __init__(self, v: TUnion[list, Point], child: Object):
        self.v = Point.c(v)
        self.child = child
        
    def render(self) -> str:
        return f"translate(v={self.v.render()}){{\n{self.child.render()}\n}}"
    
    
class Rotate(Object):
    """Represents a rotation transformation applied to an object"""

    def __init__(self, a, v: TUnion[list, Point], child: Object):
        self.a = a
        self.v = Point.c(v)
        self.child = child
        
    def render(self) -> str:
        return f"rotate(a={self.a}, v={self.v.render()}){{\n{self.child.render()}\n}}"


class Scale(Object):

    def __init__(self, v: TUnion[list, Point, float], child: Object):
        if isinstance(v, float):
            v = [v, v, v]
        self.v = Point.c(v)
        self.child = child

    def render(self) -> str:
        return f"scale(v={self.v.render()}){{\n{self.child.render()}\n}}"


class Color(Object):

    def __init__(self, child: Object, r, g, b, a=1.):
        self.color = [r, g, b, a]
        self.child = child

    def render(self) -> str:
        return f"color(c=[{','.join([str(c) for c in self.color])}]){{ {self.child.render()} }}"


class LinearExtrude(Object):
    """Represents a linear extrusion applied to an object"""

    def __init__(self, height, child: Object, convexity = 10, center: bool = False):
        self.height = height
        self.child = child
        self.convexity = convexity
        self.center = center
        # twist, slices, scale (float/vector), $fn

    def render(self) -> str:
        return f"linear_extrude(height={self.height}, center={self._center()}, convexity={self.convexity}){{\n{self.child.render()}\n}}"


class Union(Object):
    """Represents a union applied to an object (usually a collection of objects)"""

    def __init__(self, child: TUnion[Object, list]):
        self.child = Collection.c(child)

    def render(self) -> str:
        return f"union(){{ {self.child.render()} }}"

    def union(self, objects: TUnion[list, Object]) -> Object:
        return self.__class__(self.child._add(objects))


class Intersection(Object):
    """Represents an intersection applied to an object (usually a collection of objects)"""

    def __init__(self, child: TUnion[Object, list]):
        self.child = Collection.c(child)

    def render(self) -> str:
        return f"intersection(){{ {self.child.render()} }}"


class Difference(Object):
    """Represents a difference"""

    def __init__(self, subject: Object, tool: TUnion[list, Object]):
        self.subject = subject
        self.tool = Collection.c(tool)  # what to remove

    def render(self) -> str:
        return f"difference(){{ {self.subject.render()}\n{self.tool.render()} }}"

