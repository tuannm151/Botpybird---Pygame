import pygame
from constants import BGM_VOLUME, SFX_VOLUME
pygame.mixer.init()


pygame.mixer.pre_init(44100, 16, 2, 4096)


def create_sound04(name, vol):
    fullname = "bgm/" + name     # path + name of the sound file
    sound = pygame.mixer.Sound(fullname)
    sound.set_volume(vol)
    return sound


explodeSound = create_sound04('explode.wav', SFX_VOLUME)
itemSound = create_sound04("item.wav", SFX_VOLUME)
lostSound = create_sound04("lost.wav", SFX_VOLUME)
rocketSound = create_sound04("rocket.wav", SFX_VOLUME)
shootSound = create_sound04("shoot.wav", SFX_VOLUME)
music = pygame.mixer.music.load("bgm/theme.mp3")
pygame.mixer.music.set_volume(BGM_VOLUME)
