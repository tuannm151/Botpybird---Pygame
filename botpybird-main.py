from constants import OBJ_SPEED, SCENE_SPEED, WIN_WIDTH, WIN_HEIGHT, EXPLODING_TIME, HEART_HEALING_RATE
from sprites import BG_IMG, MENU_IMG
from modules.Player import Player
from modules.Obstacle import Obstacle
from modules.Projectile import Projectile
from modules.Enemy import Enemy
from modules.Item import Item
from modules.bgm import *
import pygame
import time
import os


pygame.font.init()
STAT_FONT = pygame.font.Font("8-bit-pusab.ttf", 20)


def draw_window(win, player, bg_pos, obstacles, projectiles, items, enemy, score, gameover, gamewin):
    win.fill((0, 0, 0))
    win.blit(BG_IMG, (bg_pos, 0))
    win.blit(BG_IMG, (WIN_WIDTH+bg_pos, 0))
    for obstacle in obstacles:
        obstacle.render(win)
    for projectile in projectiles:
        projectile.update()
        projectile.render(win)

    for item in items:
        item.move()
        item.render(win)

    enemy.update(player.getY(), player.y)
    enemy.render(win)

    text = STAT_FONT.render("Score: " + str(score), 1, (255, 255, 255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

    if(gameover):
        text = STAT_FONT.render("You lost!", True, (255, 255, 255))
        text_rect = text.get_rect(center=(WIN_WIDTH/2, WIN_HEIGHT/2-100))
        win.blit(text, text_rect)

        text = STAT_FONT.render(
            "Press enter to try again!", True, (255, 255, 255))
        text_rect = text.get_rect(center=(WIN_WIDTH/2, WIN_HEIGHT/2))
        win.blit(text, text_rect)

    if(gamewin):
        text = STAT_FONT.render("You win!", True, (255, 255, 255))
        text_rect = text.get_rect(center=(WIN_WIDTH/2, WIN_HEIGHT/2-100))
        win.blit(text, text_rect)

        text = STAT_FONT.render(
            "Press enter to play again!", True, (255, 255, 255))
        text_rect = text.get_rect(center=(WIN_WIDTH/2, WIN_HEIGHT/2))
        win.blit(text, text_rect)

    player.update()
    player.render(win)
    pygame.display.update()


def main(window):
    win = window
    player = Player(100, 250)
    isRun = True
    clock = pygame.time.Clock()
    bg_pos = 0
    obstacles = [Obstacle(600)]
    score = 0
    projectiles = []
    items = []
    enemy = Enemy(2000)
    last_spawn = 0
    boost_time = 200
    boost_time_offset = 0
    obj_vel = OBJ_SPEED
    bg_vel = SCENE_SPEED
    prev_vel = SCENE_SPEED
    while isRun:
        clock.tick(30)
        now = pygame.time.get_ticks()
        if(now - last_spawn > 4000):
            if(not player.isBoosted and not player.isCrazy):
                items.append(Item(1000))

            last_spawn = now
        if(player.isBoosted):
            if(boost_time_offset < boost_time):
                if(bg_vel < 25):
                    bg_vel += 0.3
                if(obj_vel < 40):
                    obj_vel += 0.3
                for obj in obstacles:
                    obj.set_vel(obj_vel)
                boost_time_offset += 1
            else:
                if(bg_vel > 8):
                    bg_vel -= 0.4
                if(obj_vel > prev_vel):
                    obj_vel -= 0.4
                for obj in obstacles:
                    obj.set_vel(obj_vel)
                if(bg_vel <= 8 and obj_vel <= prev_vel+4):
                    player.isBoosted = False
                    boost_time_offset = 0
                    prev_vel += 4
                    obj_vel = prev_vel
                    for obj in obstacles:
                        obj.set_vel(obj_vel)
        if(player.isCrazy):
            if(boost_time_offset < boost_time):
                boost_time_offset += 1
            else:
                boost_time_offset = 0
                player.isCrazy = False
        if(enemy.isEqual):
            enemyBullet = Projectile(enemy.x - 30, enemy.y, True)
            projectiles.append(enemyBullet)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isRun = False
                win.blit(pygame.transform.scale(
                    MENU_IMG, (WIN_WIDTH, WIN_HEIGHT)), (0, 0))
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    player.down_pressed = True
                if event.key == pygame.K_UP:
                    player.up_pressed = True
                if event.key == pygame.K_SPACE:
                    shootSound.play()
                    player.shooting()
                    projectiles.append(Projectile(player.x + 20, player.y))
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    player.down_pressed = False
                if event.key == pygame.K_UP:
                    player.up_pressed = False

        bg_pos -= bg_vel
        if(bg_pos < -WIN_WIDTH):
            bg_pos = 0

        toRemovePj = []
        toExplodePj = []

        #--------- Obstacles handle ---------999ik7#
        toRemoveOb = []
        add_obstacle = False
        for obstacle in obstacles:
            if(obstacle.collide(player)):
                if(not player.isBoosted and not player.isCrazy):
                    player.isLost = True
            for projectile in projectiles:
                if(not projectile.isEnemy and obstacle.collide(projectile) and not obstacle.passed):
                    if(player.isCrazy):
                        obstacle.isDestroyed = True
                        explodeSound.play()
                    toExplodePj.append(projectile)

            if(obstacle.x + obstacle.OBtop.get_width() < 0):
                toRemoveOb.append(obstacle)

            if not obstacle.passed and obstacle.x < player.x:
                obstacle.passed = True
                if(not player.isBoosted):
                    add_obstacle = True
                else:
                    obstacles.append(Obstacle(2*WIN_WIDTH))

            for item in items:
                if(obstacle.collide(item)):
                    items.remove(item)

            obstacle.move()

        if(add_obstacle):
            score += 1
            obstacles.append(Obstacle(WIN_WIDTH))

        for r in toRemoveOb:
            obstacles.remove(r)

         #-------------Item handling ---------------#

        for item in items:
            if(item.x < 0):
                items.remove(item)
                continue
            if(item.isItem and item.collide(player)):
                itemSound.play()
                if(item.isStar):
                    player.isCrazy = True
                elif(item.isRune):
                    player.isBoosted = True
                    rocketSound.play()
                elif(item.isHeart):
                    player.get_health(player.max_health*HEART_HEALING_RATE)
                items.remove(item)

        #--------- Projectiles handle ---------#
        for projectile in projectiles:

            for item in items:
                if(not projectile.isEnemy and item.collide(projectile)):
                    # explodeSound.play()
                    item.update()
                    toExplodePj.append(projectile)

            if(not projectile.isEnemy and enemy.collide(projectile)):
                # explodeSound.play()
                enemy.isDamaged = True
                enemy.hit()
                toExplodePj.append(projectile)
                score += 5

            if(projectile.isEnemy and player.collide(projectile)):
                player.hit()
                toExplodePj.append(projectile)

            if(projectile.x > WIN_WIDTH+50 or projectile.x < -50):
                toRemovePj.append(projectile)

            projectile.move()

        for projectile in toExplodePj:
            projectile.isExploding = True
            if(not projectile.hasExploded):
                if(not projectile.isEnemy):
                    explodeSound.play()
                projectile.hasExploded = True
            if(projectile.explodingTick > EXPLODING_TIME):
                toExplodePj.remove(projectile)
                toRemovePj.append(projectile)
            else:
                projectile.explodingTick += 1

        for r in toRemovePj:
            if(r in projectiles):
                projectiles.remove(r)

        cur_pos = player.y
        if cur_pos <= 0 or cur_pos >= WIN_HEIGHT:
            player.isLost = True
        if(player.isLost):
            lostSound.play()
            isRun = False
        if(enemy.isDead):
            player.isWin = True
            isRun = False
        draw_window(win, player, bg_pos, obstacles,
                    projectiles, items, enemy, score, player.isLost, player.isWin)
        enemy.isDamaged = False


def main_menu():
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption('BOTPYBIRD')
    isPlaying = False
    isInMenu = True
    clock = pygame.time.Clock()
    music = pygame.mixer.music.load("bgm/theme.mp3")
    win.blit(pygame.transform.scale(
        MENU_IMG, (WIN_WIDTH, WIN_HEIGHT)), (0, 0))
    pygame.mixer.music.play(-1)
    while(isInMenu):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not isPlaying:
                    isPlaying = True
                    main(win)
                if isPlaying and event.key == pygame.K_RETURN:
                    main(win)
        pygame.display.update()
        clock.tick(30)


main_menu()
