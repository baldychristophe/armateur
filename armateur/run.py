import math

import pygame


screen_size = screen_width, screen_height = 800, 800
screen = pygame.display.set_mode(screen_size)

radius = 5
map_size = (
    255 * 5,
    255 * 5,
)
map_surface = pygame.Surface(map_size)
interface_surface = pygame.Surface((200, screen_height))

blue = (0, 0, 255)
green = (0, 255, 0)
white = (255, 255, 255)
grey = (98, 95, 107)


class Hexagon(pygame.sprite.Sprite):
    def __init__(self, center, radius, color=green):
        super().__init__()
        self.center = center
        self.radius = radius
        self.color = color
        self.rect = None
        self.highlight = False
        self.drawing_vector = pygame.math.Vector2(0, self.radius)

    def display(self, color=None):
        points = []
        color = color or self.color
        if self.highlight:
            color = pygame.Color('red')

        for i in range(6):
            point = (self.center + self.drawing_vector.rotate(i * 60))
            points.append(tuple(map(int, point)))

        self.rect = pygame.draw.polygon(map_surface, color, points, 1)


def read_map():
    f = open('France_250_ASC_L93.OCEAN0.S.fdf')
    raw_map = []
    for line in f:
        cols = line.split(' ')
        raw_map.append(cols)


    return raw_map


def draw_map(game_map, scroll_offset):

    cos_radius = math.cos(math.radians(30))
    sin_radius = math.sin(math.radians(30))

    hexs = []
    for i in range(len(game_map)):
        for j in range(len(game_map)):
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

    map_surface.fill(white)
    interface_surface.fill(grey)

    for hex in hexs:
        hex.display()

    screen.blit(map_surface, (0, 0))

    pygame.draw.rect(interface_surface, white, (55, 50, 50, 5))
    pygame.draw.rect(interface_surface, white, (50, 55, 5, 50))

    temp = pygame.Surface((10, 10), pygame.SRCALPHA)
    temp.fill((0, 0, 0, 0))
    pygame.draw.ellipse(temp, white, (0, 0, 20, 20))
    temp = pygame.transform.smoothscale(temp, (5, 5))  # Anti-aliasing
    interface_surface.blit(temp, (50, 50))

    pygame.draw.rect(interface_surface, white, (55, 150, 50, 5))
    pygame.draw.rect(interface_surface, white, (50, 155, 5, 50))

    temp = pygame.Surface((50, 50), pygame.SRCALPHA)
    temp.fill((0, 0, 0, 0))
    pygame.draw.ellipse(temp, white, (0, 0, 100, 100))
    temp = pygame.transform.smoothscale(temp, (5, 5))  # Anti-aliasing
    interface_surface.blit(temp, (50, 150))


    screen.blit(interface_surface, (0, 0))

    pygame.display.flip()
    return hexs

def main():
    global radius
    scroll_offset = (0, 0)
    scroll_factor = 20

    pygame.init()
    pygame.mixer.quit()  # TODO fix high cpu usage (recompile pygame in local or use pygame 2+)
    pygame.display.set_caption("Armateur")

    raw_map = read_map()
    hexs = draw_map(raw_map, scroll_offset)

    running = True
    fps_limit = 20
    clock = pygame.time.Clock()
    update_hex = None

    view_rect = pygame.Rect(0, 0, screen_width, screen_height)
    scroll_surface = screen.subsurface(pygame.Rect(200, 0, screen_width - 200, screen_height))

    while running:
        clock.tick(fps_limit)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                running = False

            if event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
                scroll_offset = (scroll_offset[0], scroll_offset[1] - scroll_factor)

                scroll_surface.scroll(dy=-scroll_factor)

                view_rect.move_ip(0, scroll_factor)

                src_rect = view_rect.copy()
                src_rect.h = scroll_factor
                src_rect.bottom = view_rect.bottom

                zoom_view_rect = screen.get_clip()
                dst_rect = zoom_view_rect.copy()
                dst_rect.h = scroll_factor
                dst_rect.w = 600
                dst_rect.bottomright = zoom_view_rect.bottomright

                screen.subsurface(dst_rect).blit(map_surface.subsurface(src_rect), (0, 0))

                pygame.display.update(zoom_view_rect)

            elif event.type == pygame.KEYUP and event.key == pygame.K_UP:
                scroll_offset = (scroll_offset[0], scroll_offset[1] + scroll_factor)
                screen.scroll(dy=scroll_factor)
                screen.blit(map_surface, scroll_offset)
                pygame.display.flip()

            elif event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:
                scroll_offset = (scroll_offset[0] - scroll_factor, scroll_offset[1])
                screen.scroll(dx=-scroll_factor)
                screen.blit(map_surface, scroll_offset)
                pygame.display.flip()

            elif event.type == pygame.KEYUP and event.key == pygame.K_LEFT:
                scroll_offset = (scroll_offset[0] + scroll_factor, scroll_offset[1])
                screen.scroll(dx=scroll_factor)
                screen.blit(map_surface, scroll_offset)
                pygame.display.flip()

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 5:
                radius -= 1
                hexs = draw_map(raw_map, scroll_offset)

        mouse_pos = pygame.mouse.get_pos()
        line = (mouse_pos[1] - scroll_offset[1]) // (radius + (math.sin(math.radians(30)) * radius))
        col = (mouse_pos[0] - scroll_offset[0] + ((line % 2) * math.sin(math.radians(30)) * radius)) // (2 * math.cos(math.radians(30)) * radius)
        highlight_hex = hexs[int(255 * line + col)]

        # if highlight_hex != update_hex:
        #     highlight_hex.highlight = True
        #     highlight_hex.display()
        #
        #     if update_hex:
        #         update_hex.highlight = False
        #         update_hex.display()
        #
        #     update_hex = highlight_hex
        #
        #     screen.blit(map_surface, scroll_offset)
        #     pygame.display.flip()

        # scroll_margin = 70
        # if mouse_pos[0] < scroll_margin:
        #     pygame.event.post(pygame.event.Event(pygame.KEYUP, {'key': pygame.K_LEFT}))
        # elif mouse_pos[0] > (screen_width - scroll_margin):
        #     pygame.event.post(pygame.event.Event(pygame.KEYUP, {'key': pygame.K_RIGHT}))
        #
        # if mouse_pos[1] < scroll_margin:
        #     pygame.event.post(pygame.event.Event(pygame.KEYUP, {'key': pygame.K_UP}))
        # elif mouse_pos[1] > (screen_height - scroll_margin):
        #     pygame.event.post(pygame.event.Event(pygame.KEYUP, {'key': pygame.K_DOWN}))


if __name__ == '__main__':
    main()
