import random

import pygame


screen_size = screen_width, screen_height = 1080, 1080
screen = pygame.display.set_mode(screen_size)

pixel_size = 10


class Octagon(pygame.sprite.Sprite):
    pass



def read_map():
    f = open('France_250_ASC_L93.OCEAN0.S.fdf')
    map = []
    for line in f:
        cols = line.split(' ')
        map.append(cols)

    return map


def draw_map(map, cursor_offset):
    blue = (0, 0, 255)
    green = (0, 255, 0)
    white = (255, 255, 255)

    screen.lock()
    screen.fill(white)
    for i in range(cursor_offset[0], int((screen_height / pixel_size) + cursor_offset[0])):
        for j in range(cursor_offset[1], int((screen_width / pixel_size) + cursor_offset[1])):
            if int(map[i][j]) < 0:
                color = blue
            else:
                color = green
            inside = pygame.draw.rect(screen, color, (int((j - cursor_offset[1]) * pixel_size), int((i - cursor_offset[0]) * pixel_size), pixel_size, pixel_size))
            outside = pygame.draw.rect(screen, (0, 0, 0), inside, 1)

    screen.unlock()
    pygame.display.flip()
    print('end draw')


def main():
    cursor_offset = (0, 0)

    pygame.init()
    pygame.display.set_caption("Armateur")

    map = read_map()
    draw_map(map, cursor_offset)

    running = True
    fps_limit = 20
    clock = pygame.time.Clock()
    while running:
        clock.tick(fps_limit)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                running = False

            if event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
                cursor_offset = (cursor_offset[0] + 1, cursor_offset[1])
                draw_map(map, cursor_offset)

            if event.type == pygame.KEYUP and event.key == pygame.K_UP:
                cursor_offset = (cursor_offset[0] - 1, cursor_offset[1])
                draw_map(map, cursor_offset)

            if event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:
                cursor_offset = (cursor_offset[0], cursor_offset[1] + 1)
                draw_map(map, cursor_offset)

            if event.type == pygame.KEYUP and event.key == pygame.K_LEFT:
                cursor_offset = (cursor_offset[0], cursor_offset[1] - 1)
                draw_map(map, cursor_offset)


if __name__ == '__main__':
    main()
