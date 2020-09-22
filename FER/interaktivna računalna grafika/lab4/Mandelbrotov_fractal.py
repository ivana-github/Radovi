import math
from pyglet.gl import *
from pyglet.window import key
from pyglet.window import mouse
import numpy as np

global tocke
tocke =[]

eps, limit = 100, 16
umin, umax, vmin, vmax = -1.5, 0.5, -1, 1

class C:
    def __init__(self, re, im):
        self.re = re
        self.im = im

class Vrh:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


def divergira_li(c, m):
    z = C(float(0), float(0))
    for i in range(1, m + 1):
        z = C(np.square(z.re) - np.square(z.im)+c.re, 2 * z.re * z.im + c.im)
        if np.square(z.re) + np.square(z.im) > np.square(eps):
            return i
    return -1

def pripremi_za_crtanje():
    global tocke
    for x in range(0, width + 1):
        for y in range(0, height + 1):
            c1 = C(((umax - umin) * x) / width + umin, ((vmax - vmin) * y) / height + vmin)
            k = divergira_li(c1, limit)
            tocke.append(Vrh((x-(width / 2)) * 2 / width, (y - (height / 2)) * 2 / height, k))


window = pyglet.window.Window()
width = window.get_size()[0]
height = window.get_size()[1]
pripremi_za_crtanje()

def postavi_parametre():
    window.clear()
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-1, 1, -1, 1)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glLineWidth(1)

@window.event
def on_draw():
    global tocke
    postavi_parametre()
    for t in tocke:
        glBegin(GL_POINTS)
        if t.z == -1:
            glColor3f(0, 0, 0)
        else:
            glColor3f(t.z / limit, 1 - t.z / limit / 2, 0.8 - t.z / limit / 3)
        glVertex2f(t.x, t.y)
        glEnd()
    print("gotovo")

pyglet.app.run()
