import pygame, sys
from pygame.locals import *

pygame.init()

# Color Constants
BLUE  = pygame.Color(0, 100, 255)
GREY = pygame.Color(100, 100, 100)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400

# Initialize the game surface
SCREEN_SURFACE = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAY_SURFACE = pygame.Surface(SCREEN_SURFACE.get_size())
DISPLAY_SURFACE = DISPLAY_SURFACE.convert()
DISPLAY_SURFACE.fill(BLACK)
# title text

# testSurf = SmartSurface(DISPLAY_SURFACE, size=(0.75, 0.75))
# testSurf.set_color(GREY)
# testSurf.blit()


# testSurf = pygame.Surface((100, 50))
# testSurf.fill(RED)
# DISPLAY_SURFACE.blit(testSurf, (50, 50))

TITLE_FONT = pygame.font.SysFont(None, 150)
TITLE_TEXT = SmartText("Slayin.py", TITLE_FONT, (0.3, 0.5), DISPLAY_SURFACE)
OPTIONS_FONT = pygame.font.SysFont(None, 75)
START_TEXT = SmartText("START", OPTIONS_FONT, (0.6, 0.3), DISPLAY_SURFACE, color=GREEN)
ABOUT_TEXT = SmartText("ABOUT", OPTIONS_FONT, (0.6, 0.7), DISPLAY_SURFACE, color=BLUE)
START_TEXT.set_background(WHITE)
ABOUT_TEXT.set_background(WHITE)
TITLE_TEXT.blit()
START_TEXT.blit()
ABOUT_TEXT.blit()

def hover_menu_option(option):
    option.blit_background = True

def dehover_menu_option(option):
    option.blit_background = False

def increment(i, limit):
    if i < limit:
        return i + 1
    else:
        print(' -- wrapping around --')
        return 0

def decrement(i, wrap):
    if i > 0:
        return i - 1
    else:
        print(' -- wrapping around -- ')
        return wrap

def re_blit(objects):
    for to_blit in objects:
        to_blit.blit()

# debug grid
# draw_grid(DISPLAY_SURFACE, 3, color=RED)

SCREEN_SURFACE.blit(DISPLAY_SURFACE, (0, 0))
# update display to show newly drawn stuff
pygame.display.flip()

OPTIONS = [START_TEXT, ABOUT_TEXT]
i = 0
redraw = False

while True:
    for event in pygame.event.get():            
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_a:
                # deselect old menu option
                dehover_menu_option(OPTIONS[i])
                i = i + 1 if i < len(OPTIONS) - 1 else 0
                # select new menu option
                hover_menu_option(OPTIONS[i])
                redraw = True
            elif event.key == pygame.K_d:
                dehover_menu_option(OPTIONS[i])
                i = i - 1 if i > 0 else len(OPTIONS) - 1
                hover_menu_option(OPTIONS[i])
                redraw = True
    if redraw:
        redraw = False
        # fill with black to completely clear the screen
        DISPLAY_SURFACE.fill(BLACK)
        # re blit everything we want on the screen
        re_blit(OPTIONS)
        TITLE_TEXT.blit()
        # blit the whole ass thing to the screen
        SCREEN_SURFACE.blit(DISPLAY_SURFACE, (0, 0))
        # flip to the next frame
        pygame.display.flip()

print('hello')
