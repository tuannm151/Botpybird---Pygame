import pygame
from sprites import IDLE_IMGS, UP_IMGS, SHOOT_IMGS, BOOST_IMGS, DEAD_IMG
from constants import OBJ_SPEED, WIN_WIDTH, WIN_HEIGHT, SCENE_SPEED, PLAYER_VEL


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
        self.isPlayer = True
        self.animationsTime = 5
        self.flyTime = 200
        self.flyTimeOffset = 0
        self.up_pressed = False
        self.down_pressed = False
        self.isFlapUp = False
        self.isShooting = False
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.isBoosted = False
        self.isLost = False

    def update(self):
        if(self.isLost):
            self.image = DEAD_IMG
            return
        if(self.up_pressed and not self.down_pressed):
            self.moveUp()
        if(not self.up_pressed and not self.isShooting and not self.isBoosted):
            self.sprites = IDLE_IMGS
        if(not self.up_pressed and self.down_pressed):
            self.moveDown()

        if(self.isBoosted):
            self.sprites = BOOST_IMGS

        self.tick += 1
        if(self.tick > self.animationsTime):
            if(self.isFlapUp and not self.isShooting):
                self.current_sprite -= 1
                if(self.current_sprite <= 0):
                    self.isFlapUp = False
            else:
                self.current_sprite += 1
                if(self.current_sprite >= len(self.sprites)):
                    self.isFlapUp = True
                    self.current_sprite = len(self.sprites)-1
                    self.current_sprite -= 1
                    if(self.isShooting):
                        self.isShooting = False
                        self.current_sprite = 0
                        self.animationsTime = 5
            self.tick = 0
        self.rect = self.image.get_rect()
        if(self.current_sprite == 0):
            self.rect.center = (self.x, self.y-15)
        else:
            self.rect.center = (self.x, self.y)
        if(self.current_sprite >= len(self.sprites)):
            self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]

    def shooting(self):
        if(not self.isBoosted):
            self.current_sprite = 0
            self.isShooting = True
            self.sprites = SHOOT_IMGS
            self.animationsTime = 1

    def render(self, win):
        win.blit(self.image, self.rect)

    def moveUp(self):
        self.y = self.y - self.vel
        if(not self.isBoosted):
            self.sprites = UP_IMGS

    def moveDown(self):
        self.y = self.y + self.vel

    def get_mask(self):
        return pygame.mask.from_surface(self.image)

    def set_vel(self, vel):
        self.vel = vel
