
"""

First implementation of the ray tracing in a 2D pixel world, but there is only 1 ray, from the player to the mouse. 
The ray detects where it collides. 

"""



from game import *
from ray_trace import *
import time


class OneRay(Game):
    def __init__(self, grid_x=25, grid_y=25, pixel_size=20):
        super().__init__(grid_x, grid_y, pixel_size)

        # Variables needed for this example. Green is where the mouse is and red where the Player is. 
        self.green_point = np.array([0, 0], dtype=np.uint16)
        self.red_point = np.array([0, 0], dtype=np.float32)

        # Auxiliary variables for this example.
        self.__print_line = 0
        self.__vIntersection = None


    def reset(self):
        super().reset()
        self.green_point = np.array([0, 0], dtype=np.uint16)
        self.red_point = np.array([0, 0], dtype=np.uint16)


    def main(self):
        super().main()
        pg.mouse.set_visible(False)

        while self.RUNNING:
            self._handle_inputs()
            if self.__print_line:
                self.__vIntersection = ray_trace_start_end(self.red_point, self.green_point, self.map, self.GRID_SIZE, self.PIXEL_SIZE)

            self._draw_scene()
            self.clock.tick()
        pg.quit()


    def _draw_scene(self):
        super()._draw_scene()

        # Draw points and a line connecting them
        if self.__print_line: pg.draw.aaline(self.screen, DARK_GRAY, self.red_point, self.green_point)
        pg.draw.circle(self.screen, GREEN, self.green_point, 5)
        pg.draw.circle(self.screen, RED, self.red_point.astype(np.uint16), 5)

        if self.__vIntersection is not None:
            pg.draw.circle(self.screen, BLACK, self.__vIntersection, 3, width=1)

        pg.display.flip()


    def _handle_inputs(self):
        self.red_point = self._keyboard_player(self.red_point)
        self._handle_events()

    def _handel_other_events(self, event):
        self.green_point = self._mouse_player(event, self.green_point)
        self._mark_squares(event)
        self._other_events(event)
        self._handle_reset(event)

    def _other_events(self, event):   
        # Handle line drawing
        if event.type == pg.MOUSEBUTTONUP:
            if event.button == 3:  # Right mouse button released
                self.__print_line = 0
                self.__vIntersection = None
        mouse_pressed = pg.mouse.get_pressed()
        if mouse_pressed[2]:
            self.__print_line = 1


game = OneRay()
game.main()
