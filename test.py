
from openscad_py import Cube, Cylinder


print(Cube([1,1,1]).render())
print(Cylinder(h=5, r=2).render())
print(Cylinder.from_ends(2, [0,0,0], [1,0,0]).render())
