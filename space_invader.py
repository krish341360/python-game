import math
import random

import pygame
from pygame import mixer

# Intialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('/Users/krish/Downloads/back.png')

# Sound
mixer.music.load("/Users/krish/Downloads/sound_design_texture_soundscape_lost_in_space.wav")
mixer.music.play(-1)

# Caption and Icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('/Users/krish/Downloads/ufo.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('/Users/krish/Downloads/spaceship.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('/Users/krish/Downloads/spaceship-2.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# Bullet

# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving

bulletImg = pygame.image.load('/Users/krish/Downloads/bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

score_value = 0
font = pygame.font.Font('/Users/krish/Downloads/Orbitron-Regular_65121005c9a84031bdd58dadd8bca551.ttf', 43)


textX = 10


testY = 10

# Game Over
over_font = pygame.font.Font('/Users/krish/Downloads/Orbitron-Regular_65121005c9a84031bdd58dadd8bca551.ttf', 80)


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (173, 62, 153))
    screen.blit(score, (x, y))
def text_objects(text, font):
    textSurface = font.render(text, True, (0, 0, 0))
    return textSurface, textSurface.get_rect()

def button(text, x, y, w, h, in_colour, ac_colour, action = None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    pygame.draw.rect(background, (161, 108, 158), (x, y, w, h))
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(background, (145, 0, 136), (x, y, w, h))
        if click[0] == 1 and action != None:
            if action == "play":
                pygame.quit()
                quit()
            

    smallText = pygame.font.Font("/Users/krish/Downloads/Orbitron-Regular_65121005c9a84031bdd58dadd8bca551.ttf",20)
    textSurf, textRect = text_objects(text, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    background.blit(textSurf, textRect)


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (173, 62, 153))
    screen.blit(over_text, (140, 250))
    button("QUIT", 355, 410, 100, 50, (161, 108, 158), (145, 0, 136), "play")


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:

    # RGB = Red, Green, Blue
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "fire":
                    bulletSound = mixer.Sound("/Users/krish/Downloads/zapsplat_multimedia_laser_weapon_fire_001_25877.wav")
                    bulletSound.play()
                    # Get the current x cordinate of the spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0



    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy Movement
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 400:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosionSound = mixer.Sound("/Users/krish/Downloads/sound_spark_Glitch_Factory_01_Decimated_10.wav")
            explosionSound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, testY)
    pygame.display.update()