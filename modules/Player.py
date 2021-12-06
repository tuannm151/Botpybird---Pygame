import pygame
from sprites import IDLE_IMGS, UP_IMGS, SHOOT_IMGS, BOOST_IMGS, DEAD_IMG, CRAZY_IMGS
from constants import PLAYER_VEL, PLAYER_HEALTH, PROJECTILE_DAMAGE


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

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.isBoosted = False
        self.isCrazy = False
        self.isLost = False
        self.isWin = False
        self.isDamaged = False
        self.up_pressed = False
        self.down_pressed = False
        self.isFlapUp = False
        self.isShooting = False

        self.health = PLAYER_HEALTH
        self.target_health = PLAYER_HEALTH
        self.max_health = PLAYER_HEALTH
        self.health_bar_length = 300
        self.health_ratio = self.max_health / self.health_bar_length
        self.health_change_speed = 1

    def hit(self):
        self.isDamaged = True
        if(not self.isBoosted):
            self.target_health -= PROJECTILE_DAMAGE
            if(self.target_health <= 0):
                self.target_health = 0
                self.isLost = True

    def get_health(self, amount):
        if(self.target_health < self.max_health):
            self.target_health += amount
        if(self.target_health >= self.max_health):
            self.target_health = self.max_health

    def update(self):
        if(self.isLost):
            self.image = DEAD_IMG
            return
        if(self.up_pressed and not self.down_pressed):
            self.moveUp()
        if(not self.up_pressed and not self.isShooting and not self.isBoosted and not self.isCrazy):
            self.sprites = IDLE_IMGS
        if(not self.up_pressed and self.down_pressed):
            self.moveDown()

        if(self.isCrazy):
            self.sprites = CRAZY_IMGS

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

        if(self.isDamaged):
            self.image = self.changeColor(self.image)
            self.isDamaged = False

    def changeColor(self, image):
        color = pygame.Color(0)
        color.hsla = (0, 100, 50, 6)
        colouredImage = pygame.Surface(image.get_size())
        colouredImage.fill(color)

        finalImage = image.copy()
        finalImage.blit(colouredImage, (0, 0), special_flags=pygame.BLEND_MULT)
        return finalImage

    # def showHealthBar(self, win):
    #     pygame.draw.rect(win, (255, 0, 0),
    #                      (10, 10, self.health / self.health_ratio, 25))
    #     pygame.draw.rect(win, (255, 255, 255),
    #                      (10, 10, self.health_bar_length, 25), 4)

    def healthTransition(self, win):
        health_bar_width = self.health / self.health_ratio
        transition_width = 0
        transition_color = (255, 0, 0)

        if self.health < self.target_health:
            self.health += self.health_change_speed
            transition_width = abs(
                (self.target_health - self.health)/self.health_ratio)
            transition_color = (0, 255, 0)

        if self.health > self.target_health:
            health_bar_width = self.target_health / self.health_ratio
            self.health -= self.health_change_speed
            transition_width = abs(
                (self.target_health - self.health))/self.health_ratio
            transition_color = (255, 255, 0)

        health_bar_rect = pygame.Rect(
            10, 10, health_bar_width, 25)
        transition_bar_rect = pygame.Rect(
            health_bar_rect.right, 10, transition_width, 25)

        pygame.draw.rect(win, (255, 0, 0), health_bar_rect)
        pygame.draw.rect(win, transition_color, transition_bar_rect)
        pygame.draw.rect(win, (255, 255, 255),
                         (10, 10, self.health_bar_length, 25), 4)

    def shooting(self):
        if(not self.isBoosted):
            self.current_sprite = 0
            self.isShooting = True
            self.sprites = SHOOT_IMGS
            self.animationsTime = 1

    def render(self, win):
        self.healthTransition(win)
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

    def collide(self, obj):
        obj_mask = obj.get_mask()
        mask = pygame.mask.from_surface(self.image)
        offset = (self.rect[0] - obj.rect[0], self.rect[1] - obj.rect[1])
        return mask.overlap(obj_mask, offset)

    def getY(self):
        return self.y
