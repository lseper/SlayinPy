import numpy as np
import pygame

def draw_grid(screen, n, color=(255, 255, 255)):
    screen_rect = screen.get_rect()
    xGap, yGap = (screen_rect.width / n), (screen_rect.height / n)
    xRange = np.arange(xGap, screen.get_rect().width, xGap)
    yRange = np.arange(yGap, screen.get_rect().height, yGap)
    # text setup
    x_offset = int(xGap * 0.05)
    y_offset = int(yGap * 0.05)
    label_font = pygame.font.SysFont(None, x_offset * 2)
    for x in xRange:
        # draw from (100, 0) --> (100, 300) vertical lines
        pygame.draw.line(screen, color, (x, 0), (x, screen_rect.height))
        # render the text label for this line slightly to the right of the vertical line
        screen.blit(label_font.render(str(int(x)), True, color), (x + x_offset, 0))
    for y in yRange:
        # draw from (0, 200) --> (600, 200) horizontal lines
        pygame.draw.line(screen, color, (0, y), (screen_rect.width, y))
        # render the text label for this line slightly below the horizontal line
        screen.blit(label_font.render(str(int(y)), True, color), (0, y + y_offset))