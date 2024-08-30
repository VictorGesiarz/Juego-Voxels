from shaders import *
import pygame as pg
import numpy as np
from CONSTANTS import *



class Game(OpenGLscreen): 
    def __init__(self, grid_x=25, grid_y=25, pixel_size=20): # This would correspond to (width=500, height=500, grid_size=25)
        
        # We need to make sure that the grid size is compatible with the size of the screen. 
        self.HEIGHT, self.WIDTH = grid_x * pixel_size, grid_y * pixel_size
        self.GRID_SIZE = np.array([grid_x, grid_y], dtype=np.uint8)
        self.PIXEL_SIZE = pixel_size


        super().__init__("./Shaders/game 1/programs/pruebaMIA/vertex_shader.vert", 
                          "./Shaders/game 1/programs/pruebaMIA/selecting_grid.frag",
                          self.HEIGHT, self.WIDTH)

        # Create a player, the map and the two points
        self.player = np.array([0, 0], dtype=np.float32)
        self.mouse = np.array([0, 0], dtype=np.uint16)
        self.map = np.array([0] * self.GRID_SIZE[0] * self.GRID_SIZE[1], dtype=np.float32)

        # Auxiliary variables
        self.__first_click = 0
        self.__lights_on = 0
        self.__view_all = 0
        self.__ray_dist = 10


    def reset(self):
        self.player = np.array([0, 0], dtype=np.float32)
        self.mouse = np.array([0, 0], dtype=np.uint16)
        self.map = np.array([0] * self.GRID_SIZE[0] * self.GRID_SIZE[1], dtype=np.float32)
        self.__first_click = 0
        self.__lights_on = 0
        self.__view_all = 1
        self.__ray_dist = 1


    def load_variables(self):
        super().load_variables()
        self.lighstOn_uniform_location = glGetUniformLocation(self.shader_program, "lights_on")
        self.viewAll_uniform_location = glGetUniformLocation(self.shader_program, "view_all")
        self.player_uniform_location = glGetUniformLocation(self.shader_program, "player")
        self.mouse_uniform_location = glGetUniformLocation(self.shader_program, "mouse")
        self.rayDist_uniform_location = glGetUniformLocation(self.shader_program, "ray_dist")

        self.gridSize_uniform_location = glGetUniformLocation(self.shader_program, "grid_size")
        self.map_uniform_location = glGetUniformLocation(self.shader_program, "map")

    
    def _transmit_lighs(self):
        glUniform1i(self.lighstOn_uniform_location, self.__lights_on)

    def _transmit_view(self):
        glUniform1i(self.viewAll_uniform_location, self.__view_all)

    def _transmit_player(self):
        glUniform2f(self.player_uniform_location, self.player[0], self.player[1])
    
    def _transmit_mouse(self):
        glUniform2f(self.mouse_uniform_location, self.mouse[0], self.mouse[1])

    def _transmit_map(self):
        num_squares = len(self.map)
        glUniform1iv(self.map_uniform_location, num_squares, self.map)

    def _transmit_grid_size(self):
        glUniform2f(self.gridSize_uniform_location, self.GRID_SIZE[0], self.GRID_SIZE[1])

    def _transmit_ray_dist(self):
        glUniform1f(self.rayDist_uniform_location, self.__ray_dist)

    def _transmit_all(self):
        self._transmit_lighs()
        self._transmit_view()
        self._transmit_ray_dist()
        self._transmit_mouse()
        self._transmit_player()
        self._transmit_grid_size()
        self._transmit_map()


    """The MAIN function is up to every game"""
    def main(self):
        self._transmit_resolution()
        self._transmit_all()

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
        self._keyboard_player(self.player)
        self._handle_events()

    def _handle_events(self):
        for event in pg.event.get():
            # Handle QUIT
            if event.type == pg.QUIT:
                self.RUNNING = False
            self._handel_other_events(event)

    def _handel_other_events(self, event):
        self._mark_squares(event)
        self._mouse_player(event, self.mouse)
        self._handle_lights(event)
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
            self._transmit_mouse()
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

        changed = False
        if 0 <= next_x < self.WIDTH: 
            grid_x = int(next_x / self.PIXEL_SIZE)
            if self.map[self.GRID_SIZE[0] * grid_x + int(point[1] / self.PIXEL_SIZE)] != 1:
                point[0] = next_x
                changed = True
        if 0 <= next_y < self.HEIGHT:
            grid_y = int(next_y / self.PIXEL_SIZE)
            if self.map[self.GRID_SIZE[0] * int(point[0] / self.PIXEL_SIZE) + grid_y] != 1:
                point[1] = next_y
                changed = True

        if changed:
            self._transmit_player()

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
            current_state = self.map[self.GRID_SIZE[0] * grid_x + grid_y]
            if not self.__first_click:
                self.__first_click = current_state + 1  

            # Mark or unmark 
            if self.__first_click == 1:
                self.map[self.GRID_SIZE[0] * grid_x + grid_y] = 1
                self._transmit_map()
            elif self.__first_click == 2:
                self.map[self.GRID_SIZE[0] * grid_x + grid_y] = 0
                self._transmit_map()

        if event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:
                self.__first_click = 0


    def _handle_lights(self, event):   
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 3:
                self.__lights_on = abs(self.__lights_on - 1)
                self._transmit_lighs()

            if event.button == 4:
                if self.__ray_dist < 36:
                    self.__ray_dist += 0.25
                    self._transmit_ray_dist()
            elif event.button == 5:
                if self.__ray_dist > 0.5:
                    self.__ray_dist -= 0.25
                    self._transmit_ray_dist()
            
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                self.__view_all = abs(self.__view_all - 1)
                self._transmit_view()



GAME = Game()
GAME.main()