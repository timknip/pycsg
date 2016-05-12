import os
import sys
import unittest

sys.path.insert(0, os.getcwd())

from csg.geom import BSPNode, Polygon, Vector, Vertex

class TestBSPNode(unittest.TestCase):
    def setUp(self):
        print('setup')
    
    def tearDown(self):
        print('tear')
    
    def test_noPolygons(self):
        node = BSPNode()

    def test_simple(self):
        v0 = Vertex([0., 0., 0.])
        v1 = Vertex([1., 0., 0.])
        v2 = Vertex([1., 1., 0.])
        p0 = Polygon([v0, v1, v2])
        polygons = [p0]
        node = BSPNode(polygons)

    def test_infiniteRecursion(self):
        # This polygon is not exactly planar, causing
        # an infinite recursion when building the BSP
        # tree. Because of the last node, polygon is
        # put at the back of the list with respect to
        # its own cutting plane -- it should be classified
        # as co-planar
        v0 = Vertex([0.12, -0.24, 1.50])
        v1 = Vertex([0.01, 0.00, 1.75])
        v2 = Vertex([-0.03, 0.05, 1.79])
        v3 = Vertex([-0.13, -0.08, 1.5])
        p0 = Polygon([v0, v1, v2, v3])
        polygons = [p0]
        node = BSPNode(polygons)

if __name__ == '__main__':
    unittest.main()
