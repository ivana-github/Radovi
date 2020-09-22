from pyglet.gl import *
from pyglet.window import mouse
from varijable import *
'Primjer datoteke varijable.py' \
'is_file = False ' \
'n = 3 '\
'tocke = [(0, 0), (10, 100), (200, 300)] '\
'V = (40,200)'
'ako je is_file False onda se ucitava preko tipkovnice'
a=[]
b=[]
c=[]
if is_file:
    print("Podatci učitani iz datoteke varijable.py")
else:
    tocke = []
    n = input("Unesi broj vrhova\n")
    n = int(n)
    print("U smjeru kazaljke na sat mišem zadaj ", n, " vrhova")

window =pyglet.window.Window()

def izracunaj_koef (tocke, n):
    i0=n-1
    print("Koeficjenti jednadžbi bridova a,b,c :")
    for i in range(n):
        a.insert(int(i0), (tocke[i0][1] - tocke[i][1]))
        b.insert(i0, -(tocke[i0][0] - tocke[i][0]))
        c.insert(i0, (tocke[i0][0]*tocke[i][1])-(tocke[i0][1]*tocke[i][0]))
        i0 = i
    for i in range(n):
        print("Brid ", i+1,": ",a[i], ", ", b[i], ", ", c[i])
    return a,b,c

def nacrtaj (x1,y1,x2,y2):
    glBegin(GL_LINES)
    glVertex2f(x1, y1)
    glVertex2f(x2, y2)
    glEnd()

def ispitaj_odnos(x,y, a, b, c, n):
    unutar=0
    for i in range(n):
        if(((x*a[i])+(y*b[i])+c[i])>0):
            unutar=1
            print("TOČKA V JE IZVAN POLIGONA !")
            break
    if(unutar==0):
        print("TOČKA V JE UNUTAR POLIGONA !")

@window.event
def on_mouse_press(x, y, button, modifiers):
    if button == mouse.LEFT:
        if not is_file:
            tocke.append((x,y))
        if(len(tocke)==n):
            i0 = n - 1
            for i in range (n):
                nacrtaj(tocke[i0][0],tocke[i0][1],tocke[i][0],tocke[i][1])
                i0 = i
            if is_file:
                tocke.append((V[0], V[1]))

        if(len(tocke)== n+1):
            glBegin(GL_POINTS)
            glColor3f(1.0, 0.0, 0.0)
            glVertex2f(tocke[n][0], tocke[n][1])
            glEnd()
            a, b, c = izracunaj_koef(tocke, n)
            ispitaj_odnos(tocke[n][0], tocke[n][1], a, b, c, n)
            Y0=(min(tocke[:-1], key = lambda x:x[1])[1],max(tocke[:-1], key=lambda x: x[1])[1])
            for i in range(Y0[0],Y0[1]):
                l = min(tocke[:-1], key=lambda x: x[0])[0]
                d = max(tocke[:-1], key=lambda x: x[0])[0]
                for j in range(n):
                    if (a[j] != 0):
                        sjeciste=(-b[j]*i - c[j])/float(a[j]) #x-koordinata sjecista j-tog brida i tocke Yi
                        if(tocke[j][1]< tocke[j+1][1]):
                            if (sjeciste> l):
                                l=sjeciste
                        elif (sjeciste < d):
                            d=sjeciste
                if (l < d):
                    glBegin(GL_LINES)
                    #glColor3f(0.0, 0.0, 1.0)
                    glVertex2f(float(l), i)
                    glVertex2f(float(d), i)
                    glEnd()

pyglet.app.run()
