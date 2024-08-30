from quadtree import Quadtree, Pixel, Rectangle
import pygame
import sys


pygame.init()

size = 800
width, height = size, size
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Quadtrees")
font = pygame.font.Font(None, 36)


rect = Rectangle(0, 0, size)
Q = Quadtree(rect)
PIXEL_SIZE = 25


def draw(screen, boundaries, pixels, found, boundary_finding, text):
    screen.fill((255, 255, 255))
    
    for y in range(0, height, PIXEL_SIZE):
        pygame.draw.line(screen, (200, 200, 200), (0, y), (width, y))

    for x in range(0, width, PIXEL_SIZE):
        pygame.draw.line(screen, (200, 200, 200), (x, 0), (x, height))
    
    for pixel in pixels:
        pygame.draw.rect(screen, (0, 0, 255), (pixel.x, pixel.y, pixel.s, pixel.s)) 
    
    for pixel in found:
        pygame.draw.rect(screen, (0, 255, 0), (pixel.x, pixel.y, pixel.s, pixel.s))

    for boundary in boundaries:    
        pygame.draw.rect(screen, (0, 0, 0), (boundary.x, boundary.y, boundary.s, boundary.s), 1) 

    for boundary in boundary_finding:    
        pygame.draw.rect(screen, (0, 255, 0), (boundary.x, boundary.y, boundary.s, boundary.s), 2) 

    screen.blit(text, (10, 10)) 


mode = "insert"
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if mode == "insert": mode = "find"
                elif mode == "find": mode = "insert"
            elif event.key == pygame.K_ESCAPE:
                rect = Rectangle(0, 0, size)
                Q = Quadtree(rect)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if mode == "insert":
                x, y = pygame.mouse.get_pos()
                pixel = Pixel(x - x % PIXEL_SIZE, y - y % PIXEL_SIZE, PIXEL_SIZE)
                Q.insert(pixel)

    found = []
    boundary = []
    text = font.render("", True, (0, 0, 0))
    if mode == "find":
        x, y = pygame.mouse.get_pos()   
        BOUNDARY_SIZE = 200
        rect_x = x - BOUNDARY_SIZE // 2
        rect_y = y - BOUNDARY_SIZE // 2
        boundary = [Rectangle(rect_x, rect_y, BOUNDARY_SIZE)]
        found, count = Q.find_pixels_in_square(boundary[0])
        text = font.render(str(count), True, (0, 0, 0)) 
        
    boundaries, pixels = Q.get_boundaries() 
    draw(screen, boundaries, pixels, found, boundary, text)
    pygame.display.flip()
    pygame.time.Clock().tick(60)
