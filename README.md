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
Cube([1, 1, 2]).move([0, 0, 1])
```

becomes


```
translate(v=[0, 0, 1]) { cube(size=[1, 1, 2], center=false); }
```

