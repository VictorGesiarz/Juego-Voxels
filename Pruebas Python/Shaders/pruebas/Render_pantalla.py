
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

# Define vertex shader (dummy vertex shader, as we're not using vertex transformations)
vertex_shader = shaders.compileShader("""
    void main() {
        gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
    }
""", GL_VERTEX_SHADER)

# Define fragment shader
fragment_shader = shaders.compileShader("""
    void main() {
        // Set color to red
        gl_FragColor = vec4(1.0, 0.0, 0.0, 1.0);
    }
""", GL_FRAGMENT_SHADER)

# Compile shaders
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

    # Set viewport to cover entire window
    glViewport(0, 0, display[0], display[1])

    # Render something (e.g., a single point to cover the viewport)
    glBegin(GL_POINTS)
    glVertex3f(0, 0, 0)
    glEnd()

    pygame.display.flip()
