from constants import ITEMS_DROP_VEL, OBJ_SPEED
from sprites import CRATE_IMG, RUNE_IMG, STAR_IMG, HEART_IMG
import pygame
import random


class Item:
    def __init__(self, x):
        self.x = x
        self.vel = ITEMS_DROP_VEL
        self.y = random.randrange(50, 200)
        self.isItem = False
        self.isColliding = False

        self.randomItem = [False, False, False]
        self.randomItem[random.randrange(0, 3)] = True
        self.isRune = self.randomItem[0]
        self.isStar = self.randomItem[1]
        self.isHeart = self.randomItem[2]

        self.image = pygame.transform.scale(CRATE_IMG, (70, 70))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def move(self):
        if not self.isItem:
            self.y += self.vel
        self.x -= OBJ_SPEED
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def update(self):
        self.isItem = True
        if(self.isRune):
            self.image = pygame.transform.scale(RUNE_IMG, (70, 70))
        elif(self.isStar):
            self.image = pygame.transform.scale(STAR_IMG, (70, 70))
        elif(self.isHeart):
            self.image = pygame.transform.scale(HEART_IMG, (70, 70))
        self.mask = pygame.mask.from_surface(self.image)

    def render(self, win):
        win.blit(self.image, (self.x, self.y))

    def collide(self, obj):
        obj_mask = obj.get_mask()
        mask = pygame.mask.from_surface(self.image)
        offset = (self.rect[0] - obj.rect[0], self.rect[1] - obj.rect[1])

        return mask.overlap(obj_mask, offset)

    def get_mask(self):
        return pygame.mask.from_surface(self.image)
