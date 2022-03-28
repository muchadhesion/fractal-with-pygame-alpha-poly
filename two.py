
import operator
import pygame
import math
import random

# pygame window params
WINDOW_WIDTH=640
WINDOW_HEIGHT=800

game_time_ms = 0
import numpy as np

def draw_polygon_alpha(surface, color, points):
    lx, ly = zip(*points)
    min_x, min_y, max_x, max_y = min(lx), min(ly), max(lx), max(ly)
    target_rect = pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    pygame.draw.polygon(shape_surf, color, [(x - min_x, y - min_y) for x, y in points])
    surface.blit(shape_surf, target_rect)

def rotate(p, origin=(0, 0), degrees=0):
    angle = np.deg2rad(degrees)
    R = np.array([[np.cos(angle), -np.sin(angle)],
                  [np.sin(angle),  np.cos(angle)]])
    o = np.atleast_2d(origin)
    p = np.atleast_2d(p)
    return np.squeeze((R @ (p.T-o.T) + o.T).T)

def grow(screen, centre, size, rotation, depth):
    if depth > 30:
        return
    if size < 10:
        return
    waft = 40 * math.sin( game_time_ms / 1000 )
    rotation += waft
    c = pygame.Color(250,200,60,10)
    left = centre[0] - size/2
    top = centre[1] - size/2
    points=[(left, top), (left+size, top), (left+size, top+size), (left, top+size)]
    new_points = rotate(points, centre, degrees=rotation)
    draw_polygon_alpha(screen, c, new_points)
    # pygame.draw.polygon( screen, c, new_points)
    # pygame.draw.rect(screen, c , pygame.Rect(left, top, size, size))
    grow(screen, new_points[0], size*0.8, rotation+20, depth+1  )
    grow(screen, new_points[2], size*0.8, rotation-180+20, depth+1  )

def update(screen):
    center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
    grow( screen, center, 100, 0, 1)

#
# Create a pygame window and "game frame" boilerplate
#
def main():
    pygame.init()

    screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
    running = True
    clock = pygame.time.Clock()

    global game_time_ms
    while running:
        ms = clock.tick(60)
        game_time_ms += ms
        screen.fill((0,0,20))

        # draw the thing
        update(screen)

        pygame.display.flip()
        # check exit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


if __name__=="__main__":
    # call the main function
    main()
