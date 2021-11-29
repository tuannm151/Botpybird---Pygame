from constants import ITEMS_DROP_VEL, OBJ_SPEED, WIN_WIDTH, WIN_HEIGHT
from sprites import CRATE_IMG, RUNE_IMG, STAR_IMG, ENEMY, ENEMYDAMAGED, ENEMYEXPLODE
import pygame
import random


class Enemy:
    def __init__(self, x):
        self.x = x
        self.vel = 50
        self.y = random.randrange(50, 200)
        self.isItem = False
        self.image = ENEMY
        self.delay = 100
        self.health = 30
        self.tickDelay = 0
        self.canShoot = False
        self.isDamaged = False
        self.isDead = False
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        # self.color = (random.randint(0, 255), random.randint(
        #     0, 255), random.randint(0, 255))

    def update(self, playerY, playerX):
        if(self.isDamaged):
            self.image = ENEMYDAMAGED
            self.health -= 1
            if(self.health < 0):
                self.image = ENEMYEXPLODE
                self.isDead = True
        else:
            self.image = ENEMY

        if(self.x - playerX > WIN_WIDTH - 250):
            self.x -= self.vel
        else:
            self.x = playerX + 150

        if self.tickDelay < 100 and self.tickDelay % 10 == 0 and abs(self.y - playerY) < 200:
            moveDirection = bool(random.getrandbits(1))
            if moveDirection:
                self.moveDown()
            else:
                self.moveUp()
            self.canShoot = False
            if(self.tickDelay > 42 and self.tickDelay < 48):
                self.canShoot = True

            if(self.y < 100 or self.y >= WIN_HEIGHT-100):
                self.y = random.randrange(300, WIN_HEIGHT)

        self.tickDelay += 1
        if(self.tickDelay > self.delay*1.3):
            self.tickDelay = 0
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def moveUp(self):
        self.y = self.y - self.vel

    def moveDown(self):
        self.y = self.y + self.vel

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
