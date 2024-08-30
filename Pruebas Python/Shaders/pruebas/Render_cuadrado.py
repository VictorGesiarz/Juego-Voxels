import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GL import shaders

# Initialize Pygame
pygame.init()
display = (800, 600)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

# Set up OpenGL
glClearColor(0.0, 0.0, 0.0, 1.0)
glViewport(0, 0, display[0], display[1])


def load_shaders(path_vertex, path_fragment):
    with open(path_vertex, "r") as f:
        vertex_shader_source = f.read()
    with open(path_fragment, "r") as f:
        fragment_shader_source = f.read()
  
    vertex_shader = shaders.compileShader(vertex_shader_source, GL_VERTEX_SHADER)
    fragment_shader = shaders.compileShader(fragment_shader_source, GL_FRAGMENT_SHADER)
    return vertex_shader, fragment_shader



vertex_shader, fragment_shader = load_shaders("./RayTracing 3D/vertex_shader.vert", "./RayTracing 3D/fragment_shader.frag")
shader_program = shaders.compileProgram(vertex_shader, fragment_shader)

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Use shader program
    glUseProgram(shader_program)

    # Render a quad covering the entire screen
    glBegin(GL_QUADS)
    glVertex3f(-1, -1, 0)
    glVertex3f(1, -1, 0)
    glVertex3f(1, 1, 0)
    glVertex3f(-1, 1, 0)
    glEnd()

    pygame.display.flip()
