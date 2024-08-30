
"""

This is a global class to create the 2D games that I am doing for now, since all of them need the same basic requirements. 
The class initializes the size of the grid, the size of the screen, other variables like the map and others of pygame. 
It has programmed some basic functionalities like resetting the map, functions for drawing the grid, functions for handling inputs (I use the sames many times
so they are programmed here), etc. Also lets you mark the squares as walls. 

"""



import pygame as pg
import numpy as np
from CONSTANTS import *



class Game: 
    def __init__(self, grid_x=25, grid_y=25, pixel_size=20): # This would correspond to (width=500, height=500, grid_size=25)
        
        # We need to make sure that the grid size is compatible with the size of the screen. 
        self.HEIGHT, self.WIDTH = grid_x * pixel_size, grid_y * pixel_size
        self.GRID_SIZE = np.array([grid_x, grid_y], dtype=np.uint8)
        self.PIXEL_SIZE = pixel_size

        # Create the map and the two points
        self.map = np.array([[0] * self.GRID_SIZE[0] for _ in range(self.GRID_SIZE[1])], dtype=np.uint8)
        self.marked_squares = set()

        # PyGame variables
        self.display = (self.WIDTH, self.HEIGHT)
        self.screen = None
        self.clock = pg.time.Clock()

        # Auxiliary variables
        self.__first_click = 0
        self.RUNNING = True


    def reset(self):
        self.map = np.array([[0] * self.GRID_SIZE[0] for _ in range(self.GRID_SIZE[1])], dtype=np.uint8)
        self.marked_squares = set()
        self.__first_click = 0


    """The MAIN function is up to every game"""
    def main(self):
        pg.init()
        pg.display.set_mode(self.display)
        self.screen = pg.display.get_surface()
        ...


    """DRAWING THE SCREEN: predefined template"""
    def _draw_scene(self, background_color=WHITE, color1=BLUE, color2=WHITE, color3=GRAY):
        fps = int(self.clock.get_fps())
        pg.display.set_caption(f"Pygame FPS Example - FPS: {fps}")
        self.screen.fill(background_color)
        self._draw_pixels(color1=color1, color2=color2)
        self._draw_grid(color=color3)
        
        # MAKE SURE TO ADD
        # pg.display.flip()

    def _draw_pixels(self, color1=BLUE, draw_map=None):
        # Draw the squares
        if draw_map is None:
            draw_map = self.marked_squares
        
        for pixel in draw_map:
            x = pixel[0] * self.PIXEL_SIZE
            y = pixel[1] * self.PIXEL_SIZE
            pg.draw.rect(self.screen, color1, (x, y, self.PIXEL_SIZE, self.PIXEL_SIZE))
        
    def _draw_grid(self, color=GRAY):
        # Draw lines to visualize the grid
        for x in range(0, self.WIDTH, self.PIXEL_SIZE):
            pg.draw.line(self.screen, color, (x, 0), (x, self.HEIGHT))
        for y in range(0, self.HEIGHT, self.PIXEL_SIZE):
            pg.draw.line(self.screen, color, (0, y), (self.WIDTH, y))


    """HANDLING EVENTS: it is done in some separate functions to manage inputs in different ways if needed."""
    def _handle_inputs(self):
        self._handle_events()

    def _handle_events(self):
        for event in pg.event.get():
            # Handle QUIT
            if event.type == pg.QUIT:
                self.RUNNING = False
            self._handel_other_events(event)

    def _handel_other_events(self, event):
        self._mark_squares(event)
        self._handle_reset(event)
    

    def _handle_reset(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_BACKSPACE:
                self.reset()


    # Predefined function to move a player with a mouse
    def _mouse_player(self, event, point):
        if event.type == pg.MOUSEMOTION:
            mouse_pos = pg.mouse.get_pos()
            point[0] = max(0, min(mouse_pos[0], self.WIDTH - 1))
            point[1] = max(0, min(mouse_pos[1], self.HEIGHT - 1))
        return point

    # Predefined function to move a player with the keyboard
    def _keyboard_player(self, point, speed_1=0.5, speed_2=0.1):
        keys = pg.key.get_pressed()
        speed = speed_1
        if keys[pg.K_LSHIFT]:
            speed = speed_2
        
        next_x, next_y = point[0], point[1]
        if keys[pg.K_a]:
            next_x -= speed
        if keys[pg.K_d]:
            next_x += speed
        if keys[pg.K_w]:
            next_y -= speed
        if keys[pg.K_s]:
            next_y += speed

        if 0 <= next_x < self.WIDTH: 
            grid_x = int(next_x / self.PIXEL_SIZE)
            if self.map[int(point[1] / self.PIXEL_SIZE), grid_x] != 1:
                point[0] = next_x
        if 0 <= next_y < self.HEIGHT:
            grid_y = int(next_y / self.PIXEL_SIZE)
            if self.map[grid_y, int(point[0] / self.PIXEL_SIZE)] != 1:
                point[1] = next_y
        return point

    # Predefined function to mark the squares with the left click. 
    def _mark_squares(self, event):
        mouse_pressed = pg.mouse.get_pressed()
        # Handle Selection of squares
        if event.type == pg.MOUSEMOTION and mouse_pressed[0] or mouse_pressed[0]:  # Left mouse button held down
            # Get position
            pos = pg.mouse.get_pos()
            x, y = max(0, min(pos[0], self.WIDTH - 1)), max(0, min(pos[1], self.WIDTH - 1))
            grid_x = x // self.PIXEL_SIZE
            grid_y = y // self.PIXEL_SIZE

            # This is only for better functionality of the selection
            current_state = self.map[grid_y][grid_x]
            if not self.__first_click:
                self.__first_click = current_state + 1  

            # Mark or unmark 
            if self.__first_click == 1:
                self.map[grid_y, grid_x] = 1
                self.marked_squares.add((grid_x, grid_y))
            elif self.__first_click == 2:
                self.map[grid_y, grid_x] = 0
                self.marked_squares.add((grid_x, grid_y))
                self.marked_squares.remove((grid_x, grid_y))

        if event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:
                self.__first_click = 0
