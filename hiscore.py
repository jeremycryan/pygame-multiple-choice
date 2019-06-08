##!/usr/bin/env python

from constants import *

class HiScore(object):

    def __init__(self, g):
        self.g = g
        self.num = 10
        self.reset()


    def push(self, name, score):
        for idx, item in enumerate(self.scores):
            if item[1] <= score:
                name_surf = self.g.hi_score_font.render(name, 1, HI_SCORE_FONT_COLOR)
                score_surf = self.g.hi_score_font.render(str(score), 1, HI_SCORE_FONT_COLOR)
                self.scores.insert(idx, (name, score, name_surf, score_surf))
                print("%s: %s pushed to position %s" % (name, score, idx))
                break
        self.scores = self.scores[:self.num]


    def reset(self):
        AAA = self.g.hi_score_font.render("Empty", 1, LIGHT_GRAY)
        zero = self.g.hi_score_font.render(str(0), 1, LIGHT_GRAY)
        self.scores = [("Empty", 0, AAA, zero)] * self.num


    def is_high_score(self, score):
        for idx, item in enumerate(self.scores):
            if item[1] <= score:
                return True
        return False


    def draw(self):
        yoff = HI_SCORE_Y
        c = int(FRAME_WIDTH/2)  #   Center x coordinate
        w = int(FRAME_WIDTH*HI_SCORE_WIDTH)  #   Width of high score array
        lm = int(c - w/2)       #   X coordinate of left margin
        rm = int(c + w/2)       #   X coordinate of right margin
        
        for item in self.scores:
            name, score, name_surf, score_surf = item
            self.g.screen.blit(name_surf, (lm, yoff))
            self.g.screen.blit(score_surf, (rm - score_surf.get_width(), yoff))
            yoff += HI_SCORE_SPACING
