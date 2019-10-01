
def draw_rounded_rect(surface, color, rect):
    """Test function to draw rounded rectangles"""
    import pygame
    white = (255, 255, 255)

    pygame.draw.rect(surface, white, (55, 50, 50, 5))
    pygame.draw.rect(surface, white, (50, 55, 5, 50))

    temp = pygame.Surface((10, 10), pygame.SRCALPHA)
    temp.fill((0, 0, 0, 0))
    pygame.draw.ellipse(temp, white, (0, 0, 20, 20))
    temp = pygame.transform.smoothscale(temp, (5, 5))  # Anti-aliasing
    surface.blit(temp, (50, 50))

    pygame.draw.rect(surface, white, (60, 150, 50, 1))
    pygame.draw.rect(surface, white, (50, 160, 1, 50))

    temp = pygame.Surface((50, 50), pygame.SRCALPHA)
    temp.fill((0, 0, 0, 0))
    pygame.draw.ellipse(temp, white, (0, 0, 100, 100), 15)
    temp = pygame.transform.smoothscale(temp, (10, 10))  # Anti-aliasing
    surface.blit(temp, (50, 150))
