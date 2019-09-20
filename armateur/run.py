import math

import pygame


screen_size = screen_width, screen_height = 1080, 1080
screen = pygame.display.set_mode(screen_size)

main_surface = pygame.Surface(screen_size)

map_surface = pygame.Surface(screen_size)

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
        self.rect = None
        self.drawing_vector = pygame.math.Vector2(0, self.radius)

    def display(self):
        points = []
        for i in range(6):
            point = (self.center + self.drawing_vector.rotate(i * 60))
            points.append(tuple(map(int, point)))

        self.rect = pygame.draw.polygon(map_surface, self.color, points, 1)



def read_map():
    f = open('France_250_ASC_L93.OCEAN0.S.fdf')
    map = []
    for line in f:
        cols = line.split(' ')
        map.append(cols)

    return map


def draw_map(game_map, scroll_offset):
    radius = 5

    cos_radius = math.cos(math.radians(30))
    sin_radius = math.sin(math.radians(30))

    hexs = []
    # for i in range(int(screen_width / (radius * math.sin(math.radians(30)) * 2))):
    for i in range(255):
        for j in range(255):
        # for j in range(int(screen_height / (radius * 2 * math.cos(math.radians(30))))):
            if int(game_map[i - scroll_offset[0]][j - scroll_offset[1]]) < 0:
                color = blue
            else:
                color = green
            hexs.append(
                Hexagon(
                    (
                        (j * 2 * cos_radius * radius) + (((i + 1) % 2) * cos_radius * radius),
                        (i * (radius + (sin_radius * radius))) + radius,
                    ),
                    radius,
                    color=color,
                )
            )

    main_surface.fill(white)
    # temp = main_surface.subsurface(map_surface.get_rect())

    for hex in hexs:
        hex.display()

    main_surface.blit(map_surface, (0, 0))
    pygame.display.flip()

    screen.blit(main_surface, (0, 0))

    # main_surface.subsurface(map_surface.get_rect())
    # screen.subsurface(main_surface.get_rect())

    pygame.display.flip()
    # import ipdb; ipdb.set_trace()


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
                screen.scroll(dy=-10)
                pygame.display.update(main_surface.get_clip())

            if event.type == pygame.KEYUP and event.key == pygame.K_UP:
                scroll_offset = (scroll_offset[0] + 1, scroll_offset[1])
                main_surface.scroll(dy=+10)
                pygame.display.flip()

            if event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:
                scroll_offset = (scroll_offset[0], scroll_offset[1] - 1)
                main_surface.scroll(dx=-10)
                pygame.display.flip()

            if event.type == pygame.KEYUP and event.key == pygame.K_LEFT:
                scroll_offset = (scroll_offset[0], scroll_offset[1] + 1)
                main_surface.scroll(dx=+10)
                pygame.display.flip()

if __name__ == '__main__':
    main()
