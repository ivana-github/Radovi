from pyglet.gl import *
from pyglet.window import mouse
global y3 , y4 , a , korekcija

def draw_line(x1, y1, x2, y2):
    glBegin(GL_LINES)
    glVertex2i(x1, y1 + 20)
    glVertex2i(x2, y2 + 20)
    glEnd()
def nacrtaj_do_90(x1,y1,x2,y2):
    if(y2-y1<=x2-x1):
        a=2*(y2-y1) #nagib pravca, vrijednost koju dodajemo y u svakom koraku
        y3=y1  #početna vrijednost prvog y
        y4=-(x2-x1) #provjera možemo li osvjetliti pixel
        korekcija=-2*(x2-x1) #ako smo osvjetlili pixel tj pomaknuli y trebamo napraviti korekciju unutar y4
        for xx in range(x1,x2,1):
            glVertex2i(xx, y3)
            y4 = y4 + a
            if (y4 >= 0):
                y4 = y4 + korekcija
                y3 = y3 + 1
    else:
        x2,y2=y2,x2
        x1,y1=y1,x1
        y3=y1
        a = 2 * (y2 - y1)
        y4=-(x2-x1)
        korekcija=-2*(x2-x1)
        for xx in range (x1,x2,1):
            glVertex2i(y3,xx)
            y4 = y4 + a
            if (y4>=0):
                y4 = y4 + korekcija
                y3 = y3 + 1

def nacrtaj_do_minus_90(x1,y1,x2,y2):
    if(-(y2-y1)<=x2-x1):
        a=2*(y2-y1)
        y3=y1
        y4=(x2-x1)
        korekcija=2*(x2-x1)
        for xx in range(x1,x2,1):
            glVertex2i(xx, y3)
            y4=y4+a
            if(y4<=0):
                y4=y4+korekcija
                y3=y3-1
    else:
        x2,y1=y1,x2
        x1,y2=y2,x1
        a=2*(y2-y1)
        y3=y1
        y4=(x2-x1)
        korekcija=2*(x2-x1)
        for xx in range (x1,x2,1):
            glVertex2i(y3,xx)
            y4=y4+a
            if(y4<=0):
                y4=y4+korekcija
                y3=y3-1

def nacrtaj (x1,y1,x2,y2):
    draw_line(x1,y1,x2,y2)
    glBegin(GL_POINTS)
    if(x1<=x2) & (y1<=y2):
        nacrtaj_do_90(x1,y1,x2,y2)
    elif(x1<=x2) & (y1>y2):
        nacrtaj_do_minus_90(x1, y1, x2, y2)
    elif(x1>x2)&(y1>=y2):
        nacrtaj_do_90(x2, y2, x1, y1)
    else:
        nacrtaj_do_minus_90(x2, y2, x1, y1)
    glEnd()

tocke=[]
window =pyglet.window.Window()
#window.push_handlers(pyglet.window.event.WindowEventLogger())

@window.event
def on_mouse_press(x, y, button, modifiers):
    if button == mouse.LEFT:
        tocke.append((x,y))
        if(len(tocke)==2):
            nacrtaj(tocke[0][0],tocke[0][1],tocke[1][0],tocke[1][1])

pyglet.app.run()
