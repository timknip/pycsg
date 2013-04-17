import math
from geom import *

class CSG(object):
    """
    Constructive Solid Geometry (CSG) is a modeling technique that uses Boolean
    operations like union and intersection to combine 3D solids. This library
    implements CSG operations on meshes elegantly and concisely using BSP trees,
    and is meant to serve as an easily understandable implementation of the
    algorithm. All edge cases involving overlapping coplanar polygons in both
    solids are correctly handled.
    
    Example usage::
    
        from csg.core import CSG
        
        cube = CSG.cube();
        sphere = CSG.sphere({'radius': 1.3});
        polygons = cube.subtract(sphere).toPolygons();
    
    ## Implementation Details
    
    All CSG operations are implemented in terms of two functions, `clipTo()` and
    `invert()`, which remove parts of a BSP tree inside another BSP tree and swap
    solid and empty space, respectively. To find the union of `a` and `b`, we
    want to remove everything in `a` inside `b` and everything in `b` inside `a`,
    then combine polygons from `a` and `b` into one solid::
    
        a.clipTo(b);
        b.clipTo(a);
        a.build(b.allPolygons());
    
    The only tricky part is handling overlapping coplanar polygons in both trees.
    The code above keeps both copies, but we need to keep them in one tree and
    remove them in the other tree. To remove them from `b` we can clip the
    inverse of `b` against `a`. The code for union now looks like this::
    
        a.clipTo(b);
        b.clipTo(a);
        b.invert();
        b.clipTo(a);
        b.invert();
        a.build(b.allPolygons());
    
    Subtraction and intersection naturally follow from set operations. If
    union is `A | B`, subtraction is `A - B = ~(~A | B)` and intersection is
    `A & B = ~(~A | ~B)` where `~` is the complement operator.
    
    ## License
    
    Copyright (c) 2011 Evan Wallace (http://madebyevan.com/), under the MIT license.
    
    Python port Copyright (c) 2012 Tim Knip (http://www.floorplanner.com), under the MIT license.
    """
    def __init__(self):
        self.polygons = []
    
    @classmethod
    def fromPolygons(cls, polygons):
        csg = CSG()
        csg.polygons = polygons
        return csg
    
    def clone(self):
        csg = CSG()
        csg.polygons = map(lambda p: p.clone(), self.polygons)
        return csg
        
    def toPolygons(self):
        return self.polygons
        
    def union(self, csg):
        """
        Return a new CSG solid representing space in either this solid or in the
        solid `csg`. Neither this solid nor the solid `csg` are modified.::
        
            A.union(B)
        
            +-------+            +-------+
            |       |            |       |
            |   A   |            |       |
            |    +--+----+   =   |       +----+
            +----+--+    |       +----+       |
                 |   B   |            |       |
                 |       |            |       |
                 +-------+            +-------+
        """
        a = Node(self.clone().polygons)
        b = Node(csg.clone().polygons)
        a.clipTo(b)
        b.clipTo(a)
        b.invert()
        b.clipTo(a)
        b.invert()
        a.build(b.allPolygons());
        return CSG.fromPolygons(a.allPolygons())
        
    def subtract(self, csg):
        """
        Return a new CSG solid representing space in this solid but not in the
        solid `csg`. Neither this solid nor the solid `csg` are modified.::
        
            A.subtract(B)
        
            +-------+            +-------+
            |       |            |       |
            |   A   |            |       |
            |    +--+----+   =   |    +--+
            +----+--+    |       +----+
                 |   B   |
                 |       |
                 +-------+
        """
        a = Node(self.clone().polygons)
        b = Node(csg.clone().polygons)
        a.invert()
        a.clipTo(b)
        b.clipTo(a)
        b.invert()
        b.clipTo(a)
        b.invert()
        a.build(b.allPolygons())
        a.invert()
        return CSG.fromPolygons(a.allPolygons())
        
    def intersect(self, csg):
        """
        Return a new CSG solid representing space both this solid and in the
        solid `csg`. Neither this solid nor the solid `csg` are modified.::
        
            A.intersect(B)
        
            +-------+
            |       |
            |   A   |
            |    +--+----+   =   +--+
            +----+--+    |       +--+
                 |   B   |
                 |       |
                 +-------+
        """
        a = Node(self.clone().polygons)
        b = Node(csg.clone().polygons)
        a.invert()
        b.clipTo(a)
        b.invert()
        a.clipTo(b)
        b.clipTo(a)
        a.build(b.allPolygons())
        a.invert()
        return CSG.fromPolygons(a.allPolygons())
        
    def inverse(self):
        """
        Return a new CSG solid with solid and empty space switched. This solid is
        not modified.
        """
        csg = self.clone()
        map(lambda p: p.flip(), csg.polygons)
        return csg
    
    @classmethod
    def cube(cls, center=[0,0,0], radius=[1,1,1]):
        """
        Construct an axis-aligned solid cuboid. Optional parameters are `center` and
        `radius`, which default to `[0, 0, 0]` and `[1, 1, 1]`. The radius can be
        specified using a single number or a list of three numbers, one for each axis.
        
        Example code::
        
            cube = CSG.cube(
              center=[0, 0, 0],
              radius=1
            )
        """
        c = Vector(0, 0, 0)
        r = [1, 1, 1]
        if isinstance(center, list): c = Vector(center)
        if isinstance(radius, list): r = radius
        else: r = [radius, radius, radius]

        polygons = map(
            lambda v: Polygon( 
                map(lambda i: 
                    Vertex(
                        Vector(
                            c.x + r[0] * (2 * bool(i & 1) - 1),
                            c.y + r[1] * (2 * bool(i & 2) - 1),
                            c.z + r[2] * (2 * bool(i & 4) - 1)
                        ), 
                        v[1]
                    ), v[0])),
                    [
                        [[0, 4, 6, 2], [-1, 0, 0]],
                        [[1, 3, 7, 5], [+1, 0, 0]],
                        [[0, 1, 5, 4], [0, -1, 0]],
                        [[2, 6, 7, 3], [0, +1, 0]],
                        [[0, 2, 3, 1], [0, 0, -1]],
                        [[4, 5, 7, 6], [0, 0, +1]]
                    ])
            
        return CSG.fromPolygons(polygons)
