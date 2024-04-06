
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
        """Apply a linear extrusion,
        If center is false the linear extrusion Z range is from 0 to height; if it is true, the range is from -height/2 to height/2."""
        return LinearExtrude(height=height, child=self, convexity=convexity, center=center)
    
    def radial_offset(self, r):
        """A new 2d interior or exterior outline from an existing outline"""
        return RadialOffset(r=r, child=self)
    
    def delta_offset(self, delta, chamfer=False):
        """A new 2d interior or exterior outline from an existing outline"""
        return DeltaOffset(delta=delta, child=self, chamfer=chamfer)

    def diff(self, tool: TUnion[list, 'Object']) -> 'Object':
        """Remove from the object using a difference operator"""
        return Difference(subject=self, tool=tool)

    def union(self, objects: TUnion[list, 'Object']) -> 'Object':
        """Form the union of self and an object or list of objects"""
        return Union(child=Collection.c(objects)._add(self))


class Header:
    """Render a header (setting global values) of an OpensCAD file"""
    
    def __init__(self, quality: str = 'draft'):
        self.quality = quality
        
    def render(self):
        # See https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Other_Language_Features#Circle_resolution:_$fa,_$fs,_and_$fn
        if self.quality == 'draft':
            return ""
        if self.quality == 'mid':
            return "$fa=12;$fs=0.2;"
        if self.quality == 'best':
            return "$fa=6;$fs=0.1;"
        raise ValueError("Unknown quality")


class Cube(Object):
    """A 3D primitive, cube.
    Creates a cube in the first octant. When center is true, the cube is centered on the origin."""
    # https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/The_OpenSCAD_Language#cube
    
    def __init__(self, size: TUnion[list, Point], center: bool = False):
        self.size = Point.c(size)
        self.center = center
        
    def render(self):
        return f"cube(size={self.size.render()}, center={self._center()});"


class Sphere(Object):
    """A 3D primitive, sphere.
    Creates a sphere at the origin of the coordinate system."""
    # https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/The_OpenSCAD_Language#sphere
    
    def __init__(self, r):
        self.r = r
        # $fa, $fs, $fn
        
    def render(self):
        return f"sphere(r={self.r});"


class Cylinder(Object):
    """A 3D primitive, cylinder.
    Creates a cylinder or cone centered about the z axis. When center is true, it is also centered vertically along the z axis."""
    # https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/The_OpenSCAD_Language#cylinder
    
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
        r = z.cross(v)
        rangle = v.angle(z)
        if r.length() == 0:
            # The cylinder is in the Z direction
            if abs(abs(rangle) - 180.) < .1:
                p1 = p2
            rangle = 0
            r = z
        else:
            r = r.norm()
        return cls(h=length, r=radius, center=False).rotate(a=rangle, v=r).move(p1)


class Polyhedron(Object):
    """A 3D primitive, a polyhedron defined by a list of points and faces."""
    # See https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/The_OpenSCAD_Language#polyhedron
    # Nonplanar faces should be triangulated by opensCAD
    
    def __init__(self, points: List[TUnion[list, Point]], faces: List[list], convexity: int = 10):
        self.points = [Point.c(p) for p in points]
        self.faces = faces
        self.convexity = convexity

    @classmethod
    def tube(cls, points: List[List[TUnion[list, Point]]], convexity: int = 10):
        """Construct a tube-like polyhedron from a 2D array of points.
        Each row of points must be oriented clockwise when looking at the pipe at the start inwards.
        The rows of points form loops.
        """
        rows = len(points)
        row_len = len(points[0])
        point_list = []
        point_map = {}  # { (row_ix,col_ix) -> list_ix, ...
        for row_ix, row in enumerate(points):
            for col_ix, point in enumerate(row):
                point_map[(row_ix, col_ix)] = len(point_list)
                point_list.append(point)
                
        faces = []
        
        # Side faces
        for row_ix in range(1, rows):
            for col_ix in range(1, row_len):
                faces.append([
                    point_map[(row_ix, col_ix-1)],
                    point_map[(row_ix, col_ix)],
                    point_map[(row_ix-1, col_ix)],
                    point_map[(row_ix-1, col_ix-1)]
                ])
            faces.append([
                point_map[(row_ix, row_len-1)],
                point_map[(row_ix, 0)],
                point_map[(row_ix-1, 0)],
                point_map[(row_ix-1, row_len-1)]
            ])
            
        # Starting cap
        faces.append([point_map[(0,x)] for x in range(row_len)])
        
        # Ending cap
        faces.append([point_map[(rows-1,row_len-1-x)] for x in range(row_len)])
        
        return cls(points=point_list, faces=faces, convexity=convexity)
                
    def render(self) -> str:
        faces_list = [f"[{','.join([str(x) for x in face])}]" for face in self.faces]
        return f"polyhedron(points=[{','.join([p.render() for p in self.points])}], faces=[{','.join(faces_list)}], convexity={self.convexity});"


class PathTube(Object):
    """Creates a tube-like or toroid polyhedron from a path (list of points)."""
    
    def __init__(self, points: List[TUnion[list, Point]], radius: float, fn: int, convexity: int = 10):
        self.points = [Point.c(p) for p in points]
        self.radius = radius
        self.fn = fn  # number of sides
        self.convexity = convexity
    
    def process(self, debug: bool = False) -> Polyhedron:
        points_rows = []
        
        for ix, point in enumerate(self.points):
            if debug: print(f"//LOOP {ix}: {point.render()}")
            
            if ix == 0:
                # Start of the path
                v = self.points[1].sub(point)  # vector toward the first point
                z_point = Point([0,0,1])
                seam = v.cross(z_point)  # Track a seam along the pipe using this vector pointing from the middle line
                if seam.length() == 0: # v is in the z direction
                    seam = Point([1,0,0])
                seam = seam.norm()
                seam2 = v.cross(seam).norm()
                if debug: print(f"//Start. v={v.render()} seam={seam.render()} seam2={seam2.render()}")
                points = []
                for i in range(self.fn):
                    a = math.pi*2*i/self.fn
                    points.append((seam*math.cos(a) + seam2*math.sin(a))*self.radius + point)
                points_rows.append(points)
                if debug: print(f"//  Row: {', '.join([p.render() for p in points])}")
                
            elif ix == len(self.points) - 1:
                # End of the path
                v = point.sub(self.points[-2])
                seam2 = v.cross(seam).norm()
                if debug: print(f"//End. v={v.render()} seam={seam.render()} seam2={seam2.render()}")
                points = []
                for i in range(self.fn):
                    a = math.pi*2*i/self.fn
                    points.append((seam*math.cos(a) + seam2*math.sin(a))*self.radius + point)
                points_rows.append(points)
                if debug: print(f"//  Row: {', '.join([p.render() for p in points])}")
                
            else:
                # Middle of the path
                # (p[-1]) -va-> (p[0]) -vb-> (p[1])
                va = point.sub(self.points[ix-1]).norm()  # vector incoming to this elbow
                vb = self.points[ix+1].sub(point).norm()  # vector going out from this elbow
                if debug: print(f"//Middle. va={va.render()} vb={vb.render()}")
                # Get the vector perpendicular to va that points to the inside of the cylinder around va according
                # to the elbow at p[0]. This is the component of vb in a basis defined by va.
                vdot = va.dot(vb)
                vb_proj = va.scale(vdot) # The projection of vb onto va
                vb_perp = vb.sub(vb_proj) # This is perpendicular to va
                if debug: print(f"//  vb_proj={vb_proj.render()} vb_perp={vb_perp.render()}")
                va_inner = vb_perp.norm()
                
                va_proj = vb.scale(vdot)
                va_perp = va.sub(va_proj)
                if debug: print(f"//  va_proj={va_proj.render()} va_perp={va_perp.render()}")
                vb_inner = va_perp.scale(-1).norm()  # Here we want to project -va onto vb
                if debug: print(f"//  va_inner={va_inner.render()} vb_inner={vb_inner.render()}")
                
                # The new seam on vb (seam_b) has the same angle to vb_inner as it had on va to va_inner
                seam_angle = seam.angle(va_inner, mode="rad")
                # need to figure out the sign of the angle
                if seam_angle != 0:
                    if va_inner.cross(seam).dot(va) < 0:
                        seam_angle = -seam_angle
                vb_inner2 = vb.cross(vb_inner).norm()
                seam_b = vb_inner*math.cos(seam_angle) + vb_inner2*math.sin(seam_angle)
                if debug: print(f"//  seam={seam.render()} seam_b={seam_b.render()}")
                
                vangle = va.scale(-1).angle(vb, mode="rad")
                long_inner = (vb-va).norm().scale(1/math.sin(vangle/2))
                # long_inner is the long axis of the elliptic intersection between the cylinders around va and vb
                short = va.cross(long_inner).norm()  # the short axis of the ellipse
                if debug: print(f"//  long_inner={long_inner.render()} short={short.render()} vangle={vangle/math.pi*180}(deg) seam_angle={seam_angle/math.pi*180}(deg)")
                points = []
                for i in range(self.fn):
                    # We draw the ellipse according to long_inner and short, but use seam_angle to get the right points
                    a = math.pi*2*i/self.fn + seam_angle
                    points.append((long_inner*math.cos(a) + short*math.sin(a))*self.radius + point)
                points_rows.append(points)
                if debug: print(f"//  Row: {', '.join([p.render() for p in points])}")
                
                seam = seam_b
        
        return Polyhedron.tube(points=points_rows, convexity=self.convexity)
    
    def render(self) -> str:
        return self.process().render()


class Circle(Object):
    """A 2D primitive, circle.
    Creates a circle (or regular polygon) at the origin."""
    # https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/The_OpenSCAD_Language#circle

    def __init__(self, r: float, fn: TUnion[int, None] = None):
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


# TODO https://docs.python.org/3/reference/datamodel.html#emulating-numeric-types


class Collection(Object):
    """Represents a collection of objects"""
    
    def __init__(self, coll: list):
        self.collection = coll

    @classmethod
    def c(cls, coll: TUnion[list, Object]) -> Object:
        """Ensure the list of objects is a Collection (idempotent)"""
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

    def __init__(self, v: TUnion[list, Point, float, int], child: Object):
        if isinstance(v, float) or isinstance(v, int):
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
    """Represents a linear extrusion applied to an object.
    If center is false the linear extrusion Z range is from 0 to height; if it is true, the range is from -height/2 to height/2."""

    def __init__(self, height, child: Object, convexity = 10, center: bool = False):
        self.height = height
        self.child = child
        self.convexity = convexity
        self.center = center
        # twist, slices, scale (float/vector), $fn

    def render(self) -> str:
        return f"linear_extrude(height={self.height}, center={self._center()}, convexity={self.convexity}){{\n{self.child.render()}\n}}"


class RadialOffset(Object):
    """A new 2d interior or exterior outline from an existing outline"""
    # https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Transformations#offset
    
    def __init__(self, r, child: Object):
        self.r = r
        self.child = child
        # $fa, $fs, and $fn
        
    def render(self) -> str:
        return f"offset(r={self.r}){{\n{self.child.render()}\n}}"


class DeltaOffset(Object):
    """A new 2d interior or exterior outline from an existing outline"""
    # https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Transformations#offset
    
    def __init__(self, delta, child: Object, chamfer: bool = False):
        self.delta = delta
        self.child = child
        self.chamfer = chamfer
        
    def render(self) -> str:
        return f"offset(delta={delta}, chamfer={'true' if self.chamfer else 'false'}){{\n{self.child.render()}\n}}"


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

