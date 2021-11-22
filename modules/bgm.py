import pygame
pygame.mixer.init()
pygame.mixer.pre_init(44100, 16, 2, 4096)
explodeSound = pygame.mixer.Sound("bgm/explode.wav")
itemSound = pygame.mixer.Sound("bgm/item.wav")
lostSound = pygame.mixer.Sound("bgm/lost.wav")
rocketSound = pygame.mixer.Sound("bgm/rocket.wav")
shootSound = pygame.mixer.Sound("bgm/shoot.wav")
music = pygame.mixer.music.load("bgm/theme.mp3")
