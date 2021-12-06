import pygame
from constants import PROJECTILE_VEL, OBJ_SPEED
from sprites import PJ_IMGS, EXPLODED_IMGS, PJ_ENEMY
import random


class Projectile:
    def __init__(self, x, y, isEnemy=False):
        self.x = x
        self.y = y
        self.vel = PROJECTILE_VEL
        self.sprites = PJ_IMGS
        self.current_sprite = 0
        self.image = self.sprites[0]
        self.tick = 0
        self.delay = 4
        self.animationsTime = 5
        self.isExploding = False
        self.explodingTick = 0
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.isEnemy = isEnemy
        self.hasExploded = False
        # self.color = (random.randint(0, 255), random.randint(
        #     0, 255), random.randint(0, 255))

    def move(self):
        if(not self.isEnemy):
            if not self.isExploding:
                self.x += self.vel
            else:
                self.x -= OBJ_SPEED
        else:
            if not self.isExploding:
                self.x -= self.vel
            else:
                self.x -= OBJ_SPEED

    def update(self):
        if(self.isExploding):
            self.sprites = EXPLODED_IMGS
        if(self.tick > self.delay):
            self.current_sprite += 1
            if(self.current_sprite >= len(self.sprites)):
                self.current_sprite = 0
            self.tick = 0
        self.tick += 1
        self.image = self.sprites[self.current_sprite]
        if(self.isEnemy and not self.isExploding):
            self.image = PJ_ENEMY
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def render(self, win):
        win.blit(self.image, (self.x, self.y))
        # pygame.draw.rect(win, self.color, (self.rect.x,
        #                                    self.rect.y, self.rect.width, self.rect.height), 2)

    def get_mask(self):
        return self.mask
