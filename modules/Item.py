from constants import ITEMS_DROP_VEL, OBJ_SPEED
from sprites import CRATE_IMG, RUNE_IMG
import pygame
import random


class Item:
    def __init__(self, x):
        self.x = x
        self.vel = ITEMS_DROP_VEL
        self.top = random.randrange(50, 200)
        self.y = self.top
        self.isItem = False
        self.isColliding = False
        self.image = pygame.transform.scale(CRATE_IMG, (50, 50))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def move(self):
        if not self.isItem:
            self.y += self.vel
        self.x -= OBJ_SPEED
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self):
        self.isItem = True
        self.image = pygame.transform.scale(RUNE_IMG, (50, 50))
        if(self.isColliding):
            pass

    def render(self, win):
        win.blit(self.image, (self.x, self.y))

    def collide(self, obj):
        obj_mask = obj.get_mask()
        mask = pygame.mask.from_surface(self.image)
        offset = (self.rect[0] - obj.rect[0], self.rect[1] - obj.rect[1])

        return mask.overlap(obj_mask, offset)

    def get_mask(self):
        return pygame.mask.from_surface(self.image)
