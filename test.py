
import math
from openscad_py import Cube, PathTube


#print(Cube([1,1,1]).render())
#print(Cylinder(h=5, r=2).render())
#print(Cylinder.from_ends(2, [0,0,0], [1,0,0]).render())

points=[]
segments=128
for i in range(segments):
    points.append([
        math.sin(2*math.pi/segments*i),
        math.cos(2*math.pi/segments*i),
        i/segments
    ])
#print(points)
print(PathTube(
    points=points,
    radius=lambda p_index, r_index: (r_index % 2)*.1 + .1,
    fn=10,
    make_torus=False,
    init_seam_angle=45
).process().render())
