import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        image_1 = pygame.image.load('images/hero/shooter_front.png').convert_alpha()
        image_2 = pygame.image.load('images/hero/shooter_right.png').convert_alpha()
        image_3 = pygame.image.load('images/hero/shooter_left.png').convert_alpha()
        image_4 = pygame.image.load('images/hero/shooter_front.png').convert_alpha()

        self.image_front = image_1
        self.image_right = image_2
        self.image_left = image_3
        self.image_jump = image_4

        self.gravity = 0
        self.image = self.image_front
        self.rect = self.image.get_rect(midbottom = (400,430))

        # self.jump_sound = pygame.mixer.Sound('audion/jump.mp3')
        # self.jump_sound.set_volume(0.5)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 430:
            self.gravity = -22
            # self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 430:
            self.rect.bottom = 430

    def animation_state(self, face_left , face_right):
        if face_right:
            self.image = self.image_right
        elif face_left:
            self.image = self.image_left
        else:
            self.image = self.image_front

    def update(self, face_left, face_right):
        self.player_input()
        self.apply_gravity()
        self.animation_state(face_left, face_right)








