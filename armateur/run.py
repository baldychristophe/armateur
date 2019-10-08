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


def read_map():
    f = open('France_250_ASC_L93.OCEAN0.S.fdf')
    raw_map = []
    for line in f:
        cols = line.split(' ')
        raw_map.append(cols)

    return raw_map


class Hexagon(pygame.sprite.Sprite):
    def __init__(self, center, radius, surface, color):
        super().__init__()
        self.center = center
        self.radius = radius
        self.surface = surface
        self.color = color
        self.rect = None
        self.highlight = False
        self.drawing_vector = pygame.math.Vector2(0, self.radius)

    def display(self):
        points = []
        color = self.color
        if self.highlight:
            color = pygame.Color('red')

        for i in range(6):
            point = (self.center + self.drawing_vector.rotate(i * 60))
            points.append(tuple(map(int, point)))

        self.rect = pygame.draw.polygon(self.surface, color, points, 1)


class Display:
    cos_rad_30 = math.cos(math.radians(30))
    sin_rad_30 = math.sin(math.radians(30))

    def __init__(self, raw_map):
        self.screen_size = self.screen_width, self.screen_height = 800, 800
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption("Armateur")

        self.raw_map = raw_map
        self.radius = 5
        self.map_size = (
            255 * 10,
            255 * 10,
        )
        self.map_surface = pygame.Surface(self.map_size)
        self.interface_surface = pygame.Surface((200, screen_height))
        self.tiles = []

        self.view_rect = pygame.Rect(0, 0, self.screen_width, self.screen_height)
        self.scroll_surface = screen.subsurface(pygame.Rect(200, 0, self.screen_width - 200, self.screen_height))
        # self.scroll_surface = screen.subsurface(pygame.Rect(0, 0, self.screen_width, self.screen_height))

    def scroll(self, dx=0, dy=0):
        self.scroll_surface.scroll(dx=dx, dy=dy)
        self.view_rect.move_ip(-dx, -dy)

        src_rect = self.view_rect.copy()
        zoom_view_rect = self.scroll_surface.get_clip()
        dst_rect = zoom_view_rect.copy()

        if dy != 0:
            # dst_rect.w = 600  # Interface : 600
            src_rect.h = 20  # scroll_factor
            dst_rect.h = 20  # scroll_factor

            if dy < 0:
                src_rect.bottom = self.view_rect.bottom
                dst_rect.bottomright = zoom_view_rect.bottomright
            else:
                src_rect.top = self.view_rect.top
                dst_rect.topright = zoom_view_rect.topright

        if dx != 0:
            # dst_rect.h = 800
            src_rect.w = 20  # scroll_factor
            dst_rect.w = 20  # scroll_factor

            if dx < 0:
                src_rect.right = self.view_rect.right
                dst_rect.bottomright = zoom_view_rect.bottomright
            else:
                src_rect.left = self.view_rect.left
                dst_rect.topleft = zoom_view_rect.topleft

        self.scroll_surface.subsurface(dst_rect).blit(self.map_surface.subsurface(src_rect), (0, 0))

        pygame.display.flip()

    def draw_map_tiles(self):
        for i in range(len(self.raw_map)):
            for j in range(len(self.raw_map)):
                if int(self.raw_map[i][j]) < 0:
                    color = blue
                else:
                    color = green
                self.tiles.append(
                    Hexagon(
                        (
                            (j * 2 * self.cos_rad_30 * radius) + (((i + 1) % 2) * self.cos_rad_30 * self.radius),
                            (i * (self.radius + (self.sin_rad_30 * self.radius))) + self.radius,
                        ),
                        self.radius,
                        self.map_surface,
                        color=color,
                    )
                )

        self.map_surface.fill(white)
        self.interface_surface.fill(grey)

        for tile in self.tiles:
            tile.display()

        self.scroll_surface.blit(self.map_surface, (0, 0))  # Interface offset
        # self.screen.blit(self.interface_surface, (0, 0))

        pygame.display.flip()
        return self.tiles


class Client:
    scroll_factor = 20
    fps_limit = 20

    def __init__(self, raw_map):
        self.running = True

        self.scroll_offset = (0, 0)
        self.display = Display(raw_map)
        self.tiles = self.display.draw_map_tiles()
        self.clock = pygame.time.Clock()
        self.update_hex = None

    def run(self):
        view_rect = pygame.Rect(0, 0, screen_width, screen_height)
        scroll_surface = screen.subsurface(pygame.Rect(200, 0, screen_width - 200, screen_height))

        while self.running:
            self.clock.tick(self.fps_limit)
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                    self.running = False

                if event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
                    self.scroll_offset = (self.scroll_offset[0], self.scroll_offset[1] - self.scroll_factor)
                    self.display.scroll(dx=0, dy=-self.scroll_factor)

                elif event.type == pygame.KEYUP and event.key == pygame.K_UP:
                    self.scroll_offset = (self.scroll_offset[0], self.scroll_offset[1] + self.scroll_factor)
                    self.display.scroll(dx=0, dy=self.scroll_factor)

                elif event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:
                    self.scroll_offset = (self.scroll_offset[0] - self.scroll_factor, self.scroll_offset[1])
                    self.display.scroll(dx=-self.scroll_factor, dy=0)

                elif event.type == pygame.KEYUP and event.key == pygame.K_LEFT:
                    self.scroll_offset = (self.scroll_offset[0] + self.scroll_factor, self.scroll_offset[1])
                    self.display.scroll(dx=self.scroll_factor, dy=0)

                # elif event.type == pygame.MOUSEBUTTONUP and event.button == 5:
                #     radius -= 1
                #     hexs = draw_map(raw_map, scroll_offset)

            mouse_pos = pygame.mouse.get_pos()
            line = (mouse_pos[1] - self.scroll_offset[1]) // (radius + (math.sin(math.radians(30)) * radius))
            col = (mouse_pos[0] - self.scroll_offset[0] + ((line % 2) * math.sin(math.radians(30)) * radius)) // (
                        2 * math.cos(math.radians(30)) * radius)
            highlight_hex = self.tiles[int(255 * line + col)]

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


def main():
    pygame.init()
    pygame.mixer.quit()  # TODO fix high cpu usage (recompile pygame in local or use pygame 2+)

    raw_map = read_map()
    client = Client(raw_map)
    client.run()


if __name__ == '__main__':
    main()
