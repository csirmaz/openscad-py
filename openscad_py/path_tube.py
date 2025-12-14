
from typing import Union as TUnion
from typing import List
import math

from openscad_py.point import Point
from openscad_py.object_ import Object
from openscad_py.polyhedron import Polyhedron


class PathTube(Object):
    """Creates a tube-like or toroid polyhedron from a path (list of points)."""

    def __init__(
        self, 
        points: List[TUnion[list, Point]], 
        radius: TUnion[float, list, callable], 
        fn: int, 
        make_torus: bool = False, 
        init_seam_angle: float = 0.,
        convexity: int = 10
    ):
        """
        Arguments:
            - points: The list of points
            - radius: 
                - a float for uniform radius
                - a list of floats for each point along the path
                - a callable that returns the radius given (p_index, r_index) where
                    p_index is the position along the path and r_index is the position along the ring
                    [0, fn)
            - fn: int, The number of sides
            - make_torus: bool, Whether to make a torus instead of a pipe with ends. Warning: the last segment may be twisted.
            - init_seam_angle: Rotate the seam by this many degrees
            - convexity: see openscad
        """
        self.points = [Point.c(p) for p in points]
        if isinstance(radius, list):
            self.radius_fn = lambda p_index, r_index: radius[p_index]
        elif callable(radius):
            self.radius_fn = radius
        else:
            self.radius_fn = lambda p_index, r_index: radius
        self.fn = fn
        self.make_torus = make_torus
        self.init_seam_angle = init_seam_angle
        self.convexity = convexity

    def process(self, debug: bool = False) -> Polyhedron:
        """Generate a Polyhedron object from the parameters"""
        points_rows = []
        
        for ix, point in enumerate(self.points):
            if debug: print(f"//LOOP {ix}: {point.render()}")
            
            if (not self.make_torus) and ix == 0:
                # Start of the path
                v = self.points[1].sub(point)  # vector toward the first point
                z_point = Point([0,0,1])
                seam = v.cross(z_point)  # Track a seam along the pipe using this vector pointing from the middle line
                if seam.length() == 0: # v is in the z direction
                    seam = Point([1,0,0])
                seam = seam.norm()
                seam2 = v.cross(seam).norm()
                if debug: print(f"//Start. v={v.render()} seam={seam.render()} seam2={seam2.render()}")
                if self.init_seam_angle != 0:
                    old_seam = seam
                    old_seam2 = seam2
                    seam_angle = self.init_seam_angle / 180. * math.pi
                    seam = math.cos(seam_angle) * old_seam + math.sin(seam_angle) * old_seam2
                    seam2 = - math.sin(seam_angle) * old_seam + math.cos(seam_angle) * old_seam2
                    if debug: print(f"//Rotated. v={v.render()} seam={seam.render()} seam2={seam2.render()}")
                points = []
                for i in range(self.fn):
                    a = math.pi*2*i/self.fn
                    points.append((seam*math.cos(a) + seam2*math.sin(a))*self.radius_fn(ix, i) + point)
                points_rows.append(points)
                if debug: print(f"//  Row: {', '.join([p.render() for p in points])}")
                
            elif (not self.make_torus) and ix == len(self.points) - 1:
                # End of the path
                v = point.sub(self.points[-2])
                seam2 = v.cross(seam).norm()
                if debug: print(f"//End. v={v.render()} seam={seam.render()} seam2={seam2.render()}")
                points = []
                for i in range(self.fn):
                    a = math.pi*2*i/self.fn
                    points.append((seam*math.cos(a) + seam2*math.sin(a))*self.radius_fn(ix, i) + point)
                points_rows.append(points)
                if debug: print(f"//  Row: {', '.join([p.render() for p in points])}")
                
            else:
                # Middle of the path
                iprev = ix - 1 if ix > 0 else len(self.points) - 1
                inext = ix + 1 if ix < len(self.points) - 1 else 0
                # (p[-1]) -va-> (p[0]) -vb-> (p[1])
                va = point.sub(self.points[iprev]).norm()  # vector incoming to this elbow
                vb = self.points[inext].sub(point).norm()  # vector going out from this elbow
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
                
                if ix == 0:
                    # We just choose a seam when making a torus
                    seam_angle = self.init_seam_angle / 180. * math.pi
                else:
                    # The new seam on vb (seam_b) has the same angle to vb_inner as it had on va to va_inner
                    seam_angle = seam.angle(va_inner, mode="rad")
                    # need to figure out the sign of the angle
                    if seam_angle != 0:
                        if va_inner.cross(seam).dot(va) < 0:
                            seam_angle = -seam_angle
                vb_inner2 = vb.cross(vb_inner).norm()
                seam_b = vb_inner*math.cos(seam_angle) + vb_inner2*math.sin(seam_angle)
                if debug:
                    if ix == 0:
                        print(f"//  seam=N/A seam_b={seam_b.render()}")
                    else:
                        print(f"//  seam={seam.render()} seam_b={seam_b.render()}")
                
                vangle = va.scale(-1).angle(vb, mode="rad")
                long_inner = (vb-va).norm().scale(1/math.sin(vangle/2))
                # long_inner is the long axis of the elliptic intersection between the cylinders around va and vb
                short = va.cross(long_inner).norm()  # the short axis of the ellipse
                if debug: print(f"//  long_inner={long_inner.render()} short={short.render()} vangle={vangle/math.pi*180}(deg) seam_angle={seam_angle/math.pi*180}(deg)")
                points = []
                for i in range(self.fn):
                    # We draw the ellipse according to long_inner and short, but use seam_angle to get the right points
                    a = math.pi*2*i/self.fn + seam_angle
                    points.append((long_inner*math.cos(a) + short*math.sin(a))*self.radius_fn(ix, i) + point)
                points_rows.append(points)
                if debug: print(f"//  Row: {', '.join([p.render() for p in points])}")
                
                seam = seam_b
        
        return Polyhedron.tube(points=points_rows, convexity=self.convexity, make_torus=self.make_torus)

    def render(self) -> str:
        """Render the object into OpenSCAD code"""
        return self.process().render()


