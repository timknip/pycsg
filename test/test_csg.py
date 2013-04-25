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
        
    def test_csg(self):
        a = CSG.cube()
        b = CSG.cube([0.5, 0.5, 0.0])
        polygons = a.subtract(b).toPolygons()
        print polygons
        print Vector
        
if __name__ == '__main__':
    unittest.main()