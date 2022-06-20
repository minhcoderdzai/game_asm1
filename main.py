import pygame
import math
import random

from pygame import mixer

pygame.init()
#tao man hinh
screen = pygame.display.set_mode((800,600))

#background
background = pygame.image.load('background.png')
#ten va icon
pygame.display.set_caption("Sapce Invaders")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

#background sound
mixer.music.load('background.wav')
mixer.music.play(-1)

#player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0

#enemy
enemyImg =[]
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyImg.append(pygame.image.load('enemy1.png'))
    enemyX.append(random.randint(0, 800))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

#bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 3
bulletY_change = 10
bullet_state ="ready"

#Điểm
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
font1 = pygame.font.Font('freesansbold.ttf', 64)

textX = 10
textY = 10

#Game over text
over_font = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x, y):
    score = font.render("Score: " + str(score_value), True,(255, 255, 255))
    screen.blit(score, (x, y))

def game_over_score():
    score = font1.render("SCORE: " + str(score_value), True,(255, 0, 0))
    screen.blit(score, (280, 350))

def game_over_text():
    over_text = over_font.render("GAME OVER", True,(255, 255, 255))
    screen.blit(over_text, (200, 250))

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bulltet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x+16, y+10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX-bulletX,2)+math.pow(enemyY-bulletY,2))
    if distance<27:
        return True
    else:
        return False
#vong lap
running = True
while running:
    # mau nen (RGB)
    screen.fill((155, 150, 140))
    screen.blit(background,(0,0))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print('Đã thoát game')
            running = False

        if event.type == pygame.KEYDOWN:  # Nếu phím đã được nhấn thì kiểm tra đó là trái hay phải

            if event.key == pygame.K_LEFT:  # Kiểm tra xem phím mũi tên trái có đang được nhấn không
                playerX_change = -5
            if event.key == pygame.K_RIGHT:  # Kiểm tra xem phím mũi tên phải có đang được nhấn không
                 playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_Sound = mixer.Sound('laser.wav')
                    bullet_Sound.play()
                    bulletX = playerX
                    fire_bulltet(bulletX, bulletY)

        if event.type == pygame.KEYUP:  # Nếu phím được ngừng nhấn
             if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:  # Phím mũi tên trái hoặc phải được nhấc lên
                playerX_change = 0

    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >=736:
        playerX = 736

    if enemyY[i]<400:
        show_score(textX, textY)

    for i in range(num_of_enemies):
        #Game over
        if enemyY[i] > 440:  # khi 1 trong số Enemy đi đến điểm Y 40px thì game over
            for j in range(num_of_enemies):
                enemyY[j] = 2000  # không hiển thị trên màn hình

            game_over_text()
            game_over_score()

            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 19
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -19
            enemyY[i] += enemyY_change[i]

        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_Sound = mixer.Sound('explosion.wav')
            explosion_Sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)

    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state =="fire":
        fire_bulltet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)

    pygame.display.update()