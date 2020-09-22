import random

from pyglet.gl import *
from pyglet.window import mouse
import numpy as np
import random
vrhovi_koordinate={}
brojac_vrhova=0
brojac_poligona=0
lista_poligona=[]
a=[]
b=[]
d=[]
c=[]

dokument=open("tetrahedorn.obj", "r").readlines()

class Vrh:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

class Poligon:
    def __init__(self, v1, v2, v3):
        self.v1=v1
        self.v2=v2
        self.v3=v3

for linija in dokument:
    if(linija.startswith('#') or linija.startswith('g')):
        continue
    if(linija.startswith('v')):
        brojac_vrhova += 1
        vrhovi_koordinate[brojac_vrhova] = (Vrh(float(linija.split()[1]), float(linija.split()[2]), float(linija.split()[3].strip())) )
for linija in dokument:
    if (linija.startswith('#') or linija.startswith('g')):
        continue
    if (linija.startswith('f')):
        brojac_poligona += 1
        p = Poligon(int(linija.split()[1]), int(linija.split()[2]), int(linija.split()[3].strip()))
        lista_poligona.append(p)
        a.append((vrhovi_koordinate[p.v2].y - vrhovi_koordinate[p.v1].y)*(vrhovi_koordinate[p.v3].z - vrhovi_koordinate[p.v1].z) - (vrhovi_koordinate[p.v2].z - vrhovi_koordinate[p.v1].z)*(vrhovi_koordinate[p.v3].y - vrhovi_koordinate[p.v1].y))
        b.append( -1*(vrhovi_koordinate[p.v2].x -vrhovi_koordinate[p.v1].x)*(vrhovi_koordinate[p.v3].z-vrhovi_koordinate[p.v1].z + (vrhovi_koordinate[p.v2].z-vrhovi_koordinate[p.v1].z)*(vrhovi_koordinate[p.v3].x-vrhovi_koordinate[p.v1].x)) )
        c.append( (vrhovi_koordinate[p.v2].x -vrhovi_koordinate[p.v1].x)*(vrhovi_koordinate[p.v3].y -vrhovi_koordinate[p.v1].y) - (vrhovi_koordinate[p.v2].y -vrhovi_koordinate[p.v1].y)*(vrhovi_koordinate[p.v3].x -vrhovi_koordinate[p.v1].x))
        d.append(-1*((vrhovi_koordinate[p.v1].x)*a[brojac_poligona-1]) - ((vrhovi_koordinate[p.v1].y)*b[brojac_poligona-1]) - ((vrhovi_koordinate[p.v1].z)*c[brojac_poligona-1]))

xmin=min(vrhovi_koordinate.items(), key=lambda x: x[1].x)[1].x
xmax=max(vrhovi_koordinate.items(), key=lambda x: x[1].x)[1].x
ymin=min(vrhovi_koordinate.items(), key=lambda x: x[1].y)[1].y
ymax=max(vrhovi_koordinate.items(), key=lambda x: x[1].y)[1].y
zmin=min(vrhovi_koordinate.items(), key=lambda x: x[1].z)[1].z
zmax=max(vrhovi_koordinate.items(), key=lambda x: x[1].z)[1].z

print("Broj vrhova : ", brojac_vrhova, "\nBroj poligona : ", brojac_poligona)

srediste=((xmin+xmax)/2, (ymin+ymax)/2, (zmin+zmax)/2)
max_raspon=max(xmax-xmin,ymax-ymin,zmax-zmin)

print("Srediste tijela :",srediste)

'for vrh in vrhovi_koordinate.values(): '\
    'print(vrh.x, vrh.y, vrh.z) '
#prebaci srediste u sredinu koordinatnog sustava
i=1
for vrh in vrhovi_koordinate.values():
    vrhovi_koordinate[i]=Vrh((vrh.x -srediste[0])*2/max_raspon, (vrh.y -srediste[1])*2/max_raspon, (vrh.z -srediste[2])*2/max_raspon)
    i+=1


unutar=0
var=input("Unesi koordinate točke V x,y,z odvojene zarezom\n")
s=var.split(",")
s=np.array(s,float)

for i in range(brojac_poligona):
    if( a[i]*s[0] + b[i]*s[1] + c[i]*s[2] + d[i] > 0):
        unutar=1
        print("TOČKA V JE IZVAN TIJELA !")
        break
if(unutar==0):
        print("TOČKA V JE UNUTAR TIJELA !")


window =pyglet.window.Window()
width=window.get_size()[0]
height=window.get_size()[1]

def postavi_parametre():
    glColor3f(0.0, 2.0, 1.0)
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-1, 1, -1, 1)



def get_random_color():
    return [random.random(),random.random(),random.random()]

def nacrtaj(vrh_1, vrh_2,vrh_3):
    glBegin(GL_TRIANGLE_FAN)
    glColor3f(0.0, 2.0, 1.0)
    color=get_random_color()
    glColor3f(color[0],color[1],color[2])
    glVertex2f(vrh_1.x /1.1, vrh_1.y /1.1)
    glVertex2f(vrh_2.x /1.1, vrh_2.y /1.1)
    glVertex2f(vrh_3.x /1.1, vrh_3.y /1.1)
    glEnd()

    glColor3f(0.0, 1.0, 1.0)

    color=get_random_color()
    glColor3f(color[0],color[1],color[2])
    glBegin(GL_LINE_LOOP)
    glColor3f(1.0, 1.0, 1.0)
    glVertex2f(vrh_1.x / 1.1, vrh_1.y / 1.1)
    glVertex2f(vrh_2.x / 1.1, vrh_2.y / 1.1)
    glVertex2f(vrh_3.x / 1.1, vrh_3.y / 1.1)
    glEnd()


@window.event
def on_draw():
    postavi_parametre()

    for l in lista_poligona:
        vrh_1 = vrhovi_koordinate.get(l.v1)
        vrh_2 = vrhovi_koordinate.get(l.v2)
        vrh_3 = vrhovi_koordinate.get(l.v3)
        nacrtaj(vrh_1, vrh_2,vrh_3)

pyglet.app.run()
