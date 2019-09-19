import math

import pygame


screen_size = screen_width, screen_height = 1080, 1080
screen = pygame.display.set_mode(screen_size)

pixel_size = 20

blue = (0, 0, 255)
green = (0, 255, 0)
white = (255, 255, 255)


class Hexagon(pygame.sprite.Sprite):
    def __init__(self, center, radius, color=green):
        super().__init__()
        self.center = center
        self.radius = radius
        self.color = color
        self.drawing_vector = pygame.math.Vector2(0, self.radius)

    def display(self):
        points = []
        for i in range(6):
            point = (self.center + self.drawing_vector.rotate(i * 60))
            points.append(tuple(map(int, point)))

        pygame.draw.polygon(screen, self.color, points, 1)



def read_map():
    f = open('France_250_ASC_L93.OCEAN0.S.fdf')
    map = []
    for line in f:
        cols = line.split(' ')
        map.append(cols)

    return map


def draw_map(game_map, scroll_offset):
    screen.lock()
    screen.fill(white)
    # for i in range(scroll_offset[0], int((screen_height / pixel_size) + scroll_offset[0])):
    #     for j in range(scroll_offset[1], int((screen_width / pixel_size) + scroll_offset[1])):
    #         if int(map[i][j]) < 0:
    #             color = blue
    #         else:
    #             color = green
    #         inside = pygame.draw.rect(screen, color, (int((j - scroll_offset[1]) * pixel_size), int((i - scroll_offset[0]) * pixel_size), pixel_size, pixel_size))
    #         outside = pygame.draw.rect(screen, (0, 0, 0), inside, 1)

    radius = 36

    hexs = []
    for i in range(int(screen_width / (radius * math.sin(math.radians(30)) * 2))):
        for j in range(int(screen_height / (radius * 2 * math.cos(math.radians(30))))):
            hexs.append(
                Hexagon(
                    (
                        (j * 2 * math.cos(math.radians(30)) * radius) + (((i + 1) % 2) * math.cos(math.radians(30)) * radius),
                        (i * (radius + (math.sin(math.radians(30)) * radius))) + radius,
                    ),
                    radius,
                )
            )

    for hex in hexs:
        hex.display()

    screen.unlock()
    pygame.display.flip()


def main():
    scroll_offset = (0, 0)

    pygame.init()
    pygame.display.set_caption("Armateur")

    map = read_map()
    draw_map(map, scroll_offset)

    running = True
    fps_limit = 20
    clock = pygame.time.Clock()
    while running:
        clock.tick(fps_limit)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                running = False

            if event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
                scroll_offset = (scroll_offset[0] - 1, scroll_offset[1])
                draw_map(map, scroll_offset)

            if event.type == pygame.KEYUP and event.key == pygame.K_UP:
                scroll_offset = (scroll_offset[0] + 1, scroll_offset[1])
                draw_map(map, scroll_offset)

            if event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:
                scroll_offset = (scroll_offset[0], scroll_offset[1] - 1)
                draw_map(map, scroll_offset)

            if event.type == pygame.KEYUP and event.key == pygame.K_LEFT:
                scroll_offset = (scroll_offset[0], scroll_offset[1] + 1)
                draw_map(map, scroll_offset)


if __name__ == '__main__':
    main()
