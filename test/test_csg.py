import os
import sys
import unittest

sys.path.insert(0, os.getcwd())

from csg.core import CSG
from csg.geom import Vector

class TestCSG(unittest.TestCase):
    def setUp(self):
        print 'setup'
    
    def tearDown(self):
        print 'tear'
    
    def test_cs(self):
        print 'ss'

    def test_toPolygons(self):
        a = CSG.cube([0.5, 0.5, 0.0])
        aPolys = a.toPolygons()
        b = CSG.sphere()
        bPolys = b.toPolygons()
        c = CSG.cylinder()
        cPolys = c.toPolygons()

    def test_cone(self):
        a = CSG.cone(start=[0., 0., 0.], end=[1., 2., 3.], radius=1.0, slices=8)
        a.saveVTK('test_cone.vtk')

    def test_cube(self):
        a = CSG.cube(center=[0., 0., 0.], radius=[1., 2., 3.])
        a.saveVTK('test_cube.vtk')

    def test_cylinder(self):
        a = CSG.cylinder(start=[0., 0., 0.], end=[1., 2., 3.], radius=1.0, slices=8)
        a.saveVTK('test_cylinder.vtk')

    def test_sphere(self):
        a = CSG.sphere(center=[0., 0., 0.], radius=1., slices=4, stacks=3)
        a.saveVTK('test_sphere.vtk')
        
    def test_cube_intersect(self):
        a = CSG.cube()
        b = CSG.cube([0.5, 0.5, 0.0])
        c = a * b
        c.saveVTK('test_cube_intersect.vtk')

    def test_cube_union(self):
        a = CSG.cube()
        b = CSG.cube([0.5, 0.5, 0.0])
        c = a + b
        c.saveVTK('test_cube_union.vtk')

    def test_cube_subtract(self):
        a = CSG.cube()
        b = CSG.cube([0.5, 0.5, 0.0])
        c = a - b
        c.saveVTK('test_cube_subtract.vtk')

    def test_sphere_cylinder_intersect(self):
        a = CSG.sphere(center=[0.5, 0.5, 0.5], radius=0.5, slices=8, stacks=4)
        b = CSG.cylinder(start=[0.,0.,0.], end=[1.,0.,0.], radius=0.3, slices=16)
        a.intersect(b).saveVTK('test_sphere_cylinder_intersect.vtk')

    def test_sphere_cylinder_union(self):
        a = CSG.sphere(center=[0.5, 0.5, 0.5], radius=0.5, slices=8, stacks=4)
        b = CSG.cylinder(start=[0.,0.,0.], end=[1.,0.,0.], radius=0.3, slices=16)
        a.union(b).saveVTK('test_sphere_cylinder_union.vtk')

    def test_sphere_cylinder_subtract(self):
        a = CSG.sphere(center=[0.5, 0.5, 0.5], radius=0.5, slices=8, stacks=4)
        b = CSG.cylinder(start=[0.,0.,0.], end=[1.,0.,0.], radius=0.3, slices=16)
        a.subtract(b).saveVTK('test_sphere_cylinder_subtract.vtk')
        
if __name__ == '__main__':
    unittest.main()
