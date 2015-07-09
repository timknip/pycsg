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
        
    def test_cube_intersect(self):
        a = CSG.cube()
        b = CSG.cube([0.5, 0.5, 0.0])
        a.intersect(b).saveVTK('test_cube_intersect.vtk')

    def test_cube_union(self):
        a = CSG.cube()
        b = CSG.cube([0.5, 0.5, 0.0])
        a.union(b).saveVTK('test_cube_union.vtk')

    def test_cube_subtract(self):
        a = CSG.cube()
        b = CSG.cube([0.5, 0.5, 0.0])
        a.subtract(b).saveVTK('test_cube_subtract.vtk')
        
if __name__ == '__main__':
    unittest.main()
