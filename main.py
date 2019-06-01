##!/usr/bin/env python

# Imports all functions from these libraries
import random
import pygame

# Looks at the file constants, and imports all variables there
from constants import *
from question import *

""" This is the main loop that runs the multiple choice test. """
class Main(object):

    """ Initialization method for Main object. When you instantiate Main,
        this code automatically runs. """
    def __init__(self):
        self.g = Globals()
        self.g.question_set = QuestionSet(QUESTION_PATH)
        self.loop()

    """ Main loop. Code in here runs repeatedly until something stops it. """
    def loop(self):

        i = 0
        while i < 3:
            print(self.g.question_set.questions[i])
            i += 1
            pass


""" This object stores global values and variables so they can be passed
    around between frames. """
class Globals(object):

    def __init__(self):
        self.window_width = WINDOW_WIDTH
        self.window_height = WINDOW_HEIGHT
        self.window_size = WINDOW_SIZE


# This is the place the program goes to when you run it with python. Right
# now, it just starts an instance of Main.
if __name__ == '__main__':
    Main()
