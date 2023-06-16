import pygame
from random import randint


class Background(pygame.sprite.Sprite):
    def __init__(self, type):
        """ Create the object sattelite or spaceship """
        super().__init__()
        if type == 'sattelite':
             self.name = 'sattelite'
             sattelite = pygame.image.load('images/spaceships/sattelite.png').convert_alpha()
             self.x_pos = randint(1000,1300)
             self.y_pos = randint(40,150)
             self.frames = [sattelite]
        else:
            spaceship = pygame.image.load('images/spaceships/spaceship.png').convert_alpha()
            self.name = 'spaceship'
            self.x_pos = randint(-200, -100)
            self.y_pos = randint(70,200)
            self.frames = [spaceship]

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(center = (self.x_pos, self.y_pos))

    def animation_state(self):
        """ Animate the objects """
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
             self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        """ Update all objects """
        self.animation_state()
        if self.name == 'spaceship':
             self.rect.x += 4
        else:
             self.rect.x -= 1
        self.destroy()

    def destroy(self):
        """ Destroy objects out of the screen """
        if self.rect.x <= -200 or self.rect.x >= 1300:
               self.kill()


