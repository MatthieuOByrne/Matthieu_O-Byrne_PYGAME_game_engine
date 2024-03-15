WIDTH = 1024
HEIGHT = 768

TITLE = "My fun game"

TILESIZE = 32

# Tuples: a kind of list that doesn't change
BGCOLOR = (0, 0, 0)
GREEN = (0, 255, 0)
BROWN = (165, 42, 42)
YELLOW = (255, 250, 204)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
RED = (255, 0, 0)

FPS = 30


LIGHTGREY = (150, 150, 150)

# Player settings
PLAYER_SPEED = 300
FAST_SPEED = 600

import pygame as pg

from math import floor

class Cooldown():
    # sets all properties to zero when instantiated...
    def __init__(self, game, time):
        self.game = game
        self.current_time = 0
        self.event_time = 0
        self.cd = 0
        self.cooldown_time = time
        # ticking ensures the timer is counting...
    # must use ticking to count up or down
    def ticking(self):
        self.current_time = floor((pg.time.get_ticks())/1000)
        if self.cd > 0:
            self.countdown()
    # resets event time to zero - cooldown reset
    def get_countdown(self):
        return floor(self.cd)
    def check(self):
        if self.cooldown_time>self.current_time:
            return True
        else:
            return False

    def countdown(self):
        if self.cd > 0:
            self.cd = self.cd - self.game.dt
    def reset(self):
        self.event_time = floor((pg.time.get_ticks())/1000)
    # sets current time
    def get_current_time(self):
        self.current_time = floor((pg.time.get_ticks())/1000)