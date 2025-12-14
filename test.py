
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
        math.sin(i/segments*math.pi*8)/5.
    ])

thickness = .05
width = .2

r = math.sqrt(thickness*thickness+width*width)/2
init_angle = math.atan(width/thickness)/math.pi*180.
angles = [
    init_angle,
    180-init_angle,
    180+init_angle,
    -init_angle
]

#print(points)
print(PathTube(
    points=points,
    radius=lambda p_index, r_index: (r, angles[r_index]),
    #radius=.1,
    fn=4,
    make_torus=True,
    init_seam_angle=90
).process().render())
