
"""

This is a better implementation of the lantern in 2D, where instead of casting rays in 
all directions from the player, it only casts to the edges of the objects, making a lot less
rays and calculations, resulting in faster ray casting. Also, with this algorithm we can make
the lights more realistic, without the black lines that appeared in the other implementation. 

This implementation is inspired from the video https://www.youtube.com/watch?v=fc3nnG2CG8U&pp=ygUUcmF5Y2FzdGluZyBhbGdvcml0aG0%3D.

"""



from game import *
from ray_trace import *
import numpy as np
import time
import math


class Lantern(Game):
    def __init__(self, grid_x=25, grid_y=25, pixel_size=20):
        super().__init__(grid_x, grid_y, pixel_size)

        # Variables needed for this example. Green is where the mouse is and red where the Player is. 
        self.player = np.array([0, 0], dtype=np.float32)
        self.mouse = np.array([0, 0], dtype=np.uint16)
        self.rays, self._draw_grid_lights_off = [], []
        self.edges, self.vertices = [], []

        """LOAD A PREDEFINED MAP"""
        # self.player, self.map, self.marked_squares = get_labirinth_1()

        # Auxiliary variables for this example.
        self.__lights_on = 0
        self.__view_all = 1
        self.__show_edges = 0


    def reset(self):
        super().reset()
        self.player = np.array([0, 0], dtype=np.float32)
        self.mouse = np.array([0, 0], dtype=np.uint16)
        self.rays, self._draw_grid_lights_off = [], []
        self.edges = []
        self.__lights_on = 0
        self.__view_all = 1


    def main(self):
        super().main()

        while self.RUNNING:
            self._handle_inputs()
            
            if self.__lights_on:
                """ILUMINATE IN ONE DIRECTION"""
                # self.rays, self._draw_grid_lights_off = ray_trace_field_of_view(self.player, self.mouse, 2, 20, 360, self.map, self.GRID_SIZE, self.PIXEL_SIZE) 
                """ILLUMINATE ALL AROUND THE PLAYER"""
                self.rays, self._draw_grid_lights_off = ray_trace_all_directions(self.player, 100, 360, self.map, self.GRID_SIZE, self.PIXEL_SIZE)

            self._draw_scene()
            self.clock.tick()
        pg.quit()


    def _draw_scene(self):
        # super()._draw_scene(background_color=BLACK, color1=BLUE, color2=BLACK, color3=DARK_GRAY)
        fps = int(self.clock.get_fps())
        pg.display.set_caption(f"Pygame FPS Example - FPS: {fps}")
        self.screen.fill(BLACK)
        self._draw_pixels(color1=BLUE, color2=BLACK)
        
        # DRAW THE CORRESPONDING TRIANGLES
        
        # DRAW THE CORRESPONDING EDGES AND VERTICES

        pg.draw.circle(self.screen, RED, self.player.astype(np.uint16), 5)
        
        pg.display.flip()


    def _handle_inputs(self):
        self.player = self._keyboard_player(self.player)
        self._handle_events()

    def _handel_other_events(self, event):
        self._mark_squares(event)
        self._mouse_player(event, self.mouse)
        self._handle_lights(event)
        self._handle_reset(event)

    def _handle_lights(self, event):   
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 3:
                self.__lights_on = abs(self.__lights_on - 1)
                self.rays = []
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                self.__view_all = abs(self.__view_all - 1)
            if event.key == pg.K_KP_ENTER:
                self.__show_edges = abs(self.__show_edges - 1)



game = Lantern()

game.main()
