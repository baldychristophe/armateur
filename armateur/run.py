import math

import pygame


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


class StdSurface(pygame.sprite.Sprite):
    def __init__(self, image, rect=None):
        super().__init__()
        self.image = image
        self.rect = rect or self.image.get_rect()


class Display:
    cos_rad_30 = math.cos(math.radians(30))
    sin_rad_30 = math.sin(math.radians(30))

    def __init__(self, raw_map):
        self.screen_size = self.screen_width, self.screen_height = 1600, 900
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption("Armateur")

        self.raw_map = raw_map
        self.radius = 5
        self.map_size = (
            len(raw_map) * self.radius * self.cos_rad_30 * 2,
            # (len(raw_map) / 2) * self.radius * 2 + len(raw_map) / 2 * self.sin_rad_30 * self.radius * 2,
            len(raw_map) * (self.radius + self.sin_rad_30 * self.radius),  # Factorized from line above
        )
        self.map_surface = pygame.Surface(self.map_size)

        self.tiles = []

        self.master_surface = self.screen.subsurface(pygame.Rect(0, 0, self.screen_width, self.screen_height))

        self.scroll_surface = pygame.Surface(self.screen_size)
        self.view_rect = pygame.Rect(0, 0, self.screen_width, self.screen_height)

        self.interface_surface = pygame.Surface((480, 270))
        self.interface_surface.set_alpha(200)
        self.interface_surface.fill(grey)

        font = pygame.font.Font(None, 100)
        surf = font.render('This is a test', True, pygame.Color('red'), grey)

        button_surface = pygame.Surface((50, 20))
        button_surface.fill(pygame.Color('red'))

        self.interface_group = pygame.sprite.LayeredUpdates()

        self.interface_group.add(StdSurface(surf))
        self.interface_group.add(StdSurface(button_surface, pygame.Rect(420, 240, 50, 20)))
        self.interface_group.draw(self.interface_surface)

        self.layers = pygame.sprite.LayeredUpdates()
        self.layers.add(StdSurface(self.scroll_surface), layer=1)
        self.layers.add(StdSurface(self.interface_surface, pygame.Rect(660, 315, 480, 270)), layer=2)

        self.update_hex = None

    def flip(self):
        self.layers.draw(self.master_surface)

        pygame.display.flip()

    def mouse_clic(self, event):
        pos_sprite = pygame.sprite.Sprite()
        pos_sprite.rect = pygame.Rect(event.pos[0], event.pos[1], 1, 1)

        collided_layer = pygame.sprite.spritecollide(pos_sprite, self.layers, False)
        print(collided_layer)

    def scroll(self, dx=0, dy=0):
        if not self.view_rect.x - dx >= 0 or self.view_rect.x - dx + self.view_rect.w > self.map_surface.get_rect().w:
            return

        if not self.view_rect.y - dy >= 0 or self.view_rect.y - dy + self.view_rect.h > self.map_surface.get_rect().h:
            return

        self.scroll_surface.scroll(dx=dx, dy=dy)
        self.view_rect.move_ip(-dx, -dy)

        src_rect = self.view_rect.copy()
        zoom_view_rect = self.scroll_surface.get_clip()
        dst_rect = zoom_view_rect.copy()

        if dy != 0:
            src_rect.h = dst_rect.h = abs(dy)  # scroll_factor

            if dy < 0:
                src_rect.bottom = self.view_rect.bottom
                dst_rect.bottom = zoom_view_rect.bottom
            else:
                src_rect.top = self.view_rect.top
                dst_rect.top = zoom_view_rect.top

        if dx != 0:
            src_rect.w = dst_rect.w = abs(dx)  # scroll_factor

            if dx < 0:
                src_rect.right = self.view_rect.right
                dst_rect.right = zoom_view_rect.right
            else:
                src_rect.left = self.view_rect.left
                dst_rect.left = zoom_view_rect.left

        self.scroll_surface.subsurface(dst_rect).blit(self.map_surface.subsurface(src_rect), (0, 0))

    def mouse_update(self, mouse_pos):
        line = (mouse_pos[1] + self.view_rect.y) // (self.radius + (self.sin_rad_30 * self.radius))
        col = (mouse_pos[0] + self.view_rect.x + ((line % 2) * self.sin_rad_30 * self.radius)) // (
                    2 * self.cos_rad_30 * self.radius)
        highlight_hex = self.tiles[int(255 * line + col)]

        if highlight_hex != self.update_hex:
            highlight_hex.highlight = True
            highlight_hex.display()

            if self.update_hex:
                self.update_hex.highlight = False
                self.update_hex.display()

            self.update_hex = highlight_hex

            self.scroll_surface.blit(self.map_surface.subsurface(self.view_rect), (0, 0))

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
                            (j * 2 * self.cos_rad_30 * self.radius) + (((i + 1) % 2) * self.cos_rad_30 * self.radius),
                            (i * (self.radius + (self.sin_rad_30 * self.radius))) + self.radius,
                        ),
                        self.radius,
                        self.map_surface,
                        color=color,
                    )
                )

        self.map_surface.fill(white)

        for tile in self.tiles:
            tile.display()

        self.scroll_surface.blit(self.map_surface, (0, 0))  # Interface offset

        pygame.display.flip()
        return self.tiles


class Client:
    scroll_factor = 80
    fps_limit = 20

    def __init__(self, raw_map):
        self.running = True

        self.display = Display(raw_map)
        self.tiles = self.display.draw_map_tiles()
        self.clock = pygame.time.Clock()
        self.update_hex = None

    def run(self):
        while self.running:
            self.clock.tick(self.fps_limit)

            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                    self.running = False

                if event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
                    self.display.scroll(dx=0, dy=-self.scroll_factor)

                elif event.type == pygame.KEYUP and event.key == pygame.K_UP:
                    self.display.scroll(dx=0, dy=self.scroll_factor)

                elif event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:
                    self.display.scroll(dx=-self.scroll_factor, dy=0)

                elif event.type == pygame.KEYUP and event.key == pygame.K_LEFT:
                    self.display.scroll(dx=self.scroll_factor, dy=0)

                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.display.mouse_clic(event)

                # elif event.type == pygame.MOUSEBUTTONUP and event.button == 5:
                #     radius -= 1
                #     hexs = draw_map(raw_map, scroll_offset)

            mouse_pos = pygame.mouse.get_pos()
            self.display.mouse_update(mouse_pos)

            # Update the screen once per frame
            self.display.flip()

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
