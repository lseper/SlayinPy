import pygame



class SmartSurface():
    '''
    A class to aid in subsurfaces on parent surfaces better, 
    since a native parent->child system for surfaces is non-existent
    @author Liam Seper
    '''

    def __init__(self, parent, position=(0.5, 0.5), size=(1, 1)):
        self.parent = parent # parent surface you will be blitting the text onto
        self.surface = pygame.Surface(self.__calculate_size(size))
        self.position = position
        self.rect = self.surface.get_rect() # ( width, height )

    def set_color(self, color):
        self.surface.fill(color)

    def __calculate_size(self, rel_size):
        p_width = self.parent.get_rect().width
        p_height = self.parent.get_rect().height
        return p_width * rel_size[0], p_height * rel_size[1]

    def __align(self):
        # position is a tuple of floats between 0 and 1. It describes where, in relation to the
        # parent surface, to put the center of the new surface
        # EX: text centered in the middle = __align((0.5, 0.5))

        # align the text according to the parent
        p_rect = self.parent.get_rect()
        x = (p_rect.width * self.position[1]) - (self.rect.width // 2)
        y = (p_rect.height * self.position[0]) - (self.rect.height // 2)
        return x, y

    def blit(self, position=(0.5, 0.5)):
        # wrapper for pygame.surface.blit()
        self.parent.blit(self.surface, self.__align())

class SmartText():
    '''
    A class to aid in aligning text on parent surfaces better, 
    since a native parent->child system for surfaces is non-existent
    @author Liam Seper
    '''

    def __init__(self, text, font, position, parent, color=(255, 255, 255)):
        self.text = text # string of the text being used
        self.font = font # needs to be a pygame.Font() object, not a string
        self.parent = parent # parent surface you will be blitting the text onto
        self.color = color # color of the text
        self.__recalculate_size(self.text)
        self.__render_text()
        self.blit_background = False
        self.position = position

    def set_text(self, new_text):
        # recalculate how much the space the new text will take up
        self.__recalculate_size(new_text)
        # set the text to display as the new text
        self.text = new_text

    def set_background(self, color):
        self.background = SmartSurface(self.surface)
        self.background.set_color(color)
    
    def __recalculate_size(self, new):
        # recalculate the size rectangle (width, height) that the new text will take up
        self.rect = self.font.size(new)

    def __render_text(self):
        # render this text to a surface so it can be blitted
        self.surface = self.font.render(self.text, True, self.color)

    def __align(self):
        # position is a tuple of floats between 0 and 1. It describes where, in relation to the
        # parent surface, to put the center of the new surface
        # EX: text centered in the middle = __align((0.5, 0.5))

        # align the text according to the parent
        p_rect = self.parent.get_rect()
        x = (p_rect.width * self.position[1]) - (self.rect[0] // 2)
        y = (p_rect.height * self.position[0]) - (self.rect[1] // 2)
        return x, y

    def blit(self, position=(0.5, 0.5)):
        # wrapper for pygame.surface.blit()
        if self.blit_background:
            self.parent.blit(self.background.surface, self.__align())
        self.parent.blit(self.surface, self.__align())