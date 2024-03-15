#This game was created by: Matthieu O'Byrne


'''


start and restart screen

moving enemies

projectile

'''
# import libraries and modules
import pygame as pg
from setting import *
from sprites import *
from random import randint
import sys
from os import path
vec = pg.math.Vector2

# Define game class...
class Game:
    # Define a special method to init the properties of said class...
    def __init__(self):
        # init pygame
        pg.init()
        # set size of screen and be the screen
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        # setting game clock 
        self.clock = pg.time.Clock()
        self.load_data()
    def load_data(self):
        game_folder = path.dirname(__file__)
        self.map_data = []
        # 'r'     open for reading (default)
        # 'w'     open for writing, truncating the file first
        # 'x'     open for exclusive creation, failing if the file already exists
        # 'a'     open for writing, appending to the end of the file if it exists
        # 'b'     binary mode
        # 't'     text mode (default)
        # '+'     open a disk file for updating (reading and writing)
        # 'U'     universal newlines mode (deprecated)
        # below opens file for reading in text mode
        # with 
        '''
        The with statement is a context manager in Python. 
        It is used to ensure that a resource is properly closed or released 
        after it is used. This can help to prevent errors and leaks.
        '''
        with open(path.join(game_folder, 'map.txt'), 'rt') as f:
            for line in f:
                self.map_data.append(line)
    # Create run method which runs the whole GAME
    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.powerup = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                if tile == 'c':
                    Coin(self, col, row)
                if tile == 'p':
                    self.player = Player(self, col, row)
                if tile == 's':
                    Powerup_Speed(self, col, row)
                if tile == 'm':
                    Mob2(self,col,row)
                


    # make the player update every frame
    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()
    # actually end the python program when game is closed
    def quit(self):
         pg.quit()
         sys.exit()
    # update all positions
    def show_death_screen(self):
        self.screen.fill(BGCOLOR)
        self.draw_text(self.screen, "You died :( press any key to start", 24, ORANGE, WIDTH/2, HEIGHT/2)
        pg.display.flip()
        self.wait_for_key_or_click()
        self.player.health = 3
    def update(self):
        self.all_sprites.update()
        print(self.player.health)
        if self.player.health <= 0:
            self.show_death_screen()
            self.playing = False
    # make the grid for the game
    # def draw_grid(self):
    #      for x in range(0, WIDTH, TILESIZE):
    #           pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
    #      for y in range(0, HEIGHT, TILESIZE):
    #           pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))
    # draw screen
    def draw(self):
            self.screen.fill(BGCOLOR)
            # self.draw_grid()
            self.all_sprites.draw(self.screen)
            pg.display.flip()
    #  move it using keycodes
    def draw_text(self, surface, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x,y)
        surface.blit(text_surface, text_rect)
    def events(self):
         for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
#             if event.type == pg.KEYDOWN:
#                 if event.key == pg.K_LEFT or event.key == pg.K_a:
#                     self.player1.move(dx=-1)
#             if event.type == pg.KEYDOWN:
#                 if event.key == pg.K_UP or event.key == pg.K_w:
#                     self.player1.move(dy=-1)
#             if event.type == pg.KEYDOWN:
#                 if event.key == pg.K_RIGHT or event.key == pg.K_d:
#                     self.player1.move(dx=1)
#             if event.type == pg.KEYDOWN:
#                 if event.key == pg.K_DOWN or event.key == pg.K_s:
#                     self.player1.move(dy=1)
    

    def show_start_screen(self):
        self.screen.fill(BGCOLOR)
        self.draw_text(self.screen,"Press any key to start", 70, ORANGE, WIDTH/2-300, 100)
        pg.display.flip()
        self.wait_for_key_or_click()    
    def wait_for_key_or_click(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYUP:
                    waiting = False
                if event.type == pg.MOUSEBUTTONUP:
                    waiting = False
# # Instantiate the game... 
g = Game()
# use game method run to run
# g.show_start_screen()
g.show_start_screen()
while True:
    # actually run the game
    g.new()
    g.run()
    # g.show_go_screen()
