import pygame
import sys
from pygame.draw import rect
from pygame.locals import *
from text_utils import SmartText, SmartSurface
from debug_utils import draw_grid
import numpy as np
import random as rand

from observer_system import Observer, Observable
from game_systems import *
from game_base import *

pygame.init()
pygame.display.set_caption("Slayin.py")
        
# Color Constants
BLUE  = pygame.Color(0, 100, 255)
GREY = pygame.Color(100, 100, 100)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400

class Border(Renderable):

    def __init__(self, rect, color, side, **kwargs):
        super().__init__(rect, color, **kwargs)
        self.side = side

# change to only collidable in the future, but for now like this for debugging purposes
class Hitbox(Renderable):

    def __init__(self, rect, hitbox_type, **kwargs):
        super().__init__(rect, color=BLACK, name="hitbox")
        # hitbox is on
        self.active = True
        self.hitbox_type = hitbox_type
    
    def handle_collision(self, entity):
        print(self.hitbox_type)
        if self.hitbox_type == HitBoxType.destroy:
            self.destroy(entity)
        if self.hitbox_type == HitBoxType.hurt:
            return self.hurt(entity)
        else:
            return self.heal(entity)
        pass

    def destroy(self, entity):
        print(f"damaging {entity.id}")
        entity.health -= 1
        
    def hurt(self, entity):
        pass

    def heal(self, entity):
        pass

    def clip_to_border(self, border):
        pass


# class HitboxAction:

#     def __init__(self, game_manager)

# "Actor" could probably be extracted. This seems more as a Player class.
# additionally, a base "Actor" class could be used by the Enemy too
class Player(Actor):

    def __init__(self, size, color, **kwargs):
        super().__init__(size, color, **kwargs)
        self.gravity = 0
        self.actions = 1
        self.health = 10
        self.sword = Hitbox(Rect(self.rect.right, self.rect.centery, 20, 8), HitBoxType.destroy)
        # self.sword.rect.left = self.rect.right
        # self.sword.rect.centery = self.rect.centery

    def turn_right(self):
        if self.xvel < 0:
            self.xvel *= -1
            # hacky fix for this glitch
            # self.sword.rect.left = self.rect.right
    
    def turn_left(self):
        if self.xvel > 0:
            self.xvel *= -1
            # hacky fix for this glitch
            # self.sword.rect.right = self.rect.left

    def move(self):
        super().move()
        self.yvel += self.gravity
        # fix this to a different class that is composed of multiple hitboxes
        if self.xvel < 0:
            self.sword.rect.right = self.rect.left
        else:
            self.sword.rect.left = self.rect.right
        self.sword.rect.centery = self.rect.centery
    
    def action(self):
        if self.actions > 0:
            # should be genericized, but this works for now
            self.yvel = -15
            self.gravity = 2
            self.actions -= 1

    def clip_to_border(self, border):
        super().clip_to_border(border)
        # code repetition here of the if-statement, could be a better way to do this?
        if border.side == 'bottom':
            self.reset_actions()

    def reset_actions(self):
        self.actions = 1
        self.__ground()

    def __ground(self):
        self.yvel = 0
        self.gravity = 0

# Consider refactoring Actor and Enemy -- they share a lot of similarities
class Enemy(Renderable):

    # hard-coded thing for moving frames
    ACTION_LENGTH_MINIMUM = 5
    ACTION_LENGTH_MAXIMUM = 40

    MOVE_SPEED = 3
    
    def __init__(self, size, color, **kwargs):
        self.surface = pygame.Surface(size)
        self.health = 1
        super().__init__(self.surface.get_rect(), color, **kwargs)
        # a.i sequence -- currently just moves randomly
        self.moving_frames = Enemy.ACTION_LENGTH_MINIMUM
        self.vel = Enemy.MOVE_SPEED

    def __initiate_action(self):
        # initiate the settings for this movement (duration, speed)
        self.moving_frames = self.__random_duration()
        self.vel = Enemy.MOVE_SPEED * self.__random_direction()

    def action(self):
        # if we've exhausted the last movement duration, generate a new one
        if self.moving_frames <= 0:
            self.__initiate_action()
        # do the movement
        self.rect.x += self.vel
        self.moving_frames -= 1

    # done to prevent enemy from going off screen
    def clip_to_border(self, border):
        if border.side == 'left':
            self.rect.left = border.rect.right
        elif border.side == 'right':
            self.rect.right = border.rect.left
        elif border.side == 'bottom':
            self.rect.bottom = border.rect.top

    def handle_collision(self, enemy):
        # destroy the enemy
        # could maybe use observer pattern for this?
        # on collision, broadcast the tag of the enemy killed
        # AI System, Collission System, and Render System all subscribe to the player
        # when broadcasted, lookup entity with that tag and remove it
        pass

    def __random_direction(self):
        return rand.randint(-1, 1)
    
    def __random_duration(self):
        return rand.randint(Enemy.ACTION_LENGTH_MINIMUM, Enemy.ACTION_LENGTH_MAXIMUM)


# Initialize the clock used, and set the framerate cap to 30 FPS
clock = pygame.time.Clock()

# Initialize the screen
SCREEN_SURFACE = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# Initialize the background surface. This will also be used to erase our player
BACKGROUND = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
BACKGROUND = BACKGROUND.convert()
BACKGROUND.fill(WHITE)

left_border = Border(pygame.Rect((0, 0), (50, SCREEN_HEIGHT)), BLUE, "left") # Border that the player will watch for
right_border = Border(pygame.Rect((SCREEN_WIDTH - 50, 0), (50, SCREEN_HEIGHT)), BLUE, "right") # Border that the player will watch for
bottom_border = Border(pygame.Rect((0, SCREEN_HEIGHT - 100), (SCREEN_WIDTH, 100)), GREY, "bottom") # Border that the player will watch for

# have player start in the bottom middle of the screen
player = Player((25, 50), RED, name='player')
# set to bottom initially, with speed of 2 (this should be moved to an instantiator somewhere)
player.rect.midbottom = (SCREEN_WIDTH // 2, SCREEN_HEIGHT-100)
player.xvel = 5

# enemies
enemies = []
for i in range(10):
    enemy = Enemy((30, 25), GREEN, name=f'enemy{i}')
    # set test enemy to bottom initially, with no speed
    enemy.rect.midbottom = (SCREEN_WIDTH // 2, SCREEN_HEIGHT-40)
    enemies.append(enemy)

# create the enemy system
ai_system = AISystem(enemies)
collision_system = CollisionSystem([player, player.sword, *enemies], [left_border, right_border, bottom_border])
render_system = RenderSystem(SCREEN_SURFACE, BACKGROUND, [player, player.sword, bottom_border, left_border, right_border, *enemies])

# blit the whole background to the screen
SCREEN_SURFACE.blit(BACKGROUND, (0, 0))

while True:
    for event in pygame.event.get():            
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                player.turn_left()
            elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                player.turn_right()
            elif event.key == pygame.K_SPACE:
                player.action()
    
    # keep the FPS at 30
    clock.tick(60)
    # erase the player from the screen
    # player.erase(SCREEN_SURFACE, BACKGROUND)
    render_system.handle_erases()
    # move the player to the new position (this should be put into a system soon)
    player.move()
    # move the enemy to the new position (this should be put into a system soon)
    ai_system.perform_actions()
    # handle collisions that have occurred
    collision_system.handle_collisions()
    # render everything
    render_system.handle_renders()
    # update the screen
    pygame.display.update()