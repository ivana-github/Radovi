import math
from pyglet.gl import *
from pyglet.window import key
from pyglet.window import mouse
import numpy as np
from numpy import linalg as LA

global vrhovi_koordinate
lista_poligona=[]
global ociste, glediste, izvor
global vrh_normala
vrh_normala = {}

class Vrh:
    def __init__(self, x, y, z,h):
        self.x = x
        self.y = y
        self.z = z
        self.h = h

    def __hash__(self):
        return hash((self.x, self.y, self.z))

class Poligon:
    def __init__(self, v1, v2, v3):
        self.v1=v1
        self.v2=v2
        self.v3=v3

class N_normala:
    def __init__(self, n1, n2, n3):
        self.n1 = n1
        self.n2 = n2
        self.n3 = n3

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

def ucitaj_raspon(vrhovi_koordinate):
    xmin = min(vrhovi_koordinate.items(), key=lambda x: x[1].x)[1].x
    xmax = max(vrhovi_koordinate.items(), key=lambda x: x[1].x)[1].x
    ymin = min(vrhovi_koordinate.items(), key=lambda x: x[1].y)[1].y
    ymax = max(vrhovi_koordinate.items(), key=lambda x: x[1].y)[1].y
    zmin = min(vrhovi_koordinate.items(), key=lambda x: x[1].z)[1].z
    zmax = max(vrhovi_koordinate.items(), key=lambda x: x[1].z)[1].z
    print("Tijelo se prostire x=[", xmin, ",", xmax, "] y=[", ymin, ",", ymax, "] z=[", zmin, ",", zmax, "]")
    return xmin, xmax, ymin, ymax, zmin, zmax

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

def izracunaj_intenzitet(norma_n, norma_l):
    Ia, ka, Ii, kd = 50, 0.7, 255, 0.8

    Ig = Ia * ka
    Ii_kd = Ii * kd

    Id1 = Ii_kd * max(0, np.dot(norma_n.n1, norma_l.n1)) + Ig
    Id2 = Ii_kd * max(0, np.dot(norma_n.n2, norma_l.n2)) + Ig
    Id3 = Ii_kd * max(0, np.dot(norma_n.n3, norma_l.n3)) + Ig

    return Id1, Id2, Id3

def normala_poligona(vrh_1, vrh_2,vrh_3):
    a = (vrh_2.y - vrh_1.y) * (vrh_3.z - vrh_1.z) - (vrh_2.z - vrh_1.z) * (vrh_3.y - vrh_1.y)
    b = -(vrh_2.x - vrh_1.x) * (vrh_3.z - vrh_1.z) + (vrh_2.z - vrh_1.z) * (vrh_3.x - vrh_1.x)
    c = (vrh_2.x - vrh_1.x) * (vrh_3.y - vrh_1.y) - (vrh_2.y - vrh_1.y) * (vrh_3.x - vrh_1.x)
    return a, b, c

def normala_vektora(vrhovi_koordinate, lista_poligona):
    global vrh_normala
    for vrh in vrhovi_koordinate.values():
        vrh_normala[(vrh.__hash__())] = np.array([float(0), float(0), float(0)])

    for i in range(len(vrhovi_koordinate)):
        brojac = 0
        vrh = vrhovi_koordinate.get(i+1)
        for polygon in lista_poligona:
            if (i+1) in (polygon.v1, polygon.v2, polygon.v3):
                a, b, c = normala_poligona(vrhovi_koordinate.get(polygon.v1), vrhovi_koordinate.get(polygon.v2), vrhovi_koordinate.get(polygon.v3) )
                brojac += 1

                normala = [a, b, c] / LA.norm([a, b, c])
                vrh_normala[(vrh.__hash__())] += [float(normala[0]), float(normala[1]), float(normala[2])]

        vrh_normala[(vrh.__hash__())] /= brojac

        if LA.norm(vrh_normala[(vrh.__hash__())]) != 0:
            vrh_normala[(vrh.__hash__())] /= LA.norm(vrh_normala[(vrh.__hash__())]) #korjen iz x,y,z na kvadrat


#-------------------------------------------------------------------


vrhovi_koordinate, lista_poligona=f_ucitaj_dokument()
xmin, xmax, ymin, ymax, zmin, zmax = ucitaj_raspon(vrhovi_koordinate)

ociste = Vrh(float(7), float(6), float(4), float(1))
glediste = Vrh(float(0.5), float(0.5), float(0.5), float(1))
izvor = Vrh(2, 3, 2.8, 1)

print("glediste:", glediste.x,glediste.y,glediste.z)
print("ociste:" , ociste.x, ociste.y, ociste.z )
print("izvor: ",izvor.x, izvor.y ,izvor.z)
primjeni_transformaciju(ociste, glediste,vrhovi_koordinate)
normala_vektora(vrhovi_koordinate, lista_poligona)

window = pyglet.window.Window()
width = window.get_size()[0]
height = window.get_size()[1]


def postavi_parametre():
    window.clear()
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-1, 1, -1, 1)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()


def nacrtaj(vrh_1, vrh_2, vrh_3):
    a, b, c = normala_poligona(vrh_1, vrh_2, vrh_3)
    d = -vrh_1.x * a - vrh_1.y * b - vrh_1.z * c

    if (a * ociste.x + b * ociste.y + c * ociste.z + d < 0):
        return

    norma_n = N_normala(vrh_normala[vrh_1.__hash__()],vrh_normala[vrh_2.__hash__()],vrh_normala[vrh_3.__hash__()])

    l1 = [izvor.x - vrh_1.x, izvor.y - vrh_1.y, izvor.z - vrh_1.z] / LA.norm([izvor.x - vrh_1.x, izvor.y - vrh_1.y, izvor.z - vrh_1.z])
    l2 = [izvor.x - vrh_2.x, izvor.y - vrh_2.y, izvor.z - vrh_2.z] / LA.norm([izvor.x - vrh_2.x, izvor.y - vrh_2.y, izvor.z - vrh_2.z])
    l3 = [izvor.x - vrh_3.x, izvor.y - vrh_3.y, izvor.z - vrh_3.z] / LA.norm([izvor.x - vrh_3.x, izvor.y - vrh_3.y, izvor.z - vrh_3.z])
    norma_l = N_normala(l1, l2, l3)
    I = izracunaj_intenzitet(norma_n, norma_l)
    print(I)
    glBegin(GL_TRIANGLES)
    glColor3f(I[0]/255, I[0]/255, I[0]/255)
    glVertex2f(vrh_1.x, vrh_1.y)
    glColor3f(I[1] / 255, I[1] / 255, I[1] / 255)
    glVertex2f(vrh_2.x, vrh_2.y)
    glColor3f(I[1] / 255, I[1] / 255, I[1] / 255)
    glVertex2f(vrh_3.x, vrh_3.y)
    glEnd()

    glBegin(GL_LINE_LOOP)
    glColor3f(1.0, 1.0, 1.0)
    glVertex2f(vrh_1.x, vrh_1.y)
    glVertex2f(vrh_2.x, vrh_2.y)
    glVertex2f(vrh_3.x, vrh_3.y)
    glEnd()

@window.event
def on_resize(w,h):
    window.clear()
    width = w
    height = h
    glViewport(0, 0, width, height)
    glMatrixMode(gl.GL_PROJECTION)
    gluOrtho2D(-1, 1, -1, 1)
    glLoadIdentity()
    glMatrixMode(gl.GL_MODELVIEW)

def update():
    global vrhovi_koordinate, vrh_normala
    vrhovi_koordinate.clear()
    vrh_normala.clear()
    vrhovi_koordinate, lista_poligona = f_ucitaj_dokument()
    primjeni_transformaciju(ociste, glediste, vrhovi_koordinate)
    normala_vektora(vrhovi_koordinate, lista_poligona)

@window.event
def on_draw():
    postavi_parametre()
    for l in lista_poligona:
        vrh_1 = vrhovi_koordinate.get(l.v1)
        vrh_2 = vrhovi_koordinate.get(l.v2)
        vrh_3 = vrhovi_koordinate.get(l.v3)
        nacrtaj(vrh_1, vrh_2, vrh_3)
    glFlush()

@window.event
def on_key_press(symbol, modifiers):
    global vrhovi_koordinate, vrh_normala
    if symbol == key.O:
        ociste.x = ociste.x + 0.5
        update()
    if symbol == key.I:
        ociste.x = ociste.x - 0.5
        update()
    if symbol == key.P:
        ociste.y = ociste.y + 0.5
        update()
    if symbol == key.L:
        ociste.y = ociste.y - 0.5
        update()

    if symbol == key.G:
        glediste.x = glediste.x + 0.5
        update()
    if symbol == key.F:
        glediste.x = glediste.x - 0.5
        update()
    if symbol == key.H:
        glediste.y = glediste.y + 0.5
        update()
    if symbol == key.B:
        glediste.y = glediste.y - 0.5
        update()
pyglet.app.run()






