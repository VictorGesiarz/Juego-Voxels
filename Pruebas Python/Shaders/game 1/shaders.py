
"""

This is a global class to create the 2D games that I am doing for now, since all of them need the same basic requirements. 
The class initializes the size of the grid, the size of the screen, other variables like the map and others of pygame. 
It has programmed some basic functionalities like resetting the map, functions for drawing the grid, functions for handling inputs (I use the sames many times
so they are programmed here), etc. Also lets you mark the squares as walls. 

"""


import time
import pygame
from pygame.locals import (
    DOUBLEBUF, OPENGL,
)
from OpenGL.GL import (
    glClearColor, glViewport, glLinkProgram, glUseProgram,
    glGetUniformLocation, glUniform1f, glUniform2f, glUniform1i, glUniform2i, glUniform2iv, glUniform1iv, glUniform2fv, glUniformMatrix2fv,
    glBegin, glClear, glVertex3f, glEnd,
    GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, GL_QUADS, GL_TRUE, GL_FALSE,
    GL_VERTEX_SHADER, GL_FRAGMENT_SHADER,
    shaders,
)



class OpenGLscreen: 
    def __init__(self, vertex_shader, fragment_shader, window_height=600, window_width=800):
    
        self.HEIGHT, self.WIDTH = window_height, window_width

        # PyGame variables
        self.display = (self.WIDTH, self.HEIGHT)
        pygame.init()
        pygame.display.set_mode(self.display, DOUBLEBUF | OPENGL)
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()

        # OpenGL variables
        self.shader_program = None
        self.time_uniform_location = None
        self.load_shaders(vertex_shader, fragment_shader)
        self.setup_opengl()
        self.load_variables()

        # Auxiliary variables
        self.RUNNING = True


    def reset(self):
        ...


    """OPENGL Functions: load shaders and setup variables"""
    def load_shaders(self, path_vertex, path_fragment):
        with open(path_vertex, "r") as f:
            vertex_shader_source = f.read()
        with open(path_fragment, "r") as f:
            fragment_shader_source = f.read()

        vertex_shader = shaders.compileShader(vertex_shader_source, GL_VERTEX_SHADER)
        fragment_shader = shaders.compileShader(fragment_shader_source, GL_FRAGMENT_SHADER)
        self.shader_program = shaders.compileProgram(vertex_shader, fragment_shader)

    
    def load_variables(self):
        self.time_uniform_location = glGetUniformLocation(self.shader_program, "iTime")
        self.display_uniform_location = glGetUniformLocation(self.shader_program, "iResolution")


    def _transmit_time(self, elapsed_time):
        glUniform1f(self.time_uniform_location, elapsed_time)

    def _transmit_resolution(self):
        glUniform2f(self.display_uniform_location, self.display[0], self.display[1])


    def setup_opengl(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glViewport(0, 0, self.display[0], self.display[1])
        glLinkProgram(self.shader_program)
        glUseProgram(self.shader_program)


    """The MAIN function is up to every game"""
    def main(self):
        self._transmit_resolution()

        start_time = time.time()

        while self.RUNNING:
            current_time = time.time()
            elapsed_time = current_time - start_time
            
            self._transmit_time(elapsed_time)
            self._handle_inputs()
            self._draw_screen()

            self.clock.tick()

        pygame.quit()
        quit()
        

    """HANDLING EVENTS: it is done in some separate functions to manage inputs in different ways if needed."""
    def _handle_inputs(self):
        self._handle_events()

    def _handle_events(self):
        for event in pygame.event.get():
            # Handle QUIT
            if event.type == pygame.QUIT:
                self.RUNNING = False
            self._handel_other_events(event)

    def _handel_other_events(self, event):
        ...


    """DRAWING THE SCREEN: we draw the screen using the programmed shaders and OpenGL functions"""
    def _draw_screen(self):
        fps = int(self.clock.get_fps())
        pygame.display.set_caption(f"Pygame FPS Example - FPS: {fps}")

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Render a quad covering the entire screen
        glBegin(GL_QUADS)
        glVertex3f(-1, -1, 0)
        glVertex3f(1, -1, 0)
        glVertex3f(1, 1, 0)
        glVertex3f(-1, 1, 0)
        glEnd()

        pygame.display.flip()
