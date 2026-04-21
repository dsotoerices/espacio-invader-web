import pygame
import random
import math
import sys
import os
import asyncio 

# Inicializar pygame
pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Rutas corregidas para Pygbag y Vercel
def resource_path(relative_path):
    return os.path.join(os.getcwd(), relative_path)

# Cargar recursos
# Importante: Si esto falla, el juego se queda en negro. 
# Verifica que las carpetas en GitHub se llamen exactamente como aquí (minúsculas/mayúsculas)
background = pygame.image.load(resource_path('assets/images/background.png'))
icon = pygame.image.load(resource_path('assets/images/ufo.png'))

# --- SECCIÓN DE AUDIO (COMENTADA PARA EVITAR PANTALLA NEGRA) ---
# Pygbag tiene problemas con MP3. Una vez que el juego funcione, 
# intenta convertir a .ogg y reactivar estas líneas.
# pygame.mixer.music.load(resource_path('assets/audios/background_music.mp3'))
# pygame.mixer.music.play(-1)
# --------------------------------------------------------------

playerimg = pygame.image.load(resource_path('assets/images/space-invaders.png'))
bulletimg = pygame.image.load(resource_path('assets/images/bullet.png'))
over_font = pygame.font.Font(resource_path('assets/fonts/RAVIE.TTF'), 60)
font = pygame.font.Font(resource_path('assets/fonts/comicbd.ttf'), 32)

pygame.display.set_caption("Space Invader")
pygame.display.set_icon(icon)
clock = pygame.time.Clock()

playerX, playerY = 370, 470
playerx_change = 0
score = 0
bulletX, bulletY = 0, 480
bulletY_change = 10
bullet_state = "ready"

enemyimg, enemyX, enemyY, enemyX_change, enemyY_change = [], [], [], [], []
no_of_enemies = 10

for i in range(no_of_enemies):
    # Cargamos el enemigo (asegúrate que enemy1.png existe)
    enemyimg.append(pygame.image.load(resource_path('assets/images/enemy1.png')))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(0, 150))
    enemyX_change.append(5)
    enemyY_change.append(20)

def show_score():
    score_value = font.render("SCORE " + str(score), True, (255, 255, 255))
    screen.blit(score_value, (10, 10))

def player(x, y):
    screen.blit(playerimg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg, (x + 16, y + 10))

def isCollision(ex, ey, bx, by):
    distance = math.sqrt((math.pow(ex-bx, 2)) + (math.pow(ey-by, 2)))
    return distance < 27

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    text_rect = over_text.get_rect(center=(int(screen_width/2), int(screen_height/2)))
    screen.blit(over_text, text_rect)

async def main():
    global score, playerX, playerx_change, bulletX, bulletY, bullet_state

    in_game = True
    while in_game:
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                in_game = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT: playerx_change = -5
                if event.key == pygame.K_RIGHT: playerx_change = 5
                if event.key == pygame.K_SPACE and bullet_state == "ready":
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                    playerx_change = 0

        playerX += playerx_change
        playerX = max(0, min(playerX, 736))

        for i in range(no_of_enemies):
            if enemyY[i] > 440:
                for j in range(no_of_enemies): enemyY[j] = 2000
                game_over_text()
                break

            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0 or enemyX[i] >= 736:
                enemyX_change[i] *= -1
                enemyY[i] += enemyY_change[i]

            if isCollision(enemyX[i], enemyY[i], bulletX, bulletY):
                bulletY = 480
                bullet_state = "ready"
                score += 1
                enemyX[i], enemyY[i] = random.randint(0, 736), random.randint(0, 150)
            enemy(enemyX[i], enemyY[i], i)

        if bullet_state == "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change
            if bulletY < 0:
                bulletY = 480
                bullet_state = "ready"
        
        player(playerX, playerY)
        show_score()
        pygame.display.update()
        
        # Pausa asíncrona para que el navegador no se bloquee
        await asyncio.sleep(0)
        clock.tick(60) 

# Ejecutar el juego
asyncio.run(main())