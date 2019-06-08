##!/usr/bin/env python

# Imports all functions from these libraries
import random
import pygame
import sys

# Looks at the file constants, and imports all variables there
from constants import *
from question import *
from frame import *
from hiscore import *

""" This is the main loop that runs the multiple choice test. """
class Main(object):

    """ Initialization method for Main object. When you instantiate Main,
        this code automatically runs. """
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.g = Globals()
        while True:
            self.loop()

    """ Main loop. Code in here runs repeatedly until something stops it. """
    def loop(self):

        self.g.screen_cap = None
        OpenFrame(self.g).main()
        while self.g.current_question < len(self.g.question_set.questions):
            new_frame = QuestionFrame(self.g)
            self.g.screen_cap = new_frame.main()
            self.g.current_question += 1
        new_frame = ScoreFrame(self.g)
        self.g.screen_cap = new_frame.main()
        new_frame = HiScoreFrame(self.g)
        self.g.screen_cap = new_frame.main()

        high_scores = self.g.hi_scores
        self.g = Globals()
        self.g.hi_scores = high_scores
        self.g.hi_scores.g = self.g


""" This object stores global values and variables so they can be passed
    around between frames. """
class Globals(object):

    def __init__(self):
        self.window_width = WINDOW_WIDTH
        self.window_height = WINDOW_HEIGHT
        self.window_size = WINDOW_SIZE

        self.current_question = 0
        self.correct_answers = 0
        self.question_set = QuestionSet(QUESTION_PATH)

        self.screen_cap = None

        self.images = {}

        self.question_font = pygame.font.Font("fonts/" + QUESTION_FONT, QUESTION_FONT_SIZE)
        self.answer_font = pygame.font.Font("fonts/" + ANSWER_FONT, ANSWER_FONT_SIZE)
        self.submit_font = pygame.font.Font("fonts/" + SUBMIT_FONT, SUBMIT_FONT_SIZE)
        self.cur_num_font = pygame.font.Font("fonts/" + CUR_NUM_FONT, CUR_NUM_FONT_SIZE)
        self.tot_num_font = pygame.font.Font("fonts/" + TOT_NUM_FONT, TOT_NUM_FONT_SIZE)
        self.big_score_font = pygame.font.Font("fonts/" + BIG_SCORE_FONT, BIG_SCORE_FONT_SIZE)
        self.small_score_font = pygame.font.Font("fonts/" + SMALL_SCORE_FONT, SMALL_SCORE_FONT_SIZE)
        self.continue_font = pygame.font.Font("fonts/" + CONTINUE_FONT, CONTINUE_FONT_SIZE)
        self.hi_score_font = pygame.font.Font("fonts/" + HI_SCORE_FONT, HI_SCORE_FONT_SIZE)

        self.hi_scores = HiScore(self)

        self.clock = pygame.time.Clock()

        self.screen = pygame.Surface(FRAME_SIZE)
        self.screen_commit = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption(WINDOW_NAME)

    """ Loads an image from the path. If it's already been loaded before,
        instead just fetch it from the stored dictionary. """
    def load_image(self, path):

        #   If it exists in preloaded dictionary, fetch it
        if path in self.images:
            return self.images[path]

        #   Otherwise, load it from the file
        return pygame.image.load(path)

    """ Checks events and processes time step for each frame """
    def update_globals(self, dt):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.close_game()
        return events, dt

    """ Fills the screen with black """
    def clear_screen(self):
        self.screen.fill(BLACK)

    """ Scales the screen to the actual window and displays it """
    def display_screen(self):
        screen = self.screen
        if self.window_width != FRAME_WIDTH or self.window_height != FRAME_HEIGHT:
            screen = pygame.transform.scale(self.screen, WINDOW_SIZE)
        self.screen_commit.blit(screen, (0, 0))
        pygame.display.flip()
        self.clock.tick(50)

    """ Returns the position of the mouse on the screen """
    def mouse_pos(self):
        #   TODO account for screen scaling
        return pygame.mouse.get_pos()

    """ Closes the window """
    def close_game(self):
        pygame.quit()
        sys.exit()


# This is the place the program goes to when you run it with python. Right
# now, it just starts an instance of Main.
if __name__ == '__main__':
    Main()
