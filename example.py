
from openscad_py import Cube

colored_moved_cube = Cube([1, 1, 1]).move([2, 0, 0]).color(r=1, g=0, b=0)
print(colored_moved_cube.render())


