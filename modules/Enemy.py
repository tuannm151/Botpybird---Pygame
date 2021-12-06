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
        self.health = random.randrange(ENEMY_BASE_HEALTH, ENEMY_MAX_HEALTH)
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

            if(self.y < 100 or self.y >= WIN_HEIGHT-200):
                self.y = random.randrange(300, WIN_HEIGHT)

        self.tickDelay += 1
        if(self.tickDelay > self.delay*1.3):
            self.tickDelay = 0
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def hit(self):
        self.isDamaged = True
        self.health -= PROJECTILE_DAMAGE
        if(self.health < 0):
            self.isDead = True

    def moveUp(self):
        self.y = self.y - random.randrange(20, self.vel)

    def moveDown(self):
        self.y = self.y + random.randrange(20, self.vel)

    def render(self, win):
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
