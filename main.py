import pygame
import random
import math
from pygame import mixer

# Initialize pygame
pygame.init()

# Create screen window with background
screen = pygame.display.set_mode((800,600))
background = pygame.image.load('space.jpg')

# Background Music
mixer.music.load('background.mp3')
mixer.music.play(-1)

# Title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

# Earth
earthImg = pygame.image.load('earth.png')
earth1X = 770
earth1Y = 440
earth2X = 0
earth2Y = 440

def earth(x, y):
    screen.blit(earthImg,(x, y))

# Player
playerImg = pygame.image.load('ship.png')
playerX = 370
playerY = 480
playerX_change = 0

def player(x, y):
    screen.blit(playerImg,(x, y))

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 10

for i in range(num_of_enemies):  
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(30,736))
    enemyY.append(random.randint(30,150))
    enemyX_change.append(0.2)
    enemyY_change.append(80)

def enemy(x, y):
    screen.blit(enemyImg[0],(x, y))

# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletY_change = 2
bullet_state = "ready" # ready for ready to fire (not on screen) and fire for shooting the bullet(on screen)

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg,(x + 16, y + 10))

def isCollision(x1, y1, x2, y2):
    distance = math.sqrt(math.pow(x1-x2, 2) + math.pow(y1-y2, 2))
    if distance <= 24:
        return True
    return False

# Score
score = 0
score_font = pygame.font.Font('freesansbold.ttf', 32)
scoreX = 650
scoreY = 10

def show_score(x, y):
    show = score_font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(show, (x, y))

# Game over text
over_font = pygame.font.Font('freesansbold.ttf', 64)
def game_over_text():
    over_text = over_font.render("GAME OVER!", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

# Game loop
running = True
while running:
    #screen.fill((0, 0, 0))
    screen.blit(background,(0, 0))
    speed = 0.2

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.4
            if event.key == pygame.K_RIGHT:
               playerX_change = 0.4
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('pew.mp3')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Checking for player boundaries
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    player(playerX, playerY)

    # Checking for enemies boundaries and its movement
    for i in range(num_of_enemies):
        # Game over
        if enemyY[i] >= 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            earth1Y = 2000
            earth2Y = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = speed
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -speed
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            hit_sound = mixer.Sound('hit.mp3')
            hit_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score += 1
            enemyX[i] = random.randint(0,736)
            enemyY[i] = random.randint(50,150)
        enemy(enemyX[i], enemyY[i])

        # Increasing difficulty
        speed += 0.025
    
    # Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    earth(earth1X,earth1Y)
    earth(earth2X,earth2Y)

    show_score(scoreX, scoreY)
    pygame.display.update()

# done