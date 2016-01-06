pycsg
=====

Python port of Evan Wallace's [csg.js](https://github.com/evanw/csg.js/)

Constructive Solid Geometry (CSG) is a modeling technique that uses Boolean
operations like union and intersection to combine 3D solids. This library
implements CSG operations on meshes elegantly and concisely using BSP trees,
and is meant to serve as an easily understandable implementation of the
algorithm. All edge cases involving overlapping coplanar polygons in both
solids are correctly handled.

![alt tag](http://content.screencast.com/users/TimKnip/folders/Jing/media/c1ad71ef-5032-4733-a210-2f97ae7b03cc/2015-07-24_2013.png)

examples
========
$ python examples/pyopengl

depends on:
PyOpenGL
PyOpenGL_accelerate
