import random

import pygame


screen_size = screen_width, screen_height = 1441, 1441
screen = pygame.display.set_mode(screen_size)

pixel_size = 2


def read_map():
    f = open('France_250_ASC_L93.OCEAN0.XL.fdf')
    map = []
    for line in f:
        cols = line.split(' ')
        map.append(cols)

    return map


def main():
    white = (255, 255, 255)
    blue = (0, 0, 255)
    green = (0, 255, 0)
    DOWN_KEY = 274

    pygame.init()
    pygame.display.set_caption("Armateur")

    map = read_map()

    for i, line in enumerate(map):
        for j, col in enumerate(line):
            if int(col) < 0:
                color = blue
            else:
                color = green
            pygame.draw.rect(screen, color, (j * pixel_size, i * pixel_size, pixel_size, pixel_size))

    pygame.display.flip()

    running = True
    fps_limit = 60
    clock = pygame.time.Clock()
    while running:
        clock.tick(fps_limit)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYUP and event.key == DOWN_KEY:
                pass


if __name__ == '__main__':
    main()
