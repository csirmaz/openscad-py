# openscad-py

A Python OOP precompiler for OpenSCAD's language

OpenSCAD ( https://openscad.org/ ) uses a functional scripting language to define solid 3D CAD models.
As such, it is a prefix language (modifiers go before the things they modify).

OpenSCADPy allows one to write OpenSCAD scripts using an object representation, which uses method calls
to describe modifications. This way, modifications are written after the objects they modify in a postfix
fashion, more closely resembling a procedural ordering of steps in the creation of the models.
It also contains convenience functions to define a wider range of primitives, as well as some vector operations.

## Example

```
Cube([1, 1, 2]).move([0, 0, 1]).render()
```

returns


```
translate(v=[0, 0, 1]) { cube(size=[1, 1, 2], center=false); }
```

## Notable convenience functions

### Computational geometry

Usual computational geometry functions on the `Point` class that work in an arbitrary number of dimensions. Overloads for algebraic operators.

```
distance = (Point((0, 0, 1)) - Point((1, 0, 1))).length()
angle_between = Point((0, 0, 1) * 2).angle(Point((1, 0, 1)))
```

### Cylinders

`Cylinder.from_ends()` constructs a cylinder between two given points in space

```
openscad_code = Cylinder.from_ends(radius=2, p1=(0, 0, 1), p2=(1, 0, 2)).render()
```

### Tubes and toroids from a point grid

`Polyhedron.tube()` creates a tube-like polyhedron from a 2D array of points

`Polyhedron.torus()` creates a toroid polyhedron from a 2D array of points

### Tubes from a path

`PathTube` creates a tube-like or toroid polyhedron from an arbitrary path

```
PathTube(
    points=[(0,0,0), (0,0,1), (1,0,2), (1,1,0), (0,.5,0)],
    radius=.2,
    fn=4
)
```

![PathTube example](https://raw.github.com/csirmaz/openscad-py/master/images/pathtube.png)

### Polyhedron from a height map

```
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

`Polyhedron.render_stl()` exports any polyhedron into STL directly
