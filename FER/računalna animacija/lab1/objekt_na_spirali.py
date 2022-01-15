import numpy as np
from pyglet.gl import *
import pywavefront
import random

window = pyglet.window.Window()


def ucitaj_i_prilagodi_objekt(file_name):
    objekt = pywavefront.Wavefront(file_name, collect_faces=True)

    min_koo = (min(objekt.vertices, key=lambda x: x[0])[0], min(objekt.vertices, key=lambda x: x[1])[1],
               min(objekt.vertices, key=lambda x: x[2])[2])
    max_koo = (max(objekt.vertices, key=lambda x: x[0])[0], max(objekt.vertices, key=lambda x: x[1])[1],
               max(objekt.vertices, key=lambda x: x[2])[2])
    raspon_objekta = (min_koo, max_koo)

    skaliranje_objekta = np.full(3, 4 / max(tuple(map(lambda i, j: i - j, max_koo, min_koo))))
    transacija_objekta = list(map(lambda i, j, k: 2 * (i + j) + k, max_koo, min_koo, b_spline))

    return objekt, raspon_objekta, skaliranje_objekta, transacija_objekta


def ucitaj_tocke_spirale(file_name):
    dokument = open(file_name, "r").readlines()
    vrhovi_spirale = []
    for linija in dokument:
        if (linija.startswith('\n')):
            continue
        vrhovi_spirale.append([float(koordinata) for koordinata in linija.split()])
    return np.array(vrhovi_spirale)


def extract(lista, element_liste):
    return np.array([element[element_liste] for element in lista])


def multiply(T, M, r_x, r_y, r_z):
    return [np.dot(np.dot(T, M), r_x), np.dot(np.dot(T, M), r_y),
            np.dot(np.dot(T, M), r_z)]


def kreiraj_spline_krivulju_tocke_tangente_i_derivaciju(vrhovi_spirale):
    b_spline = []
    b_spline_tangenta = []
    b_spline_derivacija = []

    for i in range(len(vrhovi_spirale[:-3])):
        r = vrhovi_spirale[i:i + 4]
        r_x, r_y, r_z = extract(r, 0), extract(r, 1), extract(r, 2)

        for t in np.arange(0, 1 + 1e-10, 0.03):
            T_spline = np.array([t ** 3, t ** 2, t, 1])
            T_spline_tangenta = np.array([t ** 2, t, 1])
            T_spline_derivacija = np.array([t, 1])

            p_spline = multiply(T_spline, M_b_spline, r_x, r_y, r_z)
            p_spline_tangenta = multiply(T_spline_tangenta, M_b_spline_tangenta, r_x, r_y, r_z)
            p_spline_derivacija = multiply(T_spline_derivacija, M_b_spline_normala, r_x, r_y, r_z)

            b_spline.append(p_spline)
            b_spline_tangenta.append(p_spline_tangenta)
            b_spline_derivacija.append(p_spline_derivacija)

    tocke_tangente = np.array(b_spline) + 1/2 * np.array(b_spline_tangenta)

    return np.array(b_spline), np.array(b_spline_tangenta), np.array(b_spline_derivacija), tocke_tangente


def nactraj(prva_tocka, druga_tocka, boja, svaka_n_tocka=1):
    glColor3f(*boja)
    for i in range(0, len(prva_tocka), svaka_n_tocka):
        glBegin(GL_LINES)
        glVertex3f(*prva_tocka[i])
        glVertex3f(*druga_tocka[i])
        glEnd()


def nacrtaj_bspline():
    nactraj(b_spline[:-1], b_spline[1:], [1.0, 0.0, 0.0])


def nacrtaj_tangente():
    nactraj(b_spline[:-1], tocke_tangente[:-1], [0.0, 1.0, 0.0], 10)


def nacrtaj_tocke():
    glColor3f(0.0, 0.0, 1.0)
    glPointSize(5)
    glBegin(GL_POINTS)
    for i in range(0, len(vrhovi_spirale)):
        glVertex3f(*vrhovi_spirale[i])
    glEnd()


def izracunaj_rotaciju(e):
    s = [0, 0, 1]
    os = np.cross(s, e)
    se = np.dot(s, e)

    acos = se / (np.linalg.norm(s) * np.linalg.norm(e))
    acos = 1 if acos > 1 else acos
    acos = -1 if acos < -1 else acos

    fi = 180 * np.arccos(acos) / np.pi

    return (np.array([fi, *os]))


def postavi_parametre():
    window.clear()
    glViewport(0, 0, width, height)
    glLoadIdentity()


def nacrtaj_objekt():
    ist = [0, 0.5, 1, 10, 2]
    x, y, z = random.choice(ist), random.choice(ist), random.choice(ist)

    glBegin(GL_TRIANGLES)
    for mesh in objekt.mesh_list:
        for face in mesh.faces:
            glColor3f(x, y, z)
            for tocka in face:
                glVertex3f(*objekt.vertices[tocka])
    glEnd()


@window.event
def on_resize(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(30, 1.8, .5, 100)
    glMatrixMode(GL_MODELVIEW)

    return pyglet.event.EVENT_HANDLED


@window.event
def on_draw():
    global transacija_objekta

    postavi_parametre()
    gluLookAt(20, 20, 70, -10, -5, 0, 10, 10, 20)  # spirala

    for ind, b in enumerate(b_spline):
        transacija_objekta = list(map(lambda i, j, k: 10 * (i + j + k), raspon_objekta[1], raspon_objekta[0], b))
        rotacija = izracunaj_rotaciju(b_spline_tangenta[ind])

        glClear(GL_COLOR_BUFFER_BIT)

        nacrtaj_bspline()
        nacrtaj_tangente()
        nacrtaj_tocke()

        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glPushMatrix()

        glScalef(*skaliranje_objekta)
        glTranslatef(*transacija_objekta)  # translacija objekta
        glRotatef(*rotacija)  # rotacija objekta
        nacrtaj_objekt()

        glPopMatrix()
        window.flip()

if __name__ == "__main__":
    width = window.get_size()[0]
    height = window.get_size()[1]

    M_b_spline = 1 / 6 * np.array([[-1, 3, -3, 1],
                                   [3, -6, 3, 0],
                                   [-3, 0, 3, 0],
                                   [1, 4, 1, 0]])

    M_b_spline_tangenta = 1 / 2 * np.array([[-1, 3, -3, 1],
                                            [2, -4, 2, 0],
                                            [-1, 0, 1, 0]])

    M_b_spline_normala = np.array([[-1, 3, -3, 1],
                                   [1, -2, 1, 0]])

    vrhovi_spirale = ucitaj_tocke_spirale("spirala.txt")
    b_spline, b_spline_tangenta, b_spline_derivacija, tocke_tangente = kreiraj_spline_krivulju_tocke_tangente_i_derivaciju(vrhovi_spirale)
    objekt, raspon_objekta, skaliranje_objekta, transacija_objekta = ucitaj_i_prilagodi_objekt("teddy.obj")

    pyglet.app.run()
