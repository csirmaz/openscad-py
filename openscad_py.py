
from typing import Union
import numpy as np

EPSILON = 1e-7
NP_TYPE = np.float_


class Point:
    """Represents a 3D point of vector"""
    
    def __init__(self, coords):
        self.c = np.array(coords, dtype=NP_TYPE)
        
    @classmethod
    def c(cls, coords: Union[list, Point]) -> Point:
        """Ensure coords is an instance of Point"""
        if isinstance(coords, Point):
            return coords
        return Point(coords)

    def render(self) -> str:
        return ",".join([str(c) for c in self.c])

    def scale(self, x: float) -> Point:
        """Scale the current vector/point by a scalar"""
        return self.__class__(self.c * x)
     
    def add(self, p: Point) -> Point:
        assert isinstance(p, Point)
        assert self.dim() == p.dim()
        return self.__class__(self.c + p.c)
    
    def sub(self, p: Point) -> Point:
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
    
    def norm(self) -> Point:
        l = self.length()
        if l == 0:
            raise Exception("normalising 0 vector")
        return self.__class__(self.c / self.length())
    
    def dot(self, p: Point) -> float:
        return np.dot(self.c, p.c)

    def eq(self, p: Point) -> bool:
        return (self.c == p.c).all()
    
    def lt(self, p: Point) -> bool:
        return (self.c < p.c).all()

    def le(self, p: Point) -> bool:
        return (self.c <= p.c).all()

    def gt(self, p: Point) -> bool:
        return (self.c > p.c).all()

    def ge(self, p: Point) -> bool:
        return (self.c >= p.c).all()

    def allclose(self, p: Point) -> bool:
        return self.c.shape == p.c.shape and np.allclose(self.c, p.c)

    def rotate(self, coords, angle: float) -> Point:
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
    
    def __init__(self):
        pass
    
    def _center(self) -> str:
        return ('true' if self.center else 'false')
    
    def add(self, obj):
        return Collection([self, action])
    
    def render(self) -> str:
        raise Exception("abstract method")
    
    def move(self, v: Union[list, Point]):
        return Translate(v, self)


class Cube(Object):
    
    def __init__(self, size: Union[list, Point], center: bool = False):
        self.size = Point.c(position)
        self.center = center
        
    def render(self):
        return f"cube(size=[{self.size.render()}], center={self._center()});"


def Sphere(Object):
    
    def __init__(self, r):
        self.r = r
        # $fa, $fs, $fn
        
    def render(self):
        return f"sphere(r={self.r});"


def Cylinder(Object):
    
    def __init__(self, h, r=None, r1=None, r2=None, center: bool = False):
        self.height = h
        self.r1 = r if r1 is None else r1
        self.r2 = r if r2 is None else r2
        # $fa, $fs, $fn
        
    def render(self):
        return f"cylinder(h={self.height}, r1={self.r1}, r2={self.r2}, center={self._center()});"


# TODO polyhedron(points=[[],], faces[[p,],], convexity=)
# TODO https://docs.python.org/3/reference/datamodel.html#emulating-numeric-types


class Collection(Object):
    
    def __init__(self, coll: list):
        self.collection = coll
    
    def add(self, obj):
        self.collection.append(obj)
        
    def render(self):
        return "\n".join([o.render() for o in self.collection])


class Translate(Object):
    
    def __init__(self, v: Union[list, Point], child: Object):
        self.v = Point.c(v)
        
    def render(self):
        return f"translate(v=[{self.v.render()}]){{\n{self.child.render()}\n}}"
    
    
