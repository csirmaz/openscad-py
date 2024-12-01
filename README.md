# openscad-py

A Python OOP precompiler for OpenSCAD's language

[OpenSCAD](https://openscad.org/) uses a functional scripting language to define solid 3D CAD models.
As such, it is a prefix language (modifiers go before the things they modify).

OpenSCADPy allows one to write OpenSCAD scripts using an object representation, which uses method calls
to describe modifications. This way, modifications are written after the objects they modify in a postfix
fashion, more closely resembling a procedural ordering of steps in the creation of the models.

It also contains convenience functions to define a wider range of primitives, vector operations, and a method
to export polyhedra directly to STL.

## Example

```python
# example.py
from openscad_py import Cube

colored_moved_cube = Cube([1, 1, 1]).move([2, 0, 0]).color(r=1, g=0, b=0)
print(colored_moved_cube.render())
```

prints the OpenSCAD code

```
# example.scad
color(c=[1,0,0,1.0]){ translate(v=[2.0,0.0,0.0]){
cube(size=[1.0,1.0,1.0], center=false);
} }
```

An easy way to write and render the OpenSCAD code would be

```
$ python3 example.py > example.scad
$ openscad example.scad
```

## Notable convenience functions

### Computational geometry

Usual computational geometry functions are implemented in the 
[`Point` class](https://csirmaz.github.io/openscad-py/point.html)
that work in an arbitrary number of dimensions. Overloads algebraic operators. Examples:

```python
distance = (Point((0, 0, 1)) - Point((1, 0, 1))).length()
angle_between = Point((0, 0, 1) * 2).angle(Point((1, 0, 1)))
```

### Cylinders

`Cylinder.from_ends()` constructs a cylinder between two given points in space. Example:

```python
openscad_code = Cylinder.from_ends(radius=2, p1=(0, 0, 1), p2=(1, 0, 2)).render()
```

### Tubes and toroids from a point grid

[`Polyhedron.tube()`](https://csirmaz.github.io/openscad-py/polyhedron.html#openscad_py.polyhedron.Polyhedron.tube) 
creates a tube-like Polyhedron object from a 2D array of points.

[`Polyhedron.torus()`](https://csirmaz.github.io/openscad-py/polyhedron.html#openscad_py.polyhedron.Polyhedron.torus)
creates a toroid Polyhedron object from a 2D array of points.

### Tubes from a path

[`PathTube`](https://csirmaz.github.io/openscad-py/path_tube.html)
creates a tube-like or toroid Polyhedron object from an arbitrary path. Example:

```python
PathTube(
    points=[(0,0,0), (0,0,1), (1,0,2), (1,1,0), (0,.5,0)],
    radius=.2,
    fn=4
)
```

![PathTube example](https://raw.github.com/csirmaz/openscad-py/master/images/pathtube.png)

### Polyhedron from a height map

[`Polyhedron.from_heightmap()`](https://csirmaz.github.io/openscad-py/polyhedron.html#openscad_py.polyhedron.Polyhedron.from_heightmap)
creates a Polyhedron object from a 2D matrix of heights. Example:

```python
Polyhedron.from_heightmap(
    heights=[
        [3, 3, 1, 1, 1],
        [3, 3, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 2, 2],
        [1, 1, 1, 2, 2],
    ],
    base=-5
)
```

![Heightmap example](https://raw.github.com/csirmaz/openscad-py/master/images/heightmap.png)

### Direct STL export

[`Polyhedron.render_stl()`](https://csirmaz.github.io/openscad-py/polyhedron.html#openscad_py.polyhedron.Polyhedron.render_stl)
exports a Polyhedron object into STL directly.
This works well with `tube()`, `torus()`, `from_heightmap()` and `PathTube` described above. 
Note that the polyhedron object cannot be post-modified (e.g. by `union`, `difference`) - if so, 
use OpenSCAD to render the object and export to STL.

## Overview and usage

In `openscad_py`, all objects (including derived ones) come with a large set of convenience methods
to apply transformations, implemented in the base [`Object` class](https://csirmaz.github.io/openscad-py/object_.html).
This allows to freely specify transformations on any object:

```python
moved_cube = Cube([1, 1, 1]).move([2, 0, 0])
colored_moved_cube = Cube([1, 1, 1]).move([2, 0, 0]).color(r=1, g=0, b=0)
```

Once the desired object has been created, call `render()` on the final object to obtain the
OpenSCAD code.

## Reference

See https://csirmaz.github.io/openscad-py/
