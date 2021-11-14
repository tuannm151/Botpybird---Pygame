import pygame
import neat
import time
import os
import random
from sprites import IDLE_IMGS, OB_BOTTOM, UP_IMGS, BG_IMG, OB_TOP, OB_TERRAIN
from constants import OBJ_SPEED, WIN_WIDTH, WIN_HEIGHT, SCENE_SPEED, PLAYER_VEL

pygame.font.init()
STAT_FONT = pygame.font.SysFont("comicsans", 40)


class Player:

    def __init__(self, x, y):
        self.y = y
        self.x = x
        self.vel = PLAYER_VEL

        self.idle = True
        self.height = self.y
        self.current_sprite = 0
        self.sprites = IDLE_IMGS
        self.image = self.sprites[0]
        self.tick = 0
        self.animationsTime = 5
        self.up_pressed = False
        self.down_pressed = False
        self.isFlapUp = False

        self.rect = self.image.get_rect()
        self.rect.topleft = [x, y]

    def update(self):
        self.sprites = IDLE_IMGS
        if(self.up_pressed and not self.down_pressed):
            self.moveUp()
        if(not self.up_pressed and self.down_pressed):
            self.moveDown()
        self.tick += 1
        if(self.tick > self.animationsTime):
            if(self.isFlapUp):
                self.current_sprite -= 1
                if(self.current_sprite <= 0):
                    self.isFlapUp = False
            else:
                self.current_sprite += 1
                if(self.current_sprite >= len(self.sprites) - 1):
                    self.isFlapUp = True
            self.tick = 0
        if(self.current_sprite == 0):
            self.rect.topleft = [self.x, self.y-15]
        else:
            self.rect.topleft = [self.x, self.y]
        self.image = self.sprites[self.current_sprite]

    def render(self, win):
        win.blit(self.image, self.rect)

    def moveUp(self):
        self.y = self.y - self.vel
        self.sprites = UP_IMGS
        self.current_sprite = 0

    def moveDown(self):
        self.y = self.y + self.vel

    def get_mask(self):
        return pygame.mask.from_surface(self.image)


class Obstacle():
    GAP = 70
    VEL = OBJ_SPEED

    def __init__(self, x):
        self.x = x
        self.height = random.randrange(0, WIN_HEIGHT-50)
        self.distance = 400

        self.top = 0
        self.bottom = 0
        self.OBbot = pygame.transform.scale(random.choice(
            OB_BOTTOM) if self.height > 200 else random.choice(OB_TERRAIN), (150, self.height))
        self.OBtop = pygame.transform.scale(random.choice(OB_TOP), (150, max(
            WIN_HEIGHT - self.OBbot.get_height() - self.GAP, 0)))

        # determine if player has passed the obstacle
        self.passed = False
        self.set_height()

    def set_height(self):
        self.top = -40
        self.bottom = WIN_HEIGHT + 40 - self.height

    def move(self):
        self.x -= self.VEL

    def draw(self, win):
        win.blit(self.OBbot, (self.x, self.bottom))
        win.blit(self.OBtop, (self.x, self.top))

    def collide(self, player):
        player_mask = player.get_mask()
        top_mask = pygame.mask.from_surface(self.OBtop)
        bottom_mask = pygame.mask.from_surface(self.OBbot)

        top_offset = (self.x - player.x, self.top - round(player.y))
        bottom_offset = (self.x - player.x, self.bottom - round(player.y))

        b_point = player_mask.overlap(bottom_mask, bottom_offset)
        t_point = player_mask.overlap(top_mask, top_offset)

        if(t_point or b_point):
            return True
        return False


def draw_window(win, player, bg_pos, obstacles, score):
    win.fill((0, 0, 0,))
    win.blit(BG_IMG, (bg_pos, 0))
    win.blit(BG_IMG, (WIN_WIDTH+bg_pos, 0))

    for obstacle in obstacles:
        obstacle.draw(win)

    text = STAT_FONT.render("Score: " + str(score), 1, (255, 255, 255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))
    player.update()
    player.render(win)
    pygame.display.update()


def main():
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    player = Player(150, 250)
    isRun = True
    clock = pygame.time.Clock()
    bg_pos = 0
    obstacles = [Obstacle(600)]
    score = 0

    while isRun:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isRun = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    player.down_pressed = True
                if event.key == pygame.K_UP:
                    player.up_pressed = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    player.down_pressed = False
                if event.key == pygame.K_UP:
                    player.up_pressed = False
        draw_window(win, player, bg_pos, obstacles, score)
        bg_pos -= OBJ_SPEED
        if(bg_pos == -WIN_WIDTH):
            bg_pos = 0

        toRemove = []
        add_obstacle = False
        for obstacle in obstacles:
            if(obstacle.collide(player)):
                pass
            if(obstacle.x + obstacle.OBtop.get_width() < 0):
                toRemove.append(obstacle)
            if not obstacle.passed and obstacle.x < player.x:
                obstacle.passed = True
                add_obstacle = True

            obstacle.move()
        if(add_obstacle):
            score += 1
            obstacles.append(Obstacle(600))
        for r in toRemove:
            obstacles.remove(r)

        cur_pos = player.y + player.image.get_height()
        if cur_pos <= 0 or cur_pos >= WIN_HEIGHT:
            pass
    pygame.quit()
    quit()


main()


