import math

class CSG(object):
    """
    Constructive Solid Geometry (CSG) is a modeling technique that uses Boolean
    operations like union and intersection to combine 3D solids. This library
    implements CSG operations on meshes elegantly and concisely using BSP trees,
    and is meant to serve as an easily understandable implementation of the
    algorithm. All edge cases involving overlapping coplanar polygons in both
    solids are correctly handled.
    
    Example usage:
    
        cube = CSG.cube();
        sphere = CSG.sphere({'radius': 1.3});
        polygons = cube.subtract(sphere).toPolygons();
    
    ## Implementation Details
    
    All CSG operations are implemented in terms of two functions, `clipTo()` and
    `invert()`, which remove parts of a BSP tree inside another BSP tree and swap
    solid and empty space, respectively. To find the union of `a` and `b`, we
    want to remove everything in `a` inside `b` and everything in `b` inside `a`,
    then combine polygons from `a` and `b` into one solid:
    
        a.clipTo(b);
        b.clipTo(a);
        a.build(b.allPolygons());
    
    The only tricky part is handling overlapping coplanar polygons in both trees.
    The code above keeps both copies, but we need to keep them in one tree and
    remove them in the other tree. To remove them from `b` we can clip the
    inverse of `b` against `a`. The code for union now looks like this:
    
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
        solid `csg`. Neither this solid nor the solid `csg` are modified.
        
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
        a = CSG.Node(self.clone().polygons)
        b = CSG.Node(csg.clone().polygons)
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
        solid `csg`. Neither this solid nor the solid `csg` are modified.
        
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
        a = CSG.Node(self.clone().polygons)
        b = CSG.Node(csg.clone().polygons)
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
        solid `csg`. Neither this solid nor the solid `csg` are modified.
        
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
        a = CSG.Node(self.clone().polygons)
        b = CSG.Node(csg.clone().polygons)
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
        
        Example code:
        
            cube = CSG.cube(
              center=[0, 0, 0],
              radius=1
            )
        """
        c = CSG.Vector(0, 0, 0)
        r = [1, 1, 1]
        if isinstance(center, list): c = CSG.Vector(center)
        if isinstance(radius, list): r = radius
        else: r = [radius, radius, radius]

        polygons = map(
            lambda v: CSG.Polygon( 
                map(lambda i: 
                    CSG.Vertex(
                        CSG.Vector(
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
        
    class Vector(object):
        """
        class Vector

        Represents a 3D vector.
        
        Example usage:
             CSG.Vector(1, 2, 3);
             CSG.Vector([1, 2, 3]);
             CSG.Vector({ 'x': 1, 'y': 2, 'z': 3 });
        """
        def __init__(self, *args):
            if len(args) == 3:
                self.x = args[0]
                self.y = args[1]
                self.z = args[2]
            elif len(args) == 1 and isinstance(args[0], CSG.Vector):
                self.x = args[0][0]
                self.y = args[0][1]
                self.z = args[0][2]
            elif len(args) == 1 and isinstance(args[0], list):
                self.x = args[0][0]
                self.y = args[0][1]
                self.z = args[0][2]
            elif len(args) == 1 and args[0] and 'x' in args[0]:
                self.x = args[0]['x']
                self.y = args[0]['y']
                self.z = args[0]['z']
            else:
                self.x = 0.0
                self.y = 0.0
                self.z = 0.0
                
        def clone(self):
            return CSG.Vector(self.x, self.y, self.z)
            
        def negated(self):
            return CSG.Vector(-self.x, -self.y, -self.z)
        
        def plus(self, a):
            return CSG.Vector(self.x+a.x, self.y+a.y, self.z+a.z)
        
        def minus(self, a):
            return CSG.Vector(self.x-a.x, self.y-a.y, self.z-a.z)
        
        def times(self, a):
            return CSG.Vector(self.x*a, self.y*a, self.z*a)
                
        def dividedBy(self, a):
            return CSG.Vector(self.x/a, self.y/a, self.z/a)
        
        def dot(self, a):
            return self.x*a.x + self.y*a.y + self.z*a.z
        
        def lerp(self, a, t):
            return self.plus(a.minus(self).times(t));
        
        def length(self):
            return math.sqrt(self.dot(self))
        
        def unit(self):
            return self.dividedBy(self.length())
            
        def cross(self, a):
            return CSG.Vector(
                self.y * a.z - self.z * a.y,
                self.z * a.x - self.x * a.z,
                self.x * a.y - self.y * a.x)
              
        def __getitem__(self, key):
            return (self.x, self.y, self.z)[key]

        def __setitem__(self, key, value):
            l = [self.x, self.y, self.z]
            l[key] = value
            self.x, self.y, self.z = l
                
        def __len__(self):
            return 3
        
        def __iter__(self):
            return iter((self.x, self.y, self.z))
                
        def __repr__(self):
            return 'CSG.Vector(%.2f, %.2f, %0.2f)' % (self.x, self.y, self.z) 
            
    class Vertex(object):
        """ 
        Class Vertex 
    
        Represents a vertex of a polygon. Use your own vertex class instead of this
        one to provide additional features like texture coordinates and vertex
        colors. Custom vertex classes need to provide a `pos` property and `clone()`,
        `flip()`, and `interpolate()` methods that behave analogous to the ones
        defined by `CSG.Vertex`. This class provides `normal` so convenience
        functions like `CSG.sphere()` can return a smooth vertex normal, but `normal`
        is not used anywhere else.
        """
        def __init__(self, pos, normal=None):
            self.pos = CSG.Vector(pos)
            self.normal = CSG.Vector(normal)
        
        def clone(self):
            return CSG.Vertex(self.pos.clone(), self.normal.clone())
        
        def flip(self):
            """
            Invert all orientation-specific data (e.g. vertex normal). Called when the
            orientation of a polygon is flipped.
            """
            self.normal = self.normal.negated()

        def interpolate(self, other, t):
            """
            Create a new vertex between this vertex and `other` by linearly
            interpolating all properties using a parameter of `t`. Subclasses should
            override this to interpolate additional properties.
            """
            return CSG.Vertex(self.pos.lerp(other.pos, t), 
                              self.normal.lerp(other.normal, t))
                              
    class Plane(object):
        """
        class Plane

        Represents a plane in 3D space.
        """
        
        """
        `CSG.Plane.EPSILON` is the tolerance used by `splitPolygon()` to decide if a
        point is on the plane.
        """
        EPSILON = 1e-5

        def __init__(self, normal, w):
            self.normal = normal
            self.w = w
        
        @classmethod
        def fromPoints(cls, a, b, c):
            n = b.minus(a).cross(c.minus(a)).unit()
            return CSG.Plane(n, n.dot(a))

        def clone(self):
            return CSG.Plane(self.normal.clone(), self.w)
            
        def flip(self):
            self.normal = self.normal.negated()
            self.w = -self.w
        
        def splitPolygon(self, polygon, coplanarFront, coplanarBack, front, back):
            """
            Split `polygon` by this plane if needed, then put the polygon or polygon
            fragments in the appropriate lists. Coplanar polygons go into either
            `coplanarFront` or `coplanarBack` depending on their orientation with
            respect to this plane. Polygons in front or in back of this plane go into
            either `front` or `back`
            """
            COPLANAR = 0
            FRONT = 1
            BACK = 2
            SPANNING = 3

            # Classify each point as well as the entire polygon into one of the above
            # four classes.
            polygonType = 0
            types = []
            
            for i in range(0, len(polygon.vertices)):
                t = self.normal.dot(polygon.vertices[i].pos) - self.w;
                type = -1
                if t < -CSG.Plane.EPSILON: 
                    type = BACK
                elif t > CSG.Plane.EPSILON: 
                    type = FRONT
                else: 
                    type = COPLANAR
                polygonType |= type
                types.append(type)
                
            # Put the polygon in the correct list, splitting it when necessary.
            if polygonType == COPLANAR:
                if self.normal.dot(polygon.plane.normal) > 0:
                    coplanarFront.append(polygon)
                else:
                    coplanarBack.append(polygon)
            elif polygonType == FRONT:
                front.append(polygon)
            elif polygonType == BACK:
                back.append(polygon)
            elif polygonType == SPANNING:
                f = []
                b = []
                for i in range(0, len(polygon.vertices)):
                    j = (i+1) % len(polygon.vertices)
                    ti = types[i]
                    tj = types[j]
                    vi = polygon.vertices[i]
                    vj = polygon.vertices[j]
                    if ti != BACK: f.append(vi)
                    if ti != FRONT:
                        if ti != BACK: 
                            b.append(vi.clone())
                        else:
                            b.append(vi)
                    if (ti | tj) == SPANNING:
                        t = (self.w - self.normal.dot(vi.pos)) / self.normal.dot(vj.pos.minus(vi.pos))
                        v = vi.interpolate(vj, t)
                        f.append(v)
                        b.append(v.clone())
                if len(f) >= 3: front.append(CSG.Polygon(f, polygon.shared))
                if len(b) >= 3: back.append(CSG.Polygon(b, polygon.shared))
    
    class Polygon(object):
        """
        class Polygon

        Represents a convex polygon. The vertices used to initialize a polygon must
        be coplanar and form a convex loop. They do not have to be `CSG.Vertex`
        instances but they must behave similarly (duck typing can be used for
        customization).
        
        Each convex polygon has a `shared` property, which is shared between all
        polygons that are clones of each other or were split from the same polygon.
        This can be used to define per-polygon properties (such as surface color).
        """
        def __init__(self, vertices, shared=None):
            self.vertices = vertices
            self.shared = shared
            self.plane = CSG.Plane.fromPoints(vertices[0].pos, vertices[1].pos, vertices[2].pos)
        
        def clone(self):
            vertices = map(lambda v: v.clone(), self.vertices)
            return CSG.Polygon(vertices, self.shared)
                    
        def flip(self):
            self.vertices.reverse()
            map(lambda v: v.flip(), self.vertices)
            self.plane.flip()
    
    class Node(object):
        """
        class Node

        Holds a node in a BSP tree. A BSP tree is built from a collection of polygons
        by picking a polygon to split along. That polygon (and all other coplanar
        polygons) are added directly to that node and the other polygons are added to
        the front and/or back subtrees. This is not a leafy BSP tree since there is
        no distinction between internal and leaf nodes.
        """
        def __init__(self, polygons=None):
            self.plane = None
            self.front = None
            self.back = None
            self.polygons = []
            if polygons:
                self.build(polygons)
                
        def clone(self):
            node = CSG.Node()
            if self.plane: node.plane = self.plane.clone()
            if self.front: node.front = self.front.clone()
            if self.back: node.back = self.back.clone()
            node.polygons = map(lambda p: p.clone(), self.polygons)
            return node;
            
        def invert(self):
            """ 
            Convert solid space to empty space and empty space to solid space.
            """
            for poly in self.polygons:
                poly.flip()
            self.plane.flip()
            if self.front: self.front.invert()
            if self.back: self.back.invert()
            temp = self.front
            self.front = self.back
            self.back = temp
            
        def clipPolygons(self, polygons):
            """ 
            Recursively remove all polygons in `polygons` that are inside this BSP
            tree.
            """
            if not self.plane: return polygons[:]
            front = []
            back = []
            for poly in polygons:
                self.plane.splitPolygon(poly, front, back, front, back)
            if self.front: front = self.front.clipPolygons(front)
            if self.back: 
                back = self.back.clipPolygons(back)
            else:
                back = []
            front.extend(back)
            return front
            
        def clipTo(self, bsp):
            """ 
            Remove all polygons in this BSP tree that are inside the other BSP tree
            `bsp`.
            """
            self.polygons = bsp.clipPolygons(self.polygons)
            if self.front: self.front.clipTo(bsp)
            if self.back: self.back.clipTo(bsp)
            
        def allPolygons(self):
            """
            Return a list of all polygons in this BSP tree.
            """
            polygons = self.polygons[:]
            if self.front: polygons.extend(self.front.allPolygons())
            if self.back: polygons.extend(self.back.allPolygons())
            return polygons
            
        def build(self, polygons):
            if not len(polygons):
                return
            if not self.plane: self.plane = polygons[0].plane.clone()
            front = []
            back = []
            for poly in polygons:
                self.plane.splitPolygon(poly, self.polygons, self.polygons, front, back)
            if len(front):
                if not self.front: self.front = CSG.Node()
                self.front.build(front)
            if len(back):
                if not self.back: self.back = CSG.Node()
                self.back.build(back)

