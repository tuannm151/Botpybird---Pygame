import pygame
from constants import PROJECTILE_VEL, OBJ_SPEED
from sprites import PJ_IMGS, EXPLODED_IMGS


class Projectile:
    def __init__(self, x, y):
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
        self.hasExploded = False

    def move(self):
        if not self.isExploding:
            self.x += self.vel
        else:
            self.x -= OBJ_SPEED
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

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

    def render(self, win):
        win.blit(self.image, (self.x, self.y))

    def get_mask(self):
        return self.mask
