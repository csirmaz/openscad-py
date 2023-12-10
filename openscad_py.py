
from typing import Union


class Point:
    """Represents a 3D point of vector"""
    
    def __init__(self, coords):
        self.coords = coords
        
    @classmethod
    def c(cls, coords: Union[list, Point]) -> Point:
        """Ensure coords is an instance of Point"""
        if isinstance(coords, Point):
            return coords
        return Point(coords)

    def render(self) -> str:
        return ",".join([str(c) for c in self.coords])


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


# polyhedron(points=[[],], faces[[p,],], convexity=)


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
    
    
