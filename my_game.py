import pygame
from sys import exit
from random import randint

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

def obstable_movment(obstacle_list, surf, step):
    """ Move the enemey list """
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= step
            screen.blit(surf, obstacle_rect)
        # Copy only rect that are in the screen
        obstacle_list = [obstacle for obstacle in obstacle_list if 1300 >= obstacle.x >= -300]
        return obstacle_list
    else:
        return []

def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True

pygame.init()

# Init the screen
width = 800
height = 480
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Very Cool Game")
clock = pygame.time.Clock()
game_active = True
start_time = 0
# creating text
text_font = pygame.font.Font('fonts/pixeltype.ttf', 40)

# Create surface and rect for game objects
sky_surf = pygame.image.load('images/background/sky.png').convert()
ground_surf = pygame.image.load('images/background/ground_2.png').convert()

# we use .conver_alph() to speed up the game
hero_surf = pygame.image.load('images/hero/kickass_left.png').convert_alpha()
hero_rect = hero_surf.get_rect(midbottom = (150,450))

# obstacles enemies
little_enemy_surf = pygame.image.load('images/enemy/enemy_right_small.png').convert_alpha()
# enemy_rect = enemy_surf.get_rect(midbottom = (900, 450))

# Big enemy
big_enemy_surf = pygame.image.load('images/enemy/enemy_right_big.png').convert_alpha()
big_enemy_list = []
littele_enemy_list = []

# score_surf = text_font.render('Lets Kick some Ass', False, (64,64,64))
# score_rect = score_surf.get_rect(topleft = (180,70))

# continue the game after gameover
cont_surf = text_font.render('Press space to continue or Q to quit', False, (64,64,64))
cont_rect = cont_surf.get_rect(center = (400, 400))

# creating player properties
hero_gravity = 0

player_avatar_surf = pygame.image.load('images/hero/kickass_left.png').convert_alpha()
player_avater_surf = pygame.transform.rotozoom(player_avatar_surf, 0, 2) # scaling & rotating
player_avatar_rect = player_avatar_surf.get_rect(center = (400,250))

# Creating spaceships
spaceship_surf = pygame.image.load('images/spaceships/spaceship.png').convert_alpha()
spaceship_list = []

# Create sattelites
sattelite_surf = pygame.image.load('images/spaceships/sattelite.png').convert_alpha()
sattelite_list = []

# create lazer
lazer_surf = pygame.image.load('images/fire/lazer_right.png').convert_alpha()
lazer_rect = lazer_surf.get_rect(center = (hero_rect.right-5, hero_rect.y+40))
lazer_shoot = False

#Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1600)

# Game loop
while True:
    # check if user close the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if hero_rect.collidepoint(event.pos) and hero_rect.bottom >= 450:
                    hero_gravity = -22

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and hero_rect.bottom >= 450:
                    hero_gravity = -22

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    hero_rect.x -= 10

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    hero_rect.x += 10

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    lazer_shoot = True
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = pygame.time.get_ticks()//100
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                pygame.quit()
                exit()

        if event.type == obstacle_timer and game_active:
            num = randint(0,100)
            print(f"num: {num}")
            if   10 < num < 50:
                littele_enemy_list.append(little_enemy_surf.get_rect(bottomright = (randint(900,1000),450)))
            if 70 < num < 90:
                big_enemy_list.append(big_enemy_surf.get_rect(bottomright = (randint(1000,1500),450)))
            if 50 < num < 70:
                print("spawn sattelite")
                sattelite_list.append(sattelite_surf.get_rect(center = (randint(1000,1500), num)))
            if 90 < num < 100:
                print("spawn spaceship")
                spaceship_list.append(spaceship_surf.get_rect(center = (randint(-300, -100), num)))

    if game_active:
        # Other game logic and rendering code...
        screen.blit(sky_surf,(0,0))
        screen.blit(ground_surf,(0,380))
        current_score = display_score()

        # Handle ground obstacle and flying object
        big_enemy_list = obstable_movment(big_enemy_list, big_enemy_surf, 1)
        littele_enemy_list = obstable_movment(littele_enemy_list, little_enemy_surf, 3)
        sattelite_list = obstable_movment(sattelite_list, sattelite_surf, 1)
        spaceship_list = obstable_movment(spaceship_list, spaceship_surf, -3)

        #move lazer
        if (lazer_shoot):
            screen.blit(lazer_surf, lazer_rect)
            lazer_rect.x += 5
            if(lazer_rect.x > 900):
                lazer_shoot = False
                lazer_rect.x = hero_rect.right


        # Handle the Hero movement print and collision
        hero_gravity += 1
        hero_rect.y += hero_gravity
        if hero_rect.bottom >= 450:
            hero_rect.bottom = 450
        screen.blit(hero_surf, hero_rect)

        # check for collision
        # if enemy_rect.colliderect(hero_rect):
        #     # game_active = False
        #     pass
        game_active = collisions(hero_rect, big_enemy_list) and collisions(hero_rect, littele_enemy_list)

    else:
        with open('scores/best_score.txt', 'r') as fr:
            best_score = fr.readline()
        if current_score > int(best_score):
            with open('scores/best_score.txt', 'w') as fw:
                fw.write(f"{current_score}")

        # Display the end game screen
        display_end(current_score)

        # Return player to start point
        hero_rect.midbottom = (150,450)
        hero_gravity = 0
        
        # Clear all lists for new start
        littele_enemy_list.clear()
        big_enemy_list.clear()
        sattelite_list.clear()
        spaceship_list.clear()

    # update the screen
    pygame.display.update()
    clock.tick(60)

