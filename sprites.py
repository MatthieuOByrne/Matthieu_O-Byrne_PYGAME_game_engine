# Import necessary libraries
import pygame as pg
import time
from setting import *  # Import settings from a file called 'setting'
vec = pg.math.Vector2  # Alias for pygame's Vector2 class

# Function to handle collision with walls
def collide_with_walls(sprite, group, dir):
    if dir == 'x':
        # Check for collisions along the x-axis
        hits = pg.sprite.spritecollide(sprite, group, False)
        if hits:
            # Adjust position and velocity based on collision
            if hits[0].rect.centerx > sprite.rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.rect.width / 2
            if hits[0].rect.centerx < sprite.rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.rect.width / 2
            sprite.vel.x = 0
            sprite.rect.centerx = sprite.pos.x
    if dir == 'y':
        # Check for collisions along the y-axis
        hits = pg.sprite.spritecollide(sprite, group, False)
        if hits:
            # Adjust position and velocity based on collision
            if hits[0].rect.centery > sprite.rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.rect.height / 2
            if hits[0].rect.centery < sprite.rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.rect.height / 2
            sprite.vel.y = 0
            sprite.rect.centery = sprite.pos.y

# Player class definition
class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        # Define player attributes and initialize superclass
        # (pg.sprite.Sprite)
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILESIZE, TILESIZE))  # Create player surface
        self.image.fill(BLUE)  # Fill player surface with blue color
        self.game = game
        self.rect = self.image.get_rect()  # Get player rectangle
        self.x = x * TILESIZE  # Set player x position
        self.y = y * TILESIZE  # Set player y position
        self.moneyBag = 0  # Initialize money bag
        self.speed = PLAYER_SPEED  # Set player speed
        self.cooldownForSpeed = 0  # Initialize speed cooldown
        self.health = 3  # Set player health
        self.cooldown = 3  # Set general cooldown
        self.invincibility_cooldown = None  # Initialize invincibility cooldown

    # Method to handle player input
    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        # Adjust velocity based on pressed keys
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

    # Method to move the player
    def move(self, dx=0, dy=0):
        if not self.collide_with_walls(dx, dy):
            self.x += dx
            self.y += dy

    # Method to handle player collision with walls
    def collide_with_walls(self, dir):
        if dir == 'x':
            # Check for collision along the x-axis
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                # Adjust position and velocity based on collision
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0: 
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            # Check for collision along the y-axis
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                # Adjust position and velocity based on collision
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0: 
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y

    # Method to handle collision with a group of sprites
    def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            # Handle different types of collisions
            if str(hits[0].__class__.__name__) == "Coin":
                self.moneyBag += 1
            if str(hits[0].__class__.__name__) == "Powerup_Speed":
                self.cooldownForSpeed = 5           
            if str(hits[0].__class__.__name__) == "Mob2":
                if self.cooldown <= 0:
                    self.health -= 1
                    self.cooldown = 3

    # Update player attributes
    def update(self):
        if self.cooldown > 0:
            self.cooldown -= self.game.dt
        if self.cooldownForSpeed > 0:
            self.cooldown -= self.game.dt
            self.speed = FAST_SPEED
        elif self.cooldownForSpeed <= 0:
            self.speed = PLAYER_SPEED
            self.cooldown -= self.game.dt

        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')
        self.collide_with_group(self.game.powerup, True)
        self.collide_with_group(self.game.mobs, False)

# Wall class definition
class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        # Define wall attributes and initialize superclass
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILESIZE, TILESIZE))  # Create wall surface
        self.image.fill(BROWN)  # Fill wall surface with brown color
        self.game = game
        self.rect = self.image.get_rect()  # Get wall rectangle
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

# Coin class definition
class Coin(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        # Define coin attributes and initialize superclass
        self.groups = game.all_sprites, game.powerup
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILESIZE, TILESIZE))  # Create coin surface
        self.image.fill(YELLOW)  # Fill coin surface with yellow color
        self.game = game
        self.rect = self.image.get_rect()  # Get coin rectangle
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

# Powerup_Speed class definition
class Powerup_Speed(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        # Define powerup speed attributes and initialize superclass
        self.groups = game.all_sprites, game.powerup
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILESIZE, TILESIZE))  # Create powerup surface
        self.image.fill(GREEN)  # Fill powerup surface with green color
        self.game = game
        self.rect = self.image.get_rect()  # Get powerup rectangle
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

# Mob class definition
class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        # Define mob attributes and initialize superclass
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))  # Create mob surface
        self.image.fill(RED)  # Fill mob surface with red color
        self.rect = self.image.get_rect()  # Get mob rectangle
        self.x = x
        self.y = y
        self.vx, self.vy = 100, 100
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.speed = 1

    # Method to handle collision with walls for mob
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                self.vx *= -1
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                self.vy *= -1
                self.rect.y = self.y

    # Update mob position
    def update(self):
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        if self.rect.x < self.game.player.rect.x:
            self.vx = 100
        if self.rect.x > self.game.player.rect.x:
            self.vx = -100    
        if self.rect.y < self.game.player.rect.y:
            self.vy = 100
        if self.rect.y > self.game.player.rect.y:
            self.vy = -100
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')

# Mob2 class definition
class Mob2(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        # Define mob2 attributes and initialize superclass
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))  # Create mob2 surface
        self.image.fill(ORANGE)  # Fill mob2 surface with orange color
        self.rect = self.image.get_rect()  # Get mob2 rectangle
        self.pos = vec(x, y) * TILESIZE
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.chase_distance = 500
        self.speed = 150
        self.chasing = False
        self.hitpoints = 5

    # Method to sense player for mob2
    def sensor(self):
        if abs(self.rect.x - self.game.player.rect.x) < self.chase_distance and abs(self.rect.y - self.game.player.rect.y) < self.chase_distance:
            self.chasing = True
        else:
            self.chasing = False

    # Update mob2 attributes
    def update(self):
        if self.hitpoints < 1:
            print("mob2 should be dead")
            self.kill()
        self.sensor()
        # chases after the player
        if self.chasing:
            self.rot = (self.game.player.rect.center - self.pos).angle_to(vec(1, 0))
            self.rect.center = self.pos
            self.acc = vec(self.speed, 0).rotate(-self.rot)
            self.acc += self.vel * -1
            self.vel += self.acc * self.game.dt
            self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
            collide_with_walls(self, self.game.walls, 'x')
            collide_with_walls(self, self.game.walls, 'y')