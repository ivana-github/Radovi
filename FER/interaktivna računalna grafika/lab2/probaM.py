from pyglet.gl import *
from pyglet.window import key
from pyglet.window import mouse
import random

class Coefs:
    def __init__(self,a,b,c,d):
        self.a=a
        self.b=b
        self.c=c
        self.d=d

class CenterValues:
    def __init__(self,x,y,z):
        self.xs=x
        self.ys=y
        self.zs=z

window = pyglet.window.Window()

vertices = [];
polygons = [];
coefs=[]
maxmin=[]

width=window.get_size()[0]
height=window.get_size()[1]

@window.event
def on_show():

	file='teddy.obj'
    readFile(file)
    convert_coordinates()
    calculateCoefs()

@window.event
def on_draw():
    glColor3f(1.0,0.0,0.0)
    glViewport(0,0,width,height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    minx=maxmin[0]
    miny=maxmin[1]
    minz=maxmin[2]
    maxx=maxmin[3]
    maxy=maxmin[4]
    maxz=maxmin[5]
    gluOrtho2D(-1,1,-1,1)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glClearColor(0.0, 0.0, 0.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)
    glPointSize(1.0)
    glColor3f(1.0,0.0,0.0)

    print("Pritisnite ekran za testiranje tocke")

    draw_all_polygons()

@window.event
def on_mouse_press(x,y,button,modifiers):
    if button & mouse.LEFT:
        test_point()

@window.event
def on_resize(w,h):
    width=w
    height=h
    glViewport(0,0,width,height)
    glMatrixMode(gl.GL_PROJECTION)
    gluOrtho2D(-1,1,-1,1)
    glLoadIdentity()
    glMatrixMode(gl.GL_MODELVIEW)

@window.event
def on_close():
    window.close()


def convert_coordinates():
    xs = (maxmin[3] + maxmin[0]) / 2.0
    ys = (maxmin[1] + maxmin[4]) / 2.0
    zs = (maxmin[2] + maxmin[5]) / 2.0

    for v in vertices:
        v[0]=v[0]-xs
        v[1]=v[1]-ys
        v[2]=v[2]-zs
    m=max(maxmin[3]-maxmin[0], maxmin[4]-maxmin[1], maxmin[5]-maxmin[2])
    k=2/m
    for v in vertices:
        v[0]=v[0]*k
        v[1]=v[1]*k
        v[2]=v[2]*k
    for i in maxmin:
        i*=k


def draw_all_polygons():
    for p in polygons:
        polygon=[]
        for i in p:
            polygon.append(vertices[i-1])
        draw_polygon(polygon)

#draw a single polygon
def draw_polygon(pol):
    color=get_random_color()
    glColor3f(color[0],color[1],color[2]);
    glPolygonMode(GL_FRONT, GL_FILL);
    glBegin(GL_TRIANGLES)
    for i in range(len(pol)):
        v1=pol[i]
        glVertex2f(v1[0], v1[1])
    glEnd()

def get_random_color():
    return [random.random(),random.random(),random.random()]

def readFile(file):
    with open(file, 'r') as fp:
        vC = 0
        for line in fp:
            if (line.startswith('#')):
                continue
            splitted = line.split(' ')
            if (line.startswith('v')):
                splitted.remove('v')
                x = float(splitted[0])
                y = float(splitted[1])
                z = float(splitted[2])
                if (vC == 0):
                    xmin = xmax = x
                    ymin = ymax = y
                    zmin = zmax = z
                    vC += 1
                else:
                    if (xmin > x):
                        xmin = x
                    if (ymin > y):
                        ymin = y
                    if (zmin > z):
                        zmin = z
                    if (xmax < x):
                        xmax = x
                    if (ymax < y):
                        ymax = y
                    if (zmax < z):
                        zmax = z
                vertices.append([x, y, z])
            elif (line.startswith('f')):
                splitted.remove('f')
                polygons.append([int(j) for j in splitted])

    for i in [xmin, ymin, zmin, xmax, ymax, zmax]:
        maxmin.append(i)

#calculating center coordinates

def calculateCoefs():
    for pol in polygons:
        v1 = vertices[pol[0] - 1]
        v2 = vertices[pol[1] - 1]
        v3 = vertices[pol[2] - 1]
        a = (v2[1] - v1[1]) * (v3[2] - v1[2]) - (v2[2] - v1[2]) * (v3[1] - v1[1])
        b = -(v2[0] - v1[0]) * (v3[2] - v1[2]) + (v2[2] - v1[2]) * (v3[0] - v1[0])
        c = (v2[0] - v1[0]) * (v3[1] - v1[1]) - (v2[1] - v1[1]) * (v3[0] - v1[0])
        d = -v1[0] * a - v1[1] * b - v1[2] * c

        coefs.append(Coefs(a, b, c, d))

def test_point():
    point=get_point()
    if (is_inside_polygon(point)):
        print("Tocka je unutar tijela")
    else:
        print("Tocka je izvan tijela")

def get_point():
    print("Unesite koordinate ispitne tocke: ")
    x=float(input("x: "))
    y=float(input("y: "))
    z=float(input("z: "))
    return [x,y,z]

def is_inside_polygon(point):
    for c in coefs:
        res = c.a*point[0]+ c.b*point[1] + c.c*point[2] + c.d;
        if (res > 0):
            return False
    return True

pyglet.app.run()
