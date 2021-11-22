import pygame
import os
from constants import WIN_WIDTH, WIN_HEIGHT

# ------ character animation sprites----------
IDLE_IMGS = []
for picIndex in range(4):
    image = pygame.image.load(os.path.join(
        'sprites', 'idle'+str(picIndex+1)+'.png'))
    IDLE_IMGS.append(image)

UP_IMGS = []
for picIndex in range(2):
    image = pygame.image.load(os.path.join(
        'sprites', 'up'+str(picIndex+1)+'.png'))
    UP_IMGS.append(image)
SHOOT_IMGS = []
for picIndex in range(10):
    image = pygame.image.load(os.path.join(
        'sprites', 'shoot'+str(picIndex+1)+'.png'))
    SHOOT_IMGS.append(image)
BOOST_IMGS = []
for picIndex in range(3):
    image = pygame.image.load(os.path.join(
        'sprites', 'boost'+str(picIndex+1)+'.png'))
    BOOST_IMGS.append(image)

DEAD_IMG = pygame.image.load(os.path.join(
    'sprites', 'dead.png'))
# ------------------------------------ #

#---------- Obstacles sprites----------------#
BG_IMG = pygame.transform.scale(
    pygame.image.load(os.path.join('sprites', 'bg-game.png')), (WIN_WIDTH, WIN_HEIGHT))

OB_TOP = []
for picIndex in range(4):
    image = pygame.image.load(os.path.join(
        'obstacles', 'tow'+str(picIndex+1)+'.png'))
    OB_TOP.append(image)

OB_BOTTOM = []
for picIndex in range(5):
    image = pygame.image.load(os.path.join(
        'obstacles', 'vol'+str(picIndex+1)+'.png'))
    OB_BOTTOM.append(image)
OB_TERRAIN = []
for picIndex in range(2):
    image = pygame.image.load(os.path.join(
        'obstacles', 'ter'+str(picIndex+1)+'.png'))
    OB_TERRAIN.append(image)
# ----------------------------------------------#

#--------------- Item sprites -------------------#
CRATE_IMG = pygame.image.load(os.path.join('items', 'crate.png'))
RUNE_IMG = pygame.image.load(os.path.join('items', 'rune.png'))
#------------------------------------------------#

# ------ projectile animation sprites----------
PJ_IMGS = []
for picIndex in range(5):
    image = pygame.image.load(os.path.join(
        'sprites', 'pj'+str(picIndex+1)+'.png'))
    PJ_IMGS.append(image)

EXPLODED_IMGS = []
for picIndex in range(6):
    image = pygame.transform.scale2x(pygame.image.load(os.path.join(
        'sprites', 'explode'+str(picIndex+1)+'.png')))
    EXPLODED_IMGS.append(image)
# ------------------------------------ #
MENU_IMG = pygame.image.load(os.path.join(
    'sprites', 'mainmenu.png'))
