import sys
import os

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

sys.path.insert(0, os.getcwd())

from csg.core import CSG
from csg.geom import Vertex, Vector

from optparse import OptionParser

light_ambient = [0.3, 0.3, 0.3, 1.0]
light_diffuse = [0.7, 0.7, 0.7, 1.0]  # Red diffuse light
light_position = [100.0, 100.0, 100.0, 0.0]  # Infinite light location.

rot = 0.0

class TestRenderable(object):
    def __init__(self, operation):
        self.faces = []
        self.normals = []
        self.vertices = []
        self.colors = []
        self.vnormals = []
        self.list = -1
        
        a = CSG.cube()
        b = CSG.cylinder(radius=0.5, start=[0., -2., 0.], end=[0., 2., 0.])
        for p in a.polygons:
            p.shared = [1.0, 0.0, 0.0, 1.0]
        for p in b.polygons:
            p.shared = [0.0, 1.0, 0.0, 1.0]
            
        recursionlimit = sys.getrecursionlimit()
        sys.setrecursionlimit(10000)
        try:
            if operation == 'subtract':
                polygons = a.subtract(b).toPolygons()
            elif operation == 'union':
                polygons = a.union(b).toPolygons()
            elif operation == 'intersect':
                polygons = a.intersect(b).toPolygons()
            else:
                raise Exception('Unknown operation: \'%s\'' % operation)
        except RuntimeError as e:
            raise RuntimeError(e)
        sys.setrecursionlimit(recursionlimit)
        
        for polygon in polygons:
            n = polygon.plane.normal
            indices = []
            for v in polygon.vertices:
                pos = [v.pos.x, v.pos.y, v.pos.z]
                if not pos in self.vertices:
                    self.vertices.append(pos)
                    self.vnormals.append([])
                index = self.vertices.index(pos)
                indices.append(index)
                self.vnormals[index].append(v.normal)
            self.faces.append(indices)
            self.normals.append([n.x, n.y, n.z])
            self.colors.append(polygon.shared)
        
        # setup vertex-normals
        ns = []
        for vns in self.vnormals:
            n = Vector(0.0, 0.0, 0.0)
            for vn in vns:
                n = n.plus(vn)
            n = n.dividedBy(len(vns))
            ns.append([a for a in n])
        self.vnormals = ns
        
    def render(self):
        if self.list < 0:
            self.list = glGenLists(1)
            glNewList(self.list, GL_COMPILE)
            
            for n, f in enumerate(self.faces):
                glMaterialfv(GL_FRONT, GL_DIFFUSE, self.colors[n])
                glMaterialfv(GL_FRONT, GL_SPECULAR, self.colors[n])
                glMaterialf(GL_FRONT, GL_SHININESS, 50.0)
                glColor4fv(self.colors[n])
            
                glBegin(GL_POLYGON)
                if self.colors[n][0] > 0:
                    glNormal3fv(self.normals[n])

                for i in f:
                    if self.colors[n][1] > 0:
                        glNormal3fv(self.vnormals[i])
                    glVertex3fv(self.vertices[i])
                glEnd()
            glEndList()
        glCallList(self.list)
        
renderable = None

def init():
    # Enable a single OpenGL light.
    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    glEnable(GL_LIGHT0);
    glEnable(GL_LIGHTING);

    # Use depth buffering for hidden surface elimination.
    glEnable(GL_DEPTH_TEST);

    # Setup the view of the cube.
    glMatrixMode(GL_PROJECTION);
    gluPerspective(40.0, 640./480., 1.0, 10.0);
    glMatrixMode(GL_MODELVIEW);
    gluLookAt(0.0, 0.0, 5.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.)
    
def display():
    global rot
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    glPushMatrix()
    glTranslatef(0.0, 0.0, -1.0);
    glRotatef(rot, 1.0, 0.0, 0.0);
    glRotatef(rot, 0.0, 0.0, 1.0);
    rot += 0.1
    
    renderable.render()
    
    glPopMatrix()
    glFlush()
    glutSwapBuffers()
    glutPostRedisplay()
    
if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('-o', '--operation', dest='operation',
        type='str', default='subtract')
    (options, args) = parser.parse_args()

    renderable = TestRenderable(options.operation)
    
    glutInit()
    glutInitWindowSize(640,480)
    glutCreateWindow("CSG Test")
    glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGBA)
    glutDisplayFunc(display)
     
    init()

    glutMainLoop()
