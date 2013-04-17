import os
import sys
import unittest
sys.path.append(os.getcwd())

from csg.core import CSG
from csg.geom import Vector

class TestCSG(unittest.TestCase):

    def test_csg(self):
        a = CSG.cube()
        b = CSG.cube([0.5, 0.5, 0.0])
        polygons = a.subtract(b).toPolygons()
        print polygons
        print Vector
        
if __name__ == '__main__':
    unittest.main()