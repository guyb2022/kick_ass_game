import pygame
from sys import exit
from random import randint, choice
from player import Player
from obstacle import Obstacle
from background import Background
from missile import Missile
import pygame

WIDTH, HEIGHT = 800, 600

def display_score():
    """
    Display the score in seconds from program starts
    """
    current_time = pygame.time.get_ticks()//100 - start_time
    score_surf = text_font.render(f"SCORE: {current_time}", False, (64,64,64))
    score_rect = score_surf.get_rect(topleft = (100,10))
    screen.blit(score_surf, score_rect)
    return current_time

def display_end(current_score):
    """
    Display starting and end game menu
    """
    if current_score >= int(best_score):
        best_score_surf = text_font.render(f"You Are The Heighst S Kicker: {best_score}", False, (255,255,0))
    else:
        best_score_surf = text_font.render(f"Sorry Try Again, Heighst Score: {best_score}", False, (255,255,0))

    best_score_rect = best_score_surf.get_rect(center = (400, 90))
    screen.fill((95,130,160))
    screen.blit(best_score_surf, best_score_rect)
    screen.blit(player_avatar_surf, player_avatar_rect)
    gameover_surf = text_font.render(f"Yout Score: {current_score}", False, (64,64,64))
    gameover_rect = gameover_surf.get_rect(midbottom = (400,150))
    screen.blit(gameover_surf, gameover_rect)
    screen.blit(cont_surf, cont_rect)

def collision_sprite():
    player_collision = pygame.sprite.spritecollide(player.sprite, obstacle_group, False)
    missile_collisions = pygame.sprite.groupcollide(missile_group, obstacle_group, False, False)

    if player_collision:
        obstacle_group.empty()
        return False
    # Check for missile-obstacle collision
    elif missile_collisions:
        for missile in missile_collisions:
            if pygame.sprite.spritecollide(missile, obstacle_group, False):
                missile.kill()
        for obstacle in missile_collisions.values():
            obstacle_group.remove(*obstacle)
        return True

    else:
        return True

# Init pygame
pygame.init()

# Init the screen
width = 800
height = 480
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Very Cool Game")
text_font = pygame.font.Font('fonts/pixeltype.ttf', 40)
clock = pygame.time.Clock()
game_active = True
start_time = 0
score = 0

# Add sound to game
# bg_music = pygame.mixer.Sound('audio/music.wav')
# bg_music.play(loops = -1)

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()
background_group = pygame.sprite.Group()
missile_group = pygame.sprite.Group()

# Create surface and rect for game objects
sky_surf = pygame.image.load('images/background/sky.png').convert()
ground_surf = pygame.image.load('images/background/ground_2.png').convert()

# continue the game after gameover
cont_surf = text_font.render('Press space to continue or Q to quit', False, (64,64,64))
cont_rect = cont_surf.get_rect(center = (400, 400))

player_avatar_surf = pygame.image.load('images/hero/kickass_right_1.png').convert_alpha()
player_avater_surf = pygame.transform.rotozoom(player_avatar_surf, 0, 2) # scaling & rotating
player_avatar_rect = player_avatar_surf.get_rect(center = (400,250))

#Timer
obstacle_timer = pygame.USEREVENT + 1
background_timer = pygame.USEREVENT + 3
pygame.time.set_timer(obstacle_timer, 1700)
pygame.time.set_timer(background_timer, 1300)

face_right = False
face_left = False
fire_enable = False

# Starting the Main game loop
while True:
    # check if user close the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == obstacle_timer:
                enemy_choice = choice(['little_enemy','little_enemy','little_enemy','big_enemy'])
                obstacle_group.add(Obstacle(enemy_choice))
                background_choice = randint(0,100)
                if 30 < background_choice < 50:
                    background_group.add(Background('sattelite'))
                elif 70 < background_choice < 90:
                    background_group.add(Background('spachship'))

            if event.type == pygame.KEYDOWN:
                if not face_left and not face_right:
                    fire_enable = False
                if event.key == pygame.K_p and fire_enable:
                    print(face_left, face_right)
                    missile_group.add(Missile(player.sprite.rect.x, player.sprite.rect.y, face_left, face_right))

                if event.key == pygame.K_e:
                    face_right = True
                    fire_enable = True

                if event.key == pygame.K_q:
                    face_left = True
                    fire_enable = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_e:
                    face_right = False

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_q:
                    face_left = False
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = pygame.time.get_ticks()//100
                face_left = False
                face_right = False
                fire_enable = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                pygame.quit()
                exit()

    if game_active:

        screen.blit(sky_surf,(0,0))
        screen.blit(ground_surf,(0,380))
        current_score = display_score()

        player.draw(screen)
        player.update(face_left , face_right)

        missile_group.draw(screen)
        missile_group.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        background_group.draw(screen)
        background_group.update()

        game_active = collision_sprite()

    else:
        with open('scores/best_score.txt', 'r') as fr:
            best_score = fr.readline()
        if current_score > int(best_score):
            with open('scores/best_score.txt', 'w') as fw:
                fw.write(f"{current_score}")

        # Display the end game screen
        display_end(current_score)

    # update the screen
    pygame.display.update()
    clock.tick(60)

