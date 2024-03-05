# This file was created by Matthieu O'Byrne
# The code was inspired by Zelda and informed by Chris Bradfield
import pygame as pg
import time
from setting import *

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        #init super class
        pg.sprite.Sprite.__init__(self, self.groups)
        # create image for the player
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(BLUE)
        # allow him to access game properties
        self.game = game
        self.rect = self.image.get_rect()
        # set position
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.moneyBag = 0
        self.speed = PLAYER_SPEED
        self.cooldownForSpeed = None

    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx = -self.speed  
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = self.speed  
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vy = -self.speed  
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vy = self.speed
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071
            self.vy *= 0.7071
    def move(self, dx=0, dy=0):
        if not self.collide_with_walls(dx, dy):
            self.x += dx
            self.y += dy
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0: 
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0: 
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y
    # thank you Aayush
    def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == "Coin":
                self.moneyBag += 1
            if str(hits[0].__class__.__name__) == "Powerup_Speed":
                self.cooldownForSpeed = Cooldown(5000)
                self.cooldownForSpeed.start()
            if str(hits[0].__class__.__name__) == "Powerup_Normal":
                self.speed = PLAYER_SPEED
        
    # update the player

    def update(self):
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        # add collision later
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')
        self.collide_with_group(self.game.powerup, True)
        if self.cooldownForSpeed:
            self.cooldownForSpeed.update()
            print(self.cooldownForSpeed.check())
            if self.cooldownForSpeed.check() == True:
                self.speed = PLAYER_SPEED
            else:
                self.speed = FAST_SPEED
        # add colision later


# wall
class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        # makes the wall discoverable by player
        self.groups = game.all_sprites, game.walls
        # draw it
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(BROWN)
        self.game = game
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Coin(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.powerup
    
        # draw it
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.game = game
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
class Powerup_Speed(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.powerup
        # draw it
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.game = game
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
class Powerup_Normal(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.powerup
    
        # draw it
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(ORANGE)
        self.game = game
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Cooldown:
    def __init__(self, cooldown_time):
        self.cooldown_time = cooldown_time
        self.last_used_time = 0

    def start(self):
        self.last_used_time = 0

    def check(self):
        return self.last_used_time >= self.cooldown_time
   
    def reset(self):
        self.last_used_time = 0

    def update(self):
        self.last_used_time += 0.1