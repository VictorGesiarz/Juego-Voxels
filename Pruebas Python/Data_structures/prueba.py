import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from Octree import Voxel, Boundary, Octree, create_octree

def draw_voxel(voxel):
    glBegin(GL_QUADS)
    glColor3fv(voxel.color)
    size = voxel.size
    x, y, z = voxel.x, voxel.y, voxel.z

    glVertex3f(x, y, z)
    glVertex3f(x + size, y, z)
    glVertex3f(x + size, y + size, z)
    glVertex3f(x, y + size, z)

    glVertex3f(x, y, z + size)
    glVertex3f(x + size, y, z + size)
    glVertex3f(x + size, y + size, z + size)
    glVertex3f(x, y + size, z + size)

    glVertex3f(x, y, z)
    glVertex3f(x, y + size, z)
    glVertex3f(x, y + size, z + size)
    glVertex3f(x, y, z + size)

    glVertex3f(x + size, y, z)
    glVertex3f(x + size, y + size, z)
    glVertex3f(x + size, y + size, z + size)
    glVertex3f(x + size, y, z + size)

    glVertex3f(x, y, z)
    glVertex3f(x + size, y, z)
    glVertex3f(x + size, y, z + size)
    glVertex3f(x, y, z + size)

    glVertex3f(x, y + size, z)
    glVertex3f(x + size, y + size, z)
    glVertex3f(x + size, y + size, z + size)
    glVertex3f(x, y + size, z + size)

    glEnd()

def draw_octree(octree):
    if octree.divided:
        for subtree in octree.v:
            draw_octree(subtree)
    elif isinstance(octree.v, Voxel):
        draw_voxel(octree.v)



camera_position = [0.0, 0.0, -5.0]
camera_rotation = [0.0, 0.0, 0.0]
def draw_scene(octree):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluPerspective(90, (800 / 600), 0.1, 50.0)
    glTranslatef(camera_position[0], camera_position[1], camera_position[2])
    glRotatef(camera_rotation[0], 1, 0, 0)
    glRotatef(camera_rotation[1], 0, 1, 0)

    draw_octree(octree)

    pygame.display.flip()

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    octree = create_octree(64, 4)  # Replace this with your Octree instantiation
    print("Octree created")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    camera_position[0] += 0.1
                elif event.key == pygame.K_d:
                    camera_position[0] -= 0.1
                elif event.key == pygame.K_w:
                    camera_position[2] += 0.1
                elif event.key == pygame.K_s:
                    camera_position[2] -= 0.1
                elif event.key == pygame.K_e:
                    camera_position[1] -= 0.1
                elif event.key == pygame.K_q:
                    camera_position[1] += 0.1

            if event.type == pygame.MOUSEMOTION:
                x_rel, y_rel = event.rel
                camera_rotation[1] += x_rel
                camera_rotation[0] += y_rel



        draw_scene(octree)
        pygame.time.wait(10)

if __name__ == "__main__":
    main()