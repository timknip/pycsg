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
    
    def test_sphere(self):
        a = CSG.sphere(center=[0., 0., 0.], radius=1., slices=4, stacks=3)
       	a.saveVTK('test_sphere.vtk')
        b = a.refine()
        b.saveVTK('test_sphere_refined.vtk')
        
    def test_cube_union(self):
        a = CSG.cube()
        b = CSG.cube([0.5, 0.5, 0.0])
        c = a + b
        c.saveVTK('test_cube_union.vtk')
        d = c.refine().refine()
        d.saveVTK('test_cube_union_refined_2x.vtk')

if __name__ == '__main__':
    unittest.main()
