import math

import pygame


blue = (0, 0, 255)
green = (0, 255, 0)
white = (255, 255, 255)
grey = (98, 95, 107)

cos_rad_30 = math.cos(math.radians(30))
sin_rad_30 = math.sin(math.radians(30))


def read_map():
    # f = open('France_250_ASC_L93.OCEAN0.S.fdf')
    f = open('test_map.txt')
    raw_map = []
    for line in f:
        raw_map.append(line.split(' '))

    return raw_map


class Hexagon(pygame.sprite.Sprite):
    def __init__(self, pos, radius, color):
        super().__init__()
        self.radius = radius
        self.size = self.width, self.height = (round(self.radius * cos_rad_30 * 2) + 1, round(self.radius * 2) + 1)
        self.rect = pygame.Rect(pos[0], pos[1], self.width, self.height)
        self.color = color
        self.highlight = False
        self.image = pygame.Surface(self.size)
        self.draw()

    def draw(self):
        self.image.set_colorkey((50, 50, 50))
        self.image.fill((50, 50, 50))

        color = self.color
        if self.highlight:
            color = pygame.Color('red')

        w = self.image.get_width()
        h = self.image.get_height()
        points = [
            (w // 2, h - 1),
            (0, h - (self.radius * sin_rad_30)),
            (0, (self.radius * sin_rad_30)),
            (w // 2, 0),
            (w - 1, (self.radius * sin_rad_30)),
            (w - 1, h - (self.radius * sin_rad_30)),
        ]
        pygame.draw.polygon(self.image, pygame.Color('white'), points)  # inside
        pygame.draw.polygon(self.image, color, points, 1)  # outside

    def update(self, surface):
        self.draw()
        surface.blit(self.image, self.rect)


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
        self.map_size = self.map_width, self.map_height = (
            len(raw_map) * self.radius * self.cos_rad_30 * 2,
            # (len(raw_map) / 2) * self.radius * 2 + len(raw_map) / 2 * self.sin_rad_30 * self.radius * 2,
            len(raw_map) * (self.radius + self.sin_rad_30 * self.radius),  # Factorized from line above
        )
        self.tiles = pygame.sprite.OrderedUpdates()
        self.sprites = None

        self.master_surface = self.screen.subsurface(pygame.Rect(0, 0, self.screen_width, self.screen_height))

        self.view_rect = pygame.Rect(0, 0, self.screen_width, self.screen_height)

        self.scroll_surface = StdSurface(pygame.Surface(self.map_size), rect=self.view_rect)

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
        self.layers.add(self.scroll_surface, layer=1)
        self.layers.add(StdSurface(self.interface_surface, pygame.Rect(660, 315, 480, 270)), layer=2)

        self.update_hex = None
        self.draw_map_tiles()

    def flip(self):
        self.layers.draw(self.master_surface)

        pygame.display.flip()

    def mouse_clic(self, event):
        pos_sprite = pygame.sprite.Sprite()
        pos_sprite.rect = pygame.Rect(event.pos[0], event.pos[1], 1, 1)

        collided_layer = pygame.sprite.spritecollide(pos_sprite, self.layers, False)
        print(collided_layer)

    def scroll(self, dx=0, dy=0):
        if not self.view_rect.x + dx <= 0 or self.view_rect.w - (self.view_rect.x + dx) > self.map_width:
            return

        if not self.view_rect.y + dy <= 0 or self.view_rect.h - (self.view_rect.y + dy) > self.map_height:
            return

        # self.scroll_surface.image.scroll(dx=dx, dy=dy)
        self.scroll_surface.rect.move_ip(dx, dy)

    def mouse_update(self, mouse_pos):
        line = (mouse_pos[1] - self.view_rect.y) // (self.radius + (self.sin_rad_30 * self.radius))
        col = (mouse_pos[0] - self.view_rect.x + ((line % 2) * self.sin_rad_30 * self.radius)) // (
                    2 * self.cos_rad_30 * self.radius)
        highlight_hex = self.sprites[int(255 * line + col)]

        if highlight_hex and highlight_hex != self.update_hex:
            highlight_hex.highlight = True
            highlight_hex.update(self.scroll_surface.image)

            if self.update_hex:
                self.update_hex.highlight = False
                self.update_hex.update(self.scroll_surface.image)

            self.update_hex = highlight_hex

    def draw_map_tiles(self):
        for i in range(len(self.raw_map)):
            for j in range(len(self.raw_map)):
                if int(self.raw_map[i][j]) < 0:
                    color = blue
                else:
                    color = green
                self.tiles.add(
                    Hexagon(
                        (
                            (j * 2 * self.cos_rad_30 * self.radius) + (((i + 1) % 2) * self.cos_rad_30 * self.radius),
                            (i * (self.radius + (self.sin_rad_30 * self.radius))) + self.radius,
                        ),
                        self.radius,
                        color=color,
                    )
                )
        self.tiles.draw(self.scroll_surface.image)
        self.sprites = self.tiles.sprites()


class Client:
    scroll_factor = 20
    fps_limit = 20

    def __init__(self, raw_map):
        self.running = True

        self.display = Display(raw_map)
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

                elif event.type == pygame.MOUSEBUTTONUP and event.button == 5:
                    pass  # dezoom

            mouse_pos = pygame.mouse.get_pos()
            self.display.mouse_update(mouse_pos)

            # Update the screen once per frame
            self.display.flip()

            scroll_margin = 20
            if mouse_pos[0] < scroll_margin:
                pygame.event.post(pygame.event.Event(pygame.KEYUP, {'key': pygame.K_LEFT}))
            elif mouse_pos[0] > (self.display.screen_width - scroll_margin):
                pygame.event.post(pygame.event.Event(pygame.KEYUP, {'key': pygame.K_RIGHT}))

            if mouse_pos[1] < scroll_margin:
                pygame.event.post(pygame.event.Event(pygame.KEYUP, {'key': pygame.K_UP}))
            elif mouse_pos[1] > (self.display.screen_height - scroll_margin):
                pygame.event.post(pygame.event.Event(pygame.KEYUP, {'key': pygame.K_DOWN}))


def main():
    pygame.init()
    pygame.mixer.quit()  # TODO fix high cpu usage (recompile pygame in local or use pygame 2+)

    raw_map = read_map()
    client = Client(raw_map)
    client.run()


if __name__ == '__main__':
    main()
