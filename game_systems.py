import pygame
import sys
from pygame.locals import *
from text_utils import SmartText, SmartSurface
from debug_utils import draw_grid
import numpy as np
import random as rand

# Idea: Add a queue for handling collisions so that two entities don't register a collision twice (X colliding w/ Y and Y colliding w/ X)
# collisions would be sorted by priority (i.e Player's sword hitbox = first to be evaluated, next enemy hitboxes, then remaining hurtboxes)
class CollisionSystem:

    def __init__(self, collidables, borders):
        self.collidables = collidables
        self.borders = borders

    def remove_collidable(self, collidable):
        for i in range(len(self.collidables)):
            c = self.collidables[i]
            if collidable.id == c.id:
                self.collidables.pop(i)

    def add_collidable(self, collidable):
        self.collidables.append(collidable)

    def add_border(self, border):
        self.borders.append(border)
        
    def handle_collisions(self):
        self.handle_border_collisions()
        for i in range(len(self.collidables)):
            for j in range(len(self.collidables)):
                # skip things colliding with themselves
                if i == j:
                    continue
                entity_one = self.collidables[i]
                entity_two = self.collidables[j]
                if self.is_colliding(entity_one, entity_two):
                    entity_one.handle_collision(entity_two) # uniform collision handling between things
        collidables_copy = []
        for x in range(len(self.collidables)):
            if self.collidables[x].health > 0:
                collidables_copy.append(self.collidables[x])
        self.collidables = collidables_copy
    
    def handle_border_collisions(self):
        for collidable in self.collidables:
            for border in self.borders:
                if self.is_colliding(collidable, border):
                    collidable.clip_to_border(border)
    
    def is_colliding(self, entity_one, entity_two):
        # top is between the top and bottom of another thing
        if entity_one.rect.colliderect(entity_two.rect):
            return True
        return False


class RenderSystem:

    def __init__(self, screen, erase_surface, renderables):
        self.erase_surface = erase_surface
        self.screen = screen
        self.renderables = renderables
        self.to_erase = []
    
    def remove_renderable(self, renderable):
        for i in range(len(self.renderables)):
            c = self.renderables[i]
            if renderable.id == c.id:
                self.renderables.pop(i)

    def add_renderable(self, renderable):
        self.renderables.append(renderable)

    def handle_renders(self):
        for renderable in self.renderables:
            renderable.blit(self.screen)
    
    def handle_erases(self):
        for renderable in self.renderables:
            renderable.erase(self.screen, self.erase_surface)
        renderables_copy = []
        for x in range(len(self.renderables)):
            if self.renderables[x].health > 0:
                renderables_copy.append(self.renderables[x])
        self.renderables = renderables_copy

class AISystem:

    def __init__(self, ai):
        self.ai = ai

    def remove_ai(self, ai):
        for i in range(len(self.ai)):
            c = self.ai[i]
            if ai.id == c.id:
                self.ai.pop(i)

    def add_ai(self, ai):
        # maybe handle ai spawning here?
        self.ai.apppend(ai)

    def perform_actions(self):
        for ai in self.ai:
            ai.action()
        ai_copy = []
        for x in range(len(self.ai)):
            if self.ai[x].health > 0:
                ai_copy.append(self.ai[x])
        self.ai = ai_copy