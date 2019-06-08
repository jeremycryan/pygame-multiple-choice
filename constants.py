##!/usr/bin/env python

#   This file stores values that stay the same over the course of the program.
#   Variables that are constant are in all caps.

BLACK = (0, 0, 0)                           #   Use constants for colors
WHITE = (255, 255, 255)
GREEN = (50, 180, 52)
GRAY = (95, 115, 127)
LIGHT_GRAY = (120, 140, 145)

WINDOW_NAME = "Multiple Choice Test"
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT) #   Size of the window that opens

FRAME_WIDTH = 1280
FRAME_HEIGHT = 720
FRAME_SIZE = (FRAME_WIDTH, FRAME_HEIGHT)    #   Size of the virtual frame, which
                                            #   is then scaled to fit window


QUESTION_PATH = "questions.txt"             #   Path to text file with questions


QUESTION_FONT = "Montserrat-Medium.otf"     #   Text files to use when
QUESTION_FONT_SIZE = 40                     #   displaying questions and answers
QUESTION_FONT_COLOR = BLACK
QUESTION_WRAP_WIDTH = int(FRAME_WIDTH * 0.65)#   How wide the question gets (px)
                                            #   before breaking into multiple
                                            #   lines
QUESTION_Y_SPACING = 0
QUESTION_Y_POS = int(FRAME_HEIGHT * 0.3)

ANSWER_FONT = "Montserrat-Bold.otf"
ANSWER_FONT_SIZE = 32
ANSWER_FONT_COLOR = GREEN
ANSWER_FONT_COLOR_SELECT = WHITE

SUBMIT_FONT = "Montserrat-Bold.otf"
SUBMIT_FONT_SIZE = 25
SUBMIT_FONT_COLOR = WHITE

CUR_NUM_FONT = "Montserrat-Bold.otf"
CUR_NUM_FONT_SIZE = 30
CUR_NUM_FONT_COLOR = WHITE

TOT_NUM_FONT = "Montserrat-Medium.otf"
TOT_NUM_FONT_SIZE = 22
TOT_NUM_FONT_COLOR = GRAY

BIG_SCORE_FONT = "Montserrat-Medium.otf"
BIG_SCORE_FONT_SIZE = 120
BIG_SCORE_FONT_COLOR = BLACK

SMALL_SCORE_FONT = "Montserrat-Medium.otf"
SMALL_SCORE_FONT_SIZE = 40
SMALL_SCORE_FONT_COLOR = GRAY

CONTINUE_FONT = "Montserrat-Bold.otf"
CONTINUE_FONT_SIZE = 30
CONTINUE_FONT_COLOR = WHITE

HI_SCORE_FONT = "Montserrat-Medium.otf"
HI_SCORE_FONT_SIZE = 25
HI_SCORE_FONT_COLOR = BLACK

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"     #   This is important

RANDOMIZE_ANSWER_ORDER = True               #   Choose whether answers appear
                                            #   in different order each run
RANDOMIZE_QUESTION_ORDER = False            #   Choose whether questions appear
                                            #   in different order each run

BUTTON_BORDER = 0
BBORD_SLOP = 8
BUTTON_Y_OFFSET = -72
SUBMIT_BUTTON_Y_OFFSET = -36

SCORE_SPACING = 8
SMALL_SCORE_OFFSET = 0.6

HI_SCORE_SPACING = 32
HI_SCORE_WIDTH = 0.22
HI_SCORE_Y = 215
