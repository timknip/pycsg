import os
import sys
import unittest

sys.path.insert(0, os.getcwd())

from csg.core import CSG
from csg.geom import Vector

class TestCSG(unittest.TestCase):
    def setUp(self):
        print('setup')
    
    def tearDown(self):
        print('tear')
    
    def test_cs(self):
        print('ss')

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
        b = a.refine()
        b.saveVTK('test_sphere_refined.vtk')
        
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
        d = c.refine().refine()
        d.saveVTK('test_cube_union_refined_2x.vtk')

    def test_sphere_union(self):
        a = CSG.sphere(center=(0., 0., 0.), radius=1.0, slices=64, stacks=32)
        b = CSG.sphere(center=(1.99, 0., 0.), radius=1.0, slices=64, stacks=32)
        c = a + b
        a.saveVTK('test_sphere_union_a.vtk')
        b.saveVTK('test_sphere_union_b.vtk')
        c.saveVTK('test_sphere_union.vtk')

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

    def test_bolt(self):
        shaft = CSG.cylinder(start=[0., 0., 0.], end=[1., 0., 0.], radius=0.1, slices=32)
        head = CSG.cone(start=[-0.12, 0., 0.], end=[0.10, 0., 0.], radius=0.25)
        notch1 = CSG.cube(center=[-0.10, 0., 0.], radius=[0.02, 0.20, 0.02])
        notch2 = CSG.cube(center=[-0.10, 0., 0.], radius=[0.02, 0.02, 0.20])
        bolt = shaft + head - notch1 - notch2
        bolt.saveVTK('test_bolt.vtk')
        bolt2x = bolt.refine()
        bolt2x.saveVTK('test_bolt2x.vtk')

    def test_translate_cube(self):
        a = CSG.cube()
        a.saveVTK('a.vtk')
        a.translate(disp=[0.1, 0.2, 0.3])
        a.saveVTK('aTranslated.vtk')

    def test_rotate_cube(self):
        a = CSG.cube()
        a.saveVTK('a.vtk')
        a.rotate(axis=[0.1, 0.2, 0.3], angleDeg=20.0)
        a.saveVTK('aRotated.vtk')

    def test_translate_cylinder(self):
        b = CSG.cylinder()
        b.saveVTK('b.vtk')
        b.translate(disp=[0.1, 0.2, 0.3])
        b.saveVTK('bTranslated.vtk')

    def test_rotate_cylinder(self):
        b = CSG.cylinder()
        b.saveVTK('b.vtk')
        b.rotate(axis=[0.1, 0.2, 0.3], angleDeg=20.0)
        b.saveVTK('bRotated.vtk')
        
if __name__ == '__main__':
    unittest.main()
