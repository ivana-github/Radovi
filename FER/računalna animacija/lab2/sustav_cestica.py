from pyglet.gl import *
from pyglet.window import key
import random

width = 1000
height = 600

config = pyglet.gl.Config(double_buffer=True)
window = pyglet.window.Window(width=width, height=height, config=config)


class Cestica:
    def __init__(self, img, x, y, batch, skaliranje):
        self.sprite = pyglet.sprite.Sprite(img=img, x=x, y=y, batch=batch)
        self.sprite.scale = skaliranje

        self.vekrot_x = random.uniform(-3, 3)
        self.vekrot_y = random.uniform(-3, 3)


@window.event
def on_draw():
    window.clear()
    batch.draw()


def update(interval, broj_cestica_u_batchu):
    global lista_cestica
    for cestica in lista_cestica:
        cestica.sprite.opacity *= 0.98
        cestica.sprite.x += cestica.vekrot_x + x_smjer_sirenja
        cestica.sprite.y += cestica.vekrot_y + y_smjer_sirenja

        if (cestica.sprite.opacity < prag_prozirnosti):
            lista_cestica.remove(cestica)

    lista_cestica.extend(
        [Cestica(img=img, x=x_izvor, y=y_izvor, batch=batch, skaliranje=0.2) for _ in range(broj_cestica_u_batchu)])


@window.event
def on_key_press(symbol, modifiers):
    global x_izvor, y_izvor, broj_cestica_u_batchu, prag_prozirnosti, y_smjer_sirenja, x_smjer_sirenja

    if symbol == key.NUM_8:
        y_izvor = min(y_izvor + 15, height)
        y_smjer_sirenja = min(y_smjer_sirenja + 5, 50)
    elif symbol == key.NUM_2:
        y_izvor = max(y_izvor - 15, 0)
        y_smjer_sirenja = max(y_smjer_sirenja - 5, -50)
    elif symbol == key.NUM_6:
        x_izvor = min(x_izvor + 15, width)
        x_smjer_sirenja = min(x_smjer_sirenja + 5, 255)
    elif symbol == key.NUM_4:
        x_izvor = max(x_izvor - 15, 0)
        x_smjer_sirenja = max(x_smjer_sirenja - 5, -255)
    elif symbol == key.NUM_1:
        x_smjer_sirenja = max(x_smjer_sirenja - 5, -255)
        y_smjer_sirenja = max(y_smjer_sirenja - 5, -50)
    elif symbol == key.NUM_3:
        y_smjer_sirenja = max(y_smjer_sirenja - 5, -50)
        x_smjer_sirenja = min(x_smjer_sirenja + 5, 255)
    elif symbol == key.NUM_7:
        x_smjer_sirenja = max(x_smjer_sirenja - 5, -255)
        y_smjer_sirenja = min(y_smjer_sirenja + 5, 50)
    elif symbol == key.NUM_9:
        y_smjer_sirenja = min(y_smjer_sirenja + 5, 50)
        x_smjer_sirenja = min(x_smjer_sirenja + 5, 255)

    elif symbol == key.NUM_ADD:
        broj_cestica_u_batchu = min(broj_cestica_u_batchu + 1, 30)
    elif symbol == key.NUM_SUBTRACT:
        broj_cestica_u_batchu = max(broj_cestica_u_batchu - 1, 0)
    elif symbol == key.NUM_DIVIDE:
        prag_prozirnosti = min(prag_prozirnosti + 20, 255)
    elif symbol == key.NUM_MULTIPLY:
        prag_prozirnosti = max(prag_prozirnosti - 20, 0)


if __name__ == "__main__":
    lista_cestica = []

    x_izvor, y_izvor = width / 2, height / 2
    x_smjer_sirenja, y_smjer_sirenja = 0, 0

    prag_prozirnosti = 80

    img = pyglet.image.load("snow.bmp")

    batch = pyglet.graphics.Batch()

    pyglet.clock.schedule_interval(update, interval=1 / 30., broj_cestica_u_batchu=5)

    pyglet.app.run()
