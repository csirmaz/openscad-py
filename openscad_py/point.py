
from typing import Union as TUnion
from typing import List
import math
import numpy as np

EPSILON = 1e-7
NP_TYPE = np.float_


class Point:
    """Represents a point or vector in arbitrary dimensions"""
    
    def __init__(self, coords):
        self.c = np.array(coords, dtype=NP_TYPE)
        
    @classmethod
    def c(cls, coords: TUnion[list, 'Point']) -> 'Point':
        """Ensure coords is an instance of Point (idempotent)"""
        if isinstance(coords, Point):
            return coords
        return Point(coords)

    def render(self) -> str:
        """Render the object into OpenSCAD code"""
        return "[" + (",".join([str(c) for c in self.c])) + "]"
    
    def render_stl(self) -> str:
        return " ".join([str(c) for c in self.c])

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
    
    def angle(self, p: 'Point', mode: str = "deg") -> float:
        """Return the angle between two vectors in degrees or radians"""
        r = self.dot(p)
        r = r / self.length() / p.length()
        r = math.acos(r)
        if mode == "rad":
            return r
        if mode == "deg":
            return r / math.pi * 180.
        raise ValueError("Unknown mode")
    
    def z_slope(self, mode: str = "deg") -> float:
        """Return the slope of a vector in degrees or radians"""
        r = self.c[2] / self.length()
        r = math.asin(r)
        if mode == "rad":
            return r
        if mode == "deg":
            return r / math.pi * 180.
        raise ValueError("Unknown mode")        

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
    
    def __neg__(self):
        return self.scale(-1.)
    
