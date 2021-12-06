from constants import WIN_WIDTH, WIN_HEIGHT, PROJECTILE_DAMAGE, ENEMY_BASE_HEALTH, ENEMY_MAX_HEALTH
from sprites import ENEMY, ENEMYDAMAGED, ENEMYEXPLODE
import pygame
import random


class Enemy:
    def __init__(self, x):
        self.x = x
        self.vel = 50
        self.y = random.randrange(50, 200)
        self.isItem = False
        self.image = ENEMY
        self.delay = random.randrange(60, 100)

        self.max_health = random.randrange(ENEMY_BASE_HEALTH, ENEMY_MAX_HEALTH)
        self.health = self.max_health
        self.target_health = self.max_health

        self.health_bar_length = WIN_WIDTH - 50
        self.health_bar_y_pos = WIN_HEIGHT - 40

        self.health_ratio = self.max_health / self.health_bar_length
        self.health_change_speed = 3

        self.tickDelay = 0
        self.canShoot = False
        self.isDamaged = False
        self.isEqual = False
        self.isDead = False
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        # self.color = (random.randint(0, 255), random.randint(
        #     0, 255), random.randint(0, 255))

    def update(self, playerY, playerX):
        if(self.isDamaged):
            self.image = ENEMYDAMAGED
        elif(self.isDead):
            self.image = ENEMYEXPLODE
        else:
            self.image = ENEMY

        if(self.x - playerX > WIN_WIDTH - 220):
            self.x -= self.vel
        else:
            self.x = playerX + random.randrange(150, 180)
        self.isEqual = False
        if self.tickDelay < 100 and abs(self.y - playerY) < 150:
            moveDirection = bool(random.getrandbits(1))
            if(self.tickDelay % 40 == 0):
                self.isEqual = True
            if self.tickDelay % 15 == 0:
                if moveDirection:
                    self.moveDown()
                else:
                    self.moveUp()

            if(self.y < 100 or self.y >= WIN_HEIGHT-150):
                self.y = random.randrange(300, WIN_HEIGHT)

        self.tickDelay += 1
        if(self.tickDelay > self.delay*1.3):
            self.tickDelay = 0
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def hit(self):
        self.isDamaged = True
        self.target_health -= PROJECTILE_DAMAGE
        if(self.target_health <= 0):
            self.target_health = 0
            self.isDead = True

    def healthTransition(self, win):
        health_bar_width = self.health / self.health_ratio
        transition_width = 0
        transition_color = (0, 0, 255)

        if self.health > self.target_health:
            health_bar_width = self.target_health / self.health_ratio
            self.health -= self.health_change_speed
            transition_width = abs(
                (self.target_health - self.health))/self.health_ratio
            transition_color = (255, 255, 0)

        health_bar_rect = pygame.Rect(
            20, self.health_bar_y_pos, health_bar_width, 25)
        transition_bar_rect = pygame.Rect(
            health_bar_rect.right, self.health_bar_y_pos, transition_width, 25)

        pygame.draw.rect(win, (15, 44, 103), health_bar_rect)
        pygame.draw.rect(win, transition_color, transition_bar_rect)
        pygame.draw.rect(win, (255, 255, 255),
                         (20, self.health_bar_y_pos, self.health_bar_length, 25), 4)

    def moveUp(self):
        self.y = self.y - random.randrange(20, self.vel)

    def moveDown(self):
        self.y = self.y + random.randrange(20, self.vel)

    def render(self, win):
        self.healthTransition(win)
        win.blit(self.image, (self.x, self.y))
        # pygame.draw.rect(win, self.color, (self.rect.x,
        #                                    self.rect.y, self.rect.width, self.rect.height), 2)

    def collide(self, obj):
        obj_mask = obj.get_mask()
        mask = pygame.mask.from_surface(self.image)
        offset = (self.rect[0] - obj.rect[0], self.rect[1] - obj.rect[1])
        return mask.overlap(obj_mask, offset)

    def get_mask(self):
        return pygame.mask.from_surface(self.image)
