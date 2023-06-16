import pygame

class Missile(pygame.sprite.Sprite):
    def __init__(self, x, y, left, right):
        super().__init__()
        self.face_right = right
        self.face_left = left
        missile_1 = pygame.image.load('images/fire/lazer_left_1.png').convert_alpha()
        missile_2 = pygame.image.load('images/fire/lazer_right_1.png').convert_alpha()
        missile_3 = pygame.image.load('images/fire/lazer_ball.png').convert_alpha()
        if self.face_left:
            missile_image = missile_1
        elif self.face_right:
            missile_image = missile_2

        self.missile_speed = 10
        self.missile_state = "ready"
        self.x = x
        self.y = y

        self.image = missile_image
        if self.face_right:
            self.rect = self.image.get_rect(center = (self.x+140, self.y+20))
        elif self.face_left:
            self.rect = self.image.get_rect(center = (self.x-25, self.y+20))

    def update(self):
        self.missile_speed += 1
        if self.face_right:
            self.rect.x += self.missile_speed
        elif self.face_left:
            self.rect.x -= self.missile_speed
        self.destroy()

    def destroy(self):
        if self.rect.x >= 900 or self.rect.x <= -100:
            self.kill()
