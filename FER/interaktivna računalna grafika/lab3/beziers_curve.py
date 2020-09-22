import math
import numpy as np
from varijable_krivulja import *
from pyglet.gl import *

animacija = True
vrhovi_koordinate={}
lista_poligona=[]
global ociste, glediste

class Vrh:
    def __init__(self, x, y, z,h):
        self.x = x
        self.y = y
        self.z = z
        self.h = h

class Poligon:
    def __init__(self, v1, v2, v3):
        self.v1=v1
        self.v2=v2
        self.v3=v3

def f_ucitaj_dokument():
    vrhovi_koordinate = {}
    dokument = open("kocka.obj", "r").readlines()
    brojac_vrhova = 0
    for linija in dokument:
        if (linija.startswith('#') or linija.startswith('g')):
            continue

        if (linija.startswith('v')):
            brojac_vrhova += 1
            vrhovi_koordinate[brojac_vrhova] = (
                Vrh(float(linija.split()[1]), float(linija.split()[2]), float(linija.split()[3].strip()), float(1)))

        if (linija.startswith('f')):
            p = Poligon(int(linija.split()[1]), int(linija.split()[2]), int(linija.split()[3].strip()))
            lista_poligona.append(p)

    return vrhovi_koordinate, lista_poligona

def ucitaj_raspon(vrhovi_koordinate):
    xmin = min(vrhovi_koordinate.items(), key=lambda x: x[1].x)[1].x
    xmax = max(vrhovi_koordinate.items(), key=lambda x: x[1].x)[1].x
    ymin = min(vrhovi_koordinate.items(), key=lambda x: x[1].y)[1].y
    ymax = max(vrhovi_koordinate.items(), key=lambda x: x[1].y)[1].y
    zmin = min(vrhovi_koordinate.items(), key=lambda x: x[1].z)[1].z
    zmax = max(vrhovi_koordinate.items(), key=lambda x: x[1].z)[1].z
    return xmin, xmax, ymin, ymax, zmin, zmax

def postavi_parametre():
    window.clear()
    glColor3f(0.0, 2.0, 1.0)
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-1, 1, -1, 1)
    glMatrixMode(GL_MODELVIEW)

def nacrtaj (x1,y1,x2,y2):
    glBegin(GL_LINES)
    glVertex2f(x1, y1)
    glVertex2f(x2, y2)
    glEnd()

def matrica_transformacije_pogleda_T(ociste, glediste):
    # pomak T1 ishodista u 0
    T1 = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [-ociste.x, -ociste.y, -ociste.z, 1]])
    G1 = Vrh(glediste.x - ociste.x, glediste.y - ociste.y, glediste.z - ociste.z, 1.0)

    # T2 rotacija za kut a oko z osi
    if (G1.x != 0 or G1.y != 0):
        sina = float(G1.y / math.sqrt(math.pow(G1.x, 2) + math.pow(G1.y, 2)))
        cosa = float(G1.x / math.sqrt(math.pow(G1.x, 2) + math.pow(G1.y, 2)))
        T2 = np.array([[cosa, -sina, 0, 0], [sina, cosa, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
        G2 = Vrh(math.sqrt(math.pow(G1.x, 2) + math.pow(G1.y, 2)), 0.0, G1.z, 1.0)
    else:
        T2 = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
        G2 = Vrh(G1.x, G1.y, G1.z, G1.h)

    # t3 rotacija za kut b ok y osi
    if (G1.x != 0 or G1.z != 0):
        sinb = float(G2.x / math.sqrt(math.pow(G2.x, 2) + math.pow(G2.z, 2)))
        cosb = float(G2.z / math.sqrt(math.pow(G2.x, 2) + math.pow(G2.z, 2)))
        T3 = np.array([[cosb, 0, sinb, 0], [0, 1, 0, 0], [-sinb, 0, cosb, 0], [0, 0, 0, 1]])
        G3 = Vrh(0, 0, math.sqrt(math.pow(G2.x, 2) + math.pow(G2.z, 2)), 1.0)
    else:
        T3 = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
        G3 = Vrh(G2.x, G2.y, G2.z, G2.h)

    # t4 rotaija za 90 oko z osi
    T4 = np.array([[0, -1, 0, 0], [1, 0, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])

    # t5 promjena predznaka na x os
    T5 = np.array([[-1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])

    # generiranje matrice T
    T= T1 @ T2 @ T3 @ T4 @ T5
    return T, G3

def transformacija(T, M):
    tocka_x = T.x * M[0][0] + T.y * M[1][0] + T.z * M[2][0] + T.h * M[3][0]
    tocka_y = T.x * M[0][1] + T.y * M[1][1] + T.z * M[2][1] + T.h * M[3][1]
    tocka_z = T.x * M[0][2] + T.y * M[1][2] + T.z * M[2][2] + T.h * M[3][2]
    tocka_h = T.x * M[0][3] + T.y * M[1][3] + T.z * M[2][3] + T.h * M[3][3]

    tocka = Vrh(tocka_x, tocka_y, tocka_z, tocka_h)

    if (tocka.h!= 1 and tocka.h != 0):
        tocka.x = tocka.x / tocka.h
        tocka.y = tocka.y / tocka.h
        tocka.z = tocka.z / tocka.h
        tocka.h = 1
    return tocka

def primjeni_transformaciju(ociste, glediste,vrhovi_koordinate):
    T, G3 = matrica_transformacije_pogleda_T(ociste, glediste)
    P = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1 / G3.z], [0, 0, 0, 0]])

    # transformacija vrhova
    i = 1
    for vrh in vrhovi_koordinate.values():
        prva = transformacija(vrh, T)
        druga = transformacija(prva, P)
        vrhovi_koordinate[i] = Vrh(druga.x, druga.y, druga.z, druga.h)
        i += 1

    xmin, xmax, ymin, ymax, zmin, zmax = ucitaj_raspon(vrhovi_koordinate)
    srediste = ((xmin + xmax) / 2, (ymin + ymax) / 2, (zmin + zmax) / 2)
    max_raspon = max(xmax - xmin, ymax - ymin, zmax - zmin)
    i = 1
    for vrh in vrhovi_koordinate.values():
        vrhovi_koordinate[i] = Vrh((vrh.x - srediste[0]) * 2 / max_raspon, (vrh.y - srediste[1]) * 2 / max_raspon,
                                   (vrh.z - srediste[2]) * 2 / max_raspon, vrh.h)
        i += 1


def compute_b(n, t):
    b = []
    for i in range(n):
        b.append((math.factorial(n-1) / (math.factorial(i) * math.factorial(n-1-i))) * math.pow(t, i) * math.pow(1 - t, n-1-i))
    return b

def draw_bezier(points, n):
    glBegin(GL_LINE_STRIP)
    for t in np.arange(0,1,0.01):
        p = Vrh(0, 0, 0, 1)
        b = compute_b(n, t)
        for j in range(0, n):
            p.x += points[j].x * b[j]
            p.y += points[j].y * b[j]
            p.z += points[j].z * b[j]
        glVertex2f(p.x, p.y)
    glEnd()

def izracunaj_srediste(tocke):
    A = np.array(tocke)
    minimum = A.argmin(0)
    maximum = A.argmax(0)
    xmin = float(tocke[minimum[0]][0])
    xmax = float(tocke[maximum[0]][0])
    ymin = float(tocke[minimum[1]][1])
    ymax = float(tocke[maximum[1]][1])
    zmin = float(tocke[minimum[2]][2])
    zmax = float(tocke[maximum[2]][2])
    srediste = (float(xmin + xmax) / 2, float(ymin + ymax) / 2, float(zmin + zmax) / 2)
    max_raspon = max(float(xmax - xmin), float(ymax - ymin), float(zmax - zmin))
    return max_raspon,srediste


vrhovi_koordinate, lista_poligona=f_ucitaj_dokument()
xmin, xmax, ymin, ymax, zmin, zmax = ucitaj_raspon(vrhovi_koordinate)
srediste = ((xmin + xmax) / 2, (ymin + ymax) / 2, (zmin + zmax) / 2)
max_raspon = max(xmax - xmin, ymax - ymin, zmax - zmin)
glediste=Vrh(srediste[0],srediste[1], srediste[2], 1)
ociste=Vrh(0,0,0,0)

points=[]
max_raspon,srediste = izracunaj_srediste(tocke)
for tocka in tocke:
    points.append(Vrh((tocka[0] - srediste[0]) * 2 / max_raspon, (tocka[1] - srediste[1]) * 2 / max_raspon,
                  (tocka[2] - srediste[2]) * 2 / max_raspon, 1))

def nacrtaj1(vrh_1, vrh_2,vrh_3):
    a = (vrh_2.y - vrh_1.y) * (vrh_3.z - vrh_1.z) - (vrh_2.z - vrh_1.z) * (vrh_3.y - vrh_1.y)
    b = -(vrh_2.x - vrh_1.x) * (vrh_3.z - vrh_1.z) + (vrh_2.z - vrh_1.z) * (vrh_3.x - vrh_1.x)
    c = (vrh_2.x - vrh_1.x) *(vrh_3.y - vrh_1.y) - (vrh_2.y - vrh_1.y) * (vrh_3.x - vrh_1.x)
    d = -vrh_1.x * a - vrh_1.y * b - vrh_1.z * c

    if (a * ociste.x + b * ociste.y + c * ociste.z + d < 0):
            return

    glColor3f(0.0, 1.0, 1.0)
    glBegin(GL_LINE_LOOP)
    glColor3f(1.0, 1.0, 1.0)
    glVertex2f(vrh_1.x, vrh_1.y)
    glVertex2f(vrh_2.x, vrh_2.y)
    glVertex2f(vrh_3.x, vrh_3.y)
    glEnd()

t=0
def update(dt):
    global vrhovi_koordinate, t, ociste
    vrhovi_koordinate.clear()
    p = Vrh(0, 0, 0, 1)
    b = compute_b(len(points), t)
    t += 0.01
    for j in range(0, len(points)):
        p.x += points[j].x * b[j]
        p.y += points[j].y * b[j]
        p.z += points[j].z * b[j]
    ociste = Vrh(p.x, p.y, p.z, 1)
    vrhovi_koordinate, lista_poligona = f_ucitaj_dokument()
    primjeni_transformaciju(ociste, glediste, vrhovi_koordinate)

window =pyglet.window.Window()
width=window.get_size()[0]
height=window.get_size()[1]

@window.event
def on_draw():
    global animacija
    postavi_parametre()
    if (not animacija):
        for i in range(len(points) - 1):
            nacrtaj(points[i].x, points[i].y, points[i + 1].x, points[i + 1].y)
        draw_bezier(points, len(points))
        animacija = True
    else:
        for l in lista_poligona:
            vrh_1 = vrhovi_koordinate.get(l.v1)
            vrh_2 = vrhovi_koordinate.get(l.v2)
            vrh_3 = vrhovi_koordinate.get(l.v3)
            nacrtaj1(vrh_1, vrh_2, vrh_3)
        glFlush()



pyglet.clock.schedule_interval(update, 1/60)
pyglet.app.run()
