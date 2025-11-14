
from typing import Union as TUnion
from typing import List
import math

from openscad_py.point import Point
from openscad_py.object_ import Object


class Polyhedron(Object):
    """A 3D primitive, a polyhedron defined by a list of points and faces.
    Nonplanar faces will be triangulated by OpenSCAD.

    See https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/The_OpenSCAD_Language#polyhedron
    """

    def __init__(self, points: List[TUnion[list, Point]], faces: List[list], convexity: int = 10):
        """
        Arguments:
            - points: a list of Point objects or coordinate tuples defining the vertices
            - faces: defines the faces as a list of lists of vertex indices. The points of a face must be listed clockwise when looking at the face from the outside inward.
        """
        self.points = [Point.c(p) for p in points]
        self.faces = faces
        self.convexity = convexity

    @classmethod
    def torus(cls, points: List[List[TUnion[list, Point]]], torus_connect_offset: int = 0, convexity: int = 10):
        """Construct a torus-like polyhedron from a 2D array of points.
        Each row of points must be oriented clockwise when looking from the first row (loop) toward the next.
        The rows of points form loops.

        Arguments:
            - points: A 2D array of points
            - torus_connect_offset: int, Whether to shift which points are connected in a torus in the last segment
            - convexity: int, see OpensCAD
        """
        return cls.tube(points=points, convexity=convexity, make_torus=True, torus_connect_offset=torus_connect_offset)

    @classmethod
    def tube(cls, points: List[List[TUnion[list, Point]]], make_torus: bool = False, torus_connect_offset: int = 0, convexity: int = 10):
        """Construct a tube-like polyhedron from a 2D array of points.
        Each row of points must be oriented clockwise when looking at the pipe at the start inwards.
        The rows of points form loops.

        Arguments:
            - points: A 2D array of points
            - make_torus: bool, Whether to create a torus-like shape instead of a pipe with ends
            - torus_connect_offset: int, Whether to shift which points are connected in a torus in the last segment
            - convexity: int, see OpensCAD
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
            
        if not make_torus:
            
            # Starting cap
            faces.append([point_map[(0,x)] for x in range(row_len)])
            # Ending cap
            faces.append([point_map[(rows-1,row_len-1-x)] for x in range(row_len)])
            
        else:
            
            # Connect the end to the start
            for col_ix in range(row_len):
                faces.append([
                    point_map[(0, (col_ix-1+torus_connect_offset)%row_len)],
                    point_map[(0, (col_ix+torus_connect_offset)%row_len)],
                    point_map[(rows-1, col_ix%row_len)],
                    point_map[(rows-1, (col_ix-1)%row_len)]
                ])
        
        return cls(points=point_list, faces=faces, convexity=convexity)

    @classmethod
    def from_heightmap(cls, heights: List[List[float]], base: float = 0., step_x: float = 1., step_y: float = 1., convexity: int = 10):
        """Construct a polyhedron from a 2D matrix of heights. If the height at [0,0] is Z, it maps
        to the point (0, 0, Z).

        Arguments:
            - heights: The 2D matrix of heights
            - base: The height at which the base will be - in the scale of heights (optional; default 0)
            - step_x: The X coordinate becomes `step_x * index_x` (default 1)
            - step_y: The Y coordinate becomes `step_y * index_y` (default 1)
            - convexity: see OpenSCAD
        """
        rows = len(heights)
        row_len = len(heights[0])
        point_list = []
        point_map = {}  # { (row_ix,col_ix) -> list_ix, ...
        bottom_point_map = {}
        for row_ix, row in enumerate(heights):
            for col_ix, height in enumerate(row):
                point = Point([row_ix*step_x, col_ix*step_y, height])
                bottom_point = Point([row_ix*step_x, col_ix*step_y, base])
                
                point_map[(row_ix, col_ix)] = len(point_list)
                point_list.append(point)
                
                bottom_point_map[(row_ix, col_ix)] = len(point_list)
                point_list.append(bottom_point)
                
        faces = []

        # Surface (top) faces
        #  r 10 11
        # c
        # 10  1  2
        # 11  4  3
        for row_ix in range(1, rows):
            for col_ix in range(1, row_len):
                faces.append([
                    point_map[(row_ix-1, col_ix-1)],
                    point_map[(row_ix, col_ix-1)],
                    point_map[(row_ix, col_ix)],
                    point_map[(row_ix-1, col_ix)]
                ])

        # Bottom faces
        for row_ix in range(1, rows):
            for col_ix in range(1, row_len):
                faces.append([
                    bottom_point_map[(row_ix-1, col_ix-1)], # 1
                    bottom_point_map[(row_ix-1, col_ix)], # 4
                    bottom_point_map[(row_ix, col_ix)], # 3
                    bottom_point_map[(row_ix, col_ix-1)] # 2
                ])
        
        # Side faces
        for row_ix in range(1, rows):
            m = row_len - 1
            faces.append([
                point_map[(row_ix-1, m)],
                point_map[(row_ix, m)],
                bottom_point_map[(row_ix, m)],
                bottom_point_map[(row_ix-1, m)]
            ])
            faces.append([
                point_map[(row_ix, 0)],
                point_map[(row_ix-1, 0)],
                bottom_point_map[(row_ix-1, 0)],
                bottom_point_map[(row_ix, 0)]
            ])
        
        for col_ix in range(1, row_len):
            m = rows - 1
            faces.append([
                point_map[(m, col_ix)],
                point_map[(m, col_ix-1)],
                bottom_point_map[(m, col_ix-1)],
                bottom_point_map[(m, col_ix)]
            ])
            faces.append([
                point_map[(0, col_ix-1)],
                point_map[(0, col_ix)],
                bottom_point_map[(0, col_ix)],
                bottom_point_map[(0, col_ix-1)]
            ])
            
        return cls(points=point_list, faces=faces, convexity=convexity)

    def render(self) -> str:
        """Render the object into OpenSCAD code"""
        faces_list = [f"[{','.join([str(x) for x in face])}]" for face in self.faces]
        return f"polyhedron(points=[{','.join([p.render() for p in self.points])}], faces=[{','.join(faces_list)}], convexity={self.convexity});"

    def render_stl(self) -> str:
        """Export the polyhedron as an STL file"""
        stl = []
        
        def write_triangle(p1, p2, p3):
            normal = (p2 - p1).cross(p3 - p1)
            if normal.is_zero():
                # Degenerate triangle
                return
            normal = normal.norm()
            stl.append("facet normal " + normal.render_stl())
            stl.append("outer loop")
            for p in [p1, p2, p3]:
                stl.append("vertex " + p.render_stl())
            stl.append("endloop")
            stl.append("endfacet")
        
        stl.append("solid oscpy")
        for face in self.faces:
            face = [self.points[i] for i in face]
            # stl.append(f"# FACE {len(face)} {','.join([p.render() for p in face])}")
            if len(face) < 3:
                raise Exception("Face has less than 3 points")
            elif len(face) == 3:
                write_triangle(face[0], face[1], face[2])
            elif len(face) == 4:
                # Decide which diagonal is best to break on
                d1 = face[0].sub(face[2]).length()
                d2 = face[1].sub(face[3]).length()
                if d1 < d2:
                    write_triangle(face[0], face[1], face[2])
                    write_triangle(face[0], face[2], face[3])
                else:
                    write_triangle(face[0], face[1], face[3])
                    write_triangle(face[1], face[2], face[3])
            else:
                # Add central point and split face in a star-shaped form
                # of course this won't always work on concave faces
                s = None
                for p in face:
                    if s is None:
                        s = p
                    else:
                        s += p
                s = s.scale(1 / len(face))
                for i in range(len(face)):
                    i_next = i + 1
                    if i_next > len(face) - 1:
                        i_next = 0
                    write_triangle(face[i], face[i_next], s)
        stl.append("endsolid oscpy")
        return "\n".join(stl)

