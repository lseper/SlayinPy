import pygame
import sys
from pygame.locals import *
from text_utils import SmartText, SmartSurface
from debug_utils import draw_grid
import numpy as np
import random as rand
import enum

class Collidable:

    # TODO: REALLY need to NOT use class variables here lol
    id = 1

    def __init__(self, rect, name="collidable surface", priority=0):
        self.rect = rect
        # for debugging
        self.name = name
        # I really need to fix this somehow
        self.health = 1
        # done so that some objects can have "priority" in their collision handling
        # EX: handle player colliding with enemies BEFORE enemies colliding with player
        self.priority = priority
        # ensures unique ids
        self.id = Collidable.id
        Collidable.id += 1

    def handle_collision(self, entity):
        # override this to tell each collidable thing how to deal with collisions
        pass
        # print(f"{ self.name } collided with { entity.name }")

class Renderable(Collidable):

    def __init__(self, rect, color, **kwargs):
        self.surface = pygame.Surface((rect.width, rect.height))
        super().__init__(rect, **kwargs)
        self.color = color
        self.surface.fill(self.color)

    def blit(self, blit_surface):
        # draw the player onto the given surface
        blit_surface.blit(self.surface, self.rect)

    def erase(self, blit_surface, erase_surface):
        # erases the drawn player from the screen by drawing something
        # else over it
        blit_surface.blit(erase_surface, self.rect, self.rect)

class Actor(Renderable):

    def __init__(self, size, color, **kwargs):
        self.surface = pygame.Surface(size)
        super().__init__(self.surface.get_rect(), color, **kwargs)
        self.xvel = 0
        self.yvel = 0

    def move(self):
        # move in the x direction
        self.rect.x += self.xvel
        # move in the y direction
        self.rect.y += self.yvel
    
    def action(self):
        pass

    def clip_to_border(self, border):
        if border.side == 'left':
            self.rect.left = border.rect.right
        elif border.side == 'right':
            self.rect.right = border.rect.left
        elif border.side == 'bottom':
            self.rect.bottom = border.rect.top

class HitBoxType(enum.Enum):
    hurt = 0
    heal = 1
    destroy = 2

    