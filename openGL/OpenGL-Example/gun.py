import pygame as pg
from OpenGL.raw.GLUT import glutSolidTorus, glutSolidCube
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

cubeVertices = ((1,1,1),(1,1,-1),(1,-1,-1),(1, -1, 1),(-1,1,1),(-1,-1,-1),(-1,-1,1),(-1, 1, -1))
cubeEdges = ((0,1),(0,3),(0,4),(1,2),(1,7),(2,5),(2,3),(3,6),(4,6),(4,7),(5,6),(5,7))
cubeQuads = ((0,3,6,4),(2,5,6,3),(1,2,5,7),(1,0,4,7),(7,4,6,5),(2,3,0,1))


def draw_gun():
    ambient_coeffsGray = [0.3, 0.3, 0.3, 1]
    diffuse_coeffsGray = [0.5, 0.5, 0.5, 1]
    specular_coeffsGray = [0, 0, 0, 1]
    glMaterialfv(GL_FRONT, GL_AMBIENT, ambient_coeffsGray)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, diffuse_coeffsGray)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specular_coeffsGray)
    glMateriali(GL_FRONT, GL_SHININESS, 1)

    glPushMatrix()
    #glTranslatef(4, 1, 3)

    glPushMatrix()
    glTranslatef(3.1, 0, 1.75)
    glRotatef(90, 0, 1, 0)
    glScalef(1, 1, 5)
    glScalef(0.2, 0.2, 0.2)
    glutSolidTorus(0.2, 1, 10, 10)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(2.5, 0, 1.75)
    glScalef(0.1, 0.1, 1)
    glutSolidCube(1)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(1, 0, 1)
    glRotatef(10, 0, 1, 0)
    glScalef(0.1, 0.1, 1)
    glutSolidCube(1)

    glPopMatrix()

    glPushMatrix()
    glTranslatef(0.8, 0, 0.8)
    glRotatef(90, 1, 0, 0)
    glScalef(0.5, 0.5, 0.5)
    glutSolidTorus(0.2, 1, 10, 10)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(1, 0, 1.5)
    glRotatef(90, 0, 1, 0)
    glScalef(1, 1, 4)
    glutSolidCube(1)
    glPopMatrix()

    glPushMatrix()
    glRotatef(8, 0, 1, 0)
    glScalef(1.1, 0.8, 3)
    glutSolidCube(1)
    glPopMatrix()

    glPopMatrix()
def wireCube():
    glBegin(GL_LINES)
    for cubeEdge in cubeEdges:
        for cubeVertex in cubeEdge:
            glVertex3fv(cubeVertices[cubeVertex])
    glEnd()
def solidCube():
    glBegin(GL_QUADS)
    for cubeQuad in cubeQuads:
        for cubeVertex in cubeQuad:
            glVertex3fv(cubeVertices[cubeVertex])
    glEnd()

def main():
    pg.init()
    display = (1680,1050)
    pg.display.set_mode(display, DOUBLEBUF|OPENGL)
    glClearColor(0.1,0.1,0.3,0.3)
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    gluLookAt(5,5,5,0,0,0,0,0,1)

    glTranslatef(0.0,0.0, -5)
    br=0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()


        glRotatef(1, 1, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        draw_gun()
        pg.display.flip()
        pg.time.wait(10)


if __name__ == "__main__":
    main()