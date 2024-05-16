#This game was created by: Matthieu O'Byrne
'''

start and restart screen

moving enemies

projectile


Beta: Add a boss fight
'''
# Import necessary libraries and modules
import pygame as pg
from setting import *  # Import settings for the game (constants)
from sprites import *  # Import game sprites classes
from random import randint
import sys
from os import path
vec = pg.math.Vector2  # Vector class for 2D vectors
import time

LEVEL1 = "level1.txt"
LEVEL2 = "level2.txt"
LEVEL3 = "level3.txt"
NUMLEVELS = 3
# Define game class...
class Game:
    # Define a special method to initialize the properties of the class...
    def __init__(self):
        # Initialize Pygame
        pg.init()
        # Set size of screen and set the screen
        self.screen = pg.display.set_mode((WIDTH, HEIGHT)) 
        pg.display.set_caption(TITLE)
        # Setting game clock
        self.clock = pg.time.Clock()
        # Load game data
        self.load_data()
        self.lvlNum = 1
        self.storm= None
        # Load heart image for display

    # Load game data from external files
    def load_data(self):
        self.game_folder = path.dirname(__file__)
        self.map_data = []
        self.currLvl = LEVEL1
        with open(path.join(self.game_folder, LEVEL1), 'rt') as f:
            for line in f:
                self.map_data.append(line)

    def change_level(self,lvl):
        self.currLvl = lvl
        for s in self.all_sprites:
            s.kill()
        self.player.moneybag = 0
        self.map_data = []
        with open(path.join(self.game_folder, lvl), 'rt') as f:
            for line in f:
                
                self.map_data.append(line)
        for row, tiles in enumerate(self.map_data):
            
            for col, tile in enumerate(tiles):
                
                if tile == '1':
                    Wall(self, col, row)
                if tile == 'c':
                    HealthBar(self, col, row)
                if tile == 'p':
                    self.player = Player(self, col, row)
                if tile == 's':
                    Powerup_Speed(self, col, row)
                if tile == 'm':
                    Mob2(self,col,row)
                if tile == 'T':
                    self.storm = TransparentCircleOverSquare(self, col, row)
                if tile == 'N':
                    self.portal = Portal(self,col,row)


    # Create new game instance
    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.powerup = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.players = pg.sprite.Group()
        self.portals = pg.sprite.Group()
        # Iterate through map data to create game elements based on characters in the map
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                if tile == 'p':
                    self.player = Player(self, col, row)
                if tile == 'c':
                    HealthBar(self, col, row)
                if tile == 's':
                    Powerup_Speed(self, col, row)
                if tile == 'm':
                    Mob2(self,col,row)
                if tile == 'T':
                    self.storm = TransparentCircleOverSquare(self, col, row)
                if tile == 'N':
                    self.portal = Portal(self,col,row)

    # Run the game
    def run(self):
        self.playing = True
        self.draw_text(self.screen, str("self.cooldown.current_time"), 24, WHITE, WIDTH/2 - 32, 2)
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    # Quit the game
    def quit(self):
        pg.quit()
        sys.exit()


    # Show death screen
    def show_death_screen(self):
        self.screen.fill(BGCOLOR)
        self.draw_text(self.screen, "You died :( press any key to start", 24, ORANGE, WIDTH/2, HEIGHT/2)
        pg.display.flip()
        time.sleep(2.5)
        self.wait_for_key_or_click()
        self.player.health = 3

    # Update all positions
    def update(self):
        self.all_sprites.update()
        if self.portal:
            hits = pg.sprite.spritecollide(self.portal, self.players, False)
            if hits:
                if self.currLvl == LEVEL1:
                    self.change_level(LEVEL2)
                elif self.currLvl == LEVEL2:
                    self.change_level(LEVEL3)
                elif self.currLvl == LEVEL3:
                    self.show_success_screen()
                    self.playing = False
        # print(self.player.health)
        if self.player.health <= 0:
            self.show_death_screen()
            self.playing = False
        # self.screen.blit(self.image_surface, (50, 50))
        keys = pg.key.get_pressed()
        if keys[pg.K_r]:
            self.show_start_screen()
        if self.currLvl == LEVEL1 and self.player.y > 768:
            self.change_level(LEVEL2)
        if self.storm:
            if self.currLvl == LEVEL1:
                if self.storm.radius <= WIDTH/2.95:
                    self.show_death_screen()
                    self.playing = False
            if self.currLvl == LEVEL2:
                if self.storm.radius <= WIDTH/2.75:
                    self.show_death_screen()
                    self.playing = False
            if self.currLvl == LEVEL3:
                if self.storm.radius <= WIDTH/3.2:
                    self.show_death_screen()
                    self.playing = False
    # Draw screen
    def draw(self):
        self.screen.fill(BGCOLOR)
        self.all_sprites.draw(self.screen)
        pg.display.flip()

    # Draw text on the screen
    def draw_text(self, surface, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x, y)
        surface.blit(text_surface, text_rect)

    # Handle events such as quitting the game
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYUP:
                if event.key == pg.K_ESCAPE:
                    self.quit()

    # Show start screen
    def show_start_screen(self):
        self.screen.fill(BGCOLOR)
        self.draw_text(self.screen, "Press any key to start!", 60, WHITE, WIDTH/2-300, 100)
        pg.display.flip()
        time.sleep(2.5)
        self.wait_for_key_or_click()

    # Show success screen
    def show_success_screen(self):
        self.screen.fill(BGCOLOR)
        self.draw_text(self.screen, "You won!!", 120, ORANGE, WIDTH/2-300, 100)
        pg.display.flip()
        time.sleep(2.5)
        self.wait_for_key_or_click()

    # Wait for key press or mouse click
    def wait_for_key_or_click(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYUP or event.type == pg.MOUSEBUTTONUP:
                    waiting = False

# Instantiate the game...
g = Game()
# Show start screen
g.show_start_screen()
while True:
    # Run the game
    g.new()
    g.run()
