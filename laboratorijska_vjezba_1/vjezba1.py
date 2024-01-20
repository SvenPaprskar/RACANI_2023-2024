import numpy as np
import math
import pyglet.clock
from pyglet.gl import *

matrica1 = np.array([[-1, 3, -3, 1], [3, -6, 3, 0], [-3, 0, 3, 0], [1, 4, 1, 0]])
x = [[0, 0, 0], [0, 10, 5], [10, 10, 10], [10, 0, 15], [0, 0, 20], [0, 10, 25], [10, 10, 30], [10, 0, 35], [0, 0, 40], [0, 10, 45], [10, 10, 50], [10, 0, 55]]

lk = []

lo = []

lv = []

lt = []

end = 0

prozor = pyglet.window.Window()

zeljeno = np.array([0, 0, 1])

lp = []

ltan = []

lmv = []

def update(*par):
    pass

def ucitaj():
    global lv, lp
    with open("tetrahedron.obj", "r") as f:
        sve = [next.strip().split() for next in f.readlines() if next.strip() and not next.startswith(("#", "g"))]
        lv += [list(map(float, iduci[1:4])) for iduci in sve if iduci[0] == "v"]
        lp += [list(map(int, iduci[1:4])) for iduci in sve if iduci[0] == "f"]

@prozor.event
def on_resize(sirina, visina):
    new = sirina
    new2 = visina
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glViewport(0, 0, new, new2)
    aspect_ratio = float(new) / float(new2)
    gluPerspective(55, aspect_ratio, 2, 100)
    glMatrixMode(GL_MODELVIEW)
    glClearColor(1, 1, 1, 1)
    glClear(GL_COLOR_BUFFER_BIT)
    glTranslatef(-5, 3.0, -15.0)
    glRotatef(53, 3, 2, 4)
    glPointSize(1.0)
    return True

def gran(i, podaci):
    if not (0 <= i < len(podaci)):
        raise IndexError(f"Indeks '{i}' je izvan granica.")

def dalje():
    global end
    skal = lt[end][0] / 5
    draw(skal)
    end = (end + 1) % len(lt)

@prozor.event
def on_draw():
    global end

    try:
        gran(end, lt)
        prozor.clear()
        kriv()
        dalje()

    except IndexError as e:
        print(f"Error: {e}")
        end = 0

def draw2(lt):
    glBegin(GL_LINE_STRIP)
    for tocka in lt:
        skal2 = tocka[0][0] / 5
        skal3 = tocka[0][1] / 5
        skal4 = tocka[0][2] / 5
        glVertex3f(skal2, skal3, skal4)
    glEnd()

def kriv():
    global lt
    draw2(lt)


def draw(dot):
    global ltan, lk

    glPushMatrix()

    glTranslatef(dot[0], dot[1], dot[2])
    glRotatef(lk[end], lo[end][0][0], lo[end][0][1], lo[end][0][2])
    glTranslatef(-dot[0], -dot[1], -dot[2])

    lmv = [m + dot - lv[3] for m in lv]

    for pg in lp:
        glBegin(GL_POLYGON)
        for l in pg:
            m = lmv[l - 1]
            glVertex3f(m[0], m[1], m[2])
        glEnd()
    ltannorm = np.linalg.norm(ltan[end])
    d = ltan[end] / ltannorm + dot

    glBegin(GL_LINE_STRIP)
    glVertex3f(dot[0], dot[1], dot[2])
    glVertex3f(d[0][0], d[0][1], d[0][2])
    glEnd()

    glPopMatrix()

def main():
    global lt, ltan, lo, lk, lv
    ucitaj()
    lv = np.array(lv)
    glColor3f(0, 1, 0)
    lt = []
    ltan = []
    lo = []
    lk = []

    steps = 100
    step_size = 1.0 / steps

    for i in range(len(x) - 3):
        x1, x2, x3, x4 = x[i:i + 4]
        matrica3 = np.array([x1, x2, x3, x4])

        for step in range(steps):
            j = step * step_size
            pom1 = j * j * j
            pom2 = j * j
            pom3 = j
            pom4 = 1
            pom5 = 3 * j * j
            pom6 = 2 * j
            pom7 = 1
            pom8 = 0
            matrica2 = np.array([[pom1, pom2, pom3, pom4]])
            mat_pom = matrica2 * 1 / 6
            med = mat_pom @ matrica1
            res = med @ matrica3
            lt.append(res)
            matrica2 = np.array([[pom5, pom6, pom7, pom8]])
            mat_pom2 = matrica2 @ matrica1
            cilj = mat_pom2 @ matrica3
            ltan.append(cilj)
            os = np.cross(zeljeno, cilj)
            lo.append(os)
            prod = np.multiply(zeljeno, cilj)
            nmzeljeno = np.linalg.norm(zeljeno)
            nmcilj = np.linalg.norm(cilj)
            nmzajednicko = nmzeljeno * nmcilj
            cos = prod / nmzajednicko
            arccos = math.acos(cos[0][2])
            kut = math.degrees(arccos)
            lk.append(kut)

    pyglet.clock.schedule_interval(update, 1 / 60)
    pyglet.app.run()


if __name__ == '__main__':
    main()