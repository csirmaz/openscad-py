
from typing import Union as TUnion
from typing import List
import math
import numpy as np

EPSILON = 1e-7
NP_TYPE = np.float_


class Point:
    """Represents a point or vector in arbitrary number of dimensions"""
    
    def __init__(self, coords: List[float]):
        self.c = np.array(coords, dtype=NP_TYPE)
        
    @classmethod
    def c(cls, coords: TUnion[list[float], 'Point']) -> 'Point':
        """Ensure `coords` is an instance of Point (idempotent)"""
        if isinstance(coords, Point):
            return coords
        return Point(coords)

    def render(self) -> str:
        """Render the point / vector into OpenSCAD code"""
        return "[" + (",".join([str(c) for c in self.c])) + "]"
    
    def render_stl(self) -> str:
        """Render the point / vector into STL"""
        return " ".join([str(c) for c in self.c])

    def scale(self, x: float) -> 'Point':
        """Scale the current point / vector by the scalar `x`"""
        return self.__class__(self.c * x)
     
    def add(self, p: 'Point') -> 'Point':
        """Add another point / vector `p` to the current one"""
        assert isinstance(p, Point)
        assert self.dim() == p.dim()
        return self.__class__(self.c + p.c)
    
    def sub(self, p: 'Point') -> 'Point':
        """Subtract another point / vector `p` from the current one"""
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
        """Return a normalized version of the vector (scaled to length 1)"""
        l = self.length()
        if l == 0:
            raise Exception("Attempted to normalise 0 vector")
        return self.__class__(self.c / self.length())
    
    def dot(self, p: 'Point') -> float:
        """Return the dot product of the current vector and `p`"""
        return np.dot(self.c, p.c)
    
    def cross(self, p: 'Point') -> 'Point':
        """Return the cross product of the current vector and `p`"""
        assert self.dim() == 3
        assert p.dim() == 3
        return Point([
            self.c[1]*p.c[2] - self.c[2]*p.c[1],
            self.c[2]*p.c[0] - self.c[0]*p.c[2],
            self.c[0]*p.c[1] - self.c[1]*p.c[0]
            
        ])

    def eq(self, p: 'Point') -> bool:
        """Return whether the current point / vector and `p` are equal"""
        return (self.c == p.c).all()
    
    def lt(self, p: 'Point') -> bool:
        """Return whether the current vector is smaller than `p` in each dimension"""
        return (self.c < p.c).all()

    def le(self, p: 'Point') -> bool:
        """Return whether the current vector is smaller or equal to `p` in each dimension"""
        return (self.c <= p.c).all()

    def gt(self, p: 'Point') -> bool:
        """Return whether the current vector is greater than `p` in each dimension"""
        return (self.c > p.c).all()

    def ge(self, p: 'Point') -> bool:
        """Return whether the current vector is greater or equal to `p` in each dimension"""
        return (self.c >= p.c).all()

    def allclose(self, p: 'Point') -> bool:
        """Return whether the current point / vector and `p` are close to each other"""
        return self.c.shape == p.c.shape and np.allclose(self.c, p.c)
    
    def angle(self, p: 'Point', mode: str = "deg") -> float:
        """Return the angle between two vectors in degrees or radians

        Arguments:
            - p: a Point object
            - mode: "deg" | "rad"
        """
        r = self.dot(p)
        r = r / self.length() / p.length()
        r = math.acos(r)
        if mode == "rad":
            return r
        if mode == "deg":
            return r / math.pi * 180.
        raise ValueError("Unknown mode")
    
    def z_slope(self, mode: str = "deg") -> float:
        """Return the slope of a vector in degrees or radians

        Arguments:
            - mode: "deg" | "rad"
        """
        r = self.c[2] / self.length()
        r = math.asin(r)
        if mode == "rad":
            return r
        if mode == "deg":
            return r / math.pi * 180.
        raise ValueError("Unknown mode")        

    def rotate(self, coords, angle: float) -> 'Point':
        """Rotate the current vector

         Arguments:
             - coords: A list of 2 coordinate indices to rotate
             - angle: the angle to rotate by, in degrees
        """
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
        """Use `p1 + p2` to add two vectors"""
        return self.add(other)

    def __radd__(self, other):
        """Use `p1 + p2` to add two vectors"""
        assert isinstance(other, Point)
        return other.add(self)

    def __sub__(self, other):
        """Use `p1 - p2` to subtract two vectors"""
        return self.sub(other)

    def __rsub__(self, other):
        """Use `p1 - p2` to subtract two vectors"""
        assert isinstance(other, Point)
        return other.sub(self)

    def __mul__(self, other):
        """Use `p * x` to scale a vector"""
        return self.scale(other)
    
    def __rmul__(self, other):
        """Use `x * p` to scale a vector"""
        return self.scale(other)
    
    def __neg__(self):
        """Use `-p` to negate a vector"""
        return self.scale(-1.)
    

__pdoc__ = {
    'Point.__add__': True,
    'Point.__sub__': True,
    'Point.__mul__': True,
    'Point.__rmul__': True,
    'Point.__neg__': True,
}