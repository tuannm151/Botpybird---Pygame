import pygame
import random
from sprites import OB_BOTTOM, OB_TOP, OB_TERRAIN
from constants import OBJ_SPEED, WIN_HEIGHT


class Obstacle():
    GAP = 80
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

    def render(self, win):
        win.blit(self.OBbot, (self.x, self.bottom))
        win.blit(self.OBtop, (self.x, self.top))

    def get_mask(self):
        return pygame.mask.from_surface(self.OBbot)

    def collide(self, player):
        player_mask = player.get_mask()
        top_mask = pygame.mask.from_surface(self.OBtop)
        bottom_mask = pygame.mask.from_surface(self.OBbot)

        top_offset = (self.x - player.x, self.top - round(player.y))
        bottom_offset = (self.x - player.x, self.bottom -
                         round(player.y) + self.GAP-40)

        b_point = player_mask.overlap(bottom_mask, bottom_offset)
        t_point = player_mask.overlap(top_mask, top_offset)

        if(t_point or b_point):
            return True
        return False

    def set_vel(self, vel):
        self.VEL = vel
