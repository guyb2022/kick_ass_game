import pygame
from random import randint

class Obstacle(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()
        if type == 'little_enemy':
             little_enemy_1 = pygame.image.load('images/enemy/enemy_right_small_1.png').convert_alpha()
             little_enemy_2 = pygame.image.load('images/enemy/enemy_right_small_2.png').convert_alpha()
             self.frames = [little_enemy_1, little_enemy_2]
             y_pos = 450
        else:
             big_enemy_1 = pygame.image.load('images/enemy/enemy_right_big_1.png').convert_alpha()
             big_enemy_2 = pygame.image.load('images/enemy/enemy_right_big_2.png').convert_alpha()
             self.frames = [big_enemy_1, big_enemy_2]
             y_pos = 450

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900,1100),y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
             self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100 or self.rect.x >= 1300:
               self.kill()


