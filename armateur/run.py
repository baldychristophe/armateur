import random

import pygame


screen_size = screen_width, screen_height = 600, 450
screen = pygame.display.set_mode(screen_size)


class Pixel:
    def __init__(self, color, position):
        self.color = color
        self.position = position

    def display(self):
        pygame.draw.rect(screen, self.color, ((*self.position), 50, 50))

def main():
    white = (255, 255, 255)
    blue = (0, 0, 255)
    green = (0, 255, 0)

    pygame.init()

    pygame.display.set_caption("Armateur")
    screen.fill(white)
    pixels = []
    for i in range(int(screen_width / 50)):
        for j in range(int(screen_height / 50)):
            color = blue if (i + j) % 2 == 0 else green
            pixels.append(Pixel(color, (i * 50, j * 50)))

    for pixel in pixels:
        pixel.display()

    pygame.display.flip()

    running = True
    while running:
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False


if __name__ == '__main__':
    main()
