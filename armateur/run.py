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


def draw_map(map, cursor_offset):
    blue = (0, 0, 255)
    green = (0, 255, 0)

    for i, line in enumerate(map):
        if i < cursor_offset[1]:
            pass
        if ((i * pixel_size) - cursor_offset[1]) > screen_width:
            print('break i: %s' % i)
            break
        for j, col in enumerate(line):
            if j < cursor_offset[0]:
                pass
            if ((j * pixel_size) - cursor_offset[0]) > screen_height:
                print('break j: %s' % j)
                break
            if int(col) < 0:
                color = blue
            else:
                color = green
            pygame.draw.rect(screen, color, (int((j * pixel_size) - cursor_offset[1]), int((i * pixel_size) - cursor_offset[0]), pixel_size, pixel_size))

    pygame.display.flip()


def main():
    white = (255, 255, 255)

    DOWN_KEY = 274

    cursor_offset = (0, 0)

    pygame.init()
    pygame.display.set_caption("Armateur")

    map = read_map()
    draw_map(map, cursor_offset)

    running = True
    fps_limit = 60
    clock = pygame.time.Clock()
    while running:
        clock.tick(fps_limit)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYUP and event.key == DOWN_KEY:
                print('key up event')
                cursor_offset = (cursor_offset[0] + 50, cursor_offset[1])
                draw_map(map, cursor_offset)


if __name__ == '__main__':
    main()
