##!/usr/bin/env python

import pygame
import time
from constants import *
from button import *

""" Object representing one frame of the quiz. This could be a title screen,
    a single question, etc. """
class Frame(object):

    def __init__(self, globals):
        self.g = globals


    """ Main method. Should return another Frame object, telling the program
        which frame to run next. """
    def main(self):
        pass


""" Frame to ask the user a question """
class QuestionFrame(Frame):

    def __init__(self, globals):
        Frame.__init__(self, globals)

    """ Returns a list of pygame surfaces corresponding to each line of the
        question as rendered fonts """
    def question_render(self, text):
        surfs = []
        positions = []
        words = text.split()
        cur_surf = pygame.Surface((1, 1))
        cur_surf_words = []

        #   Put the words in the correct locations to generate surfaces with
        #   typsetting, or something
        #   TODO clean up this code, it's a bit of a mess
        while len(words):
            cur_surf_words.append(words.pop(0))
            cur_surf = self.g.question_font.render(" ".join(cur_surf_words),
                                                    1,
                                                    QUESTION_FONT_COLOR)

            if cur_surf.get_width() > QUESTION_WRAP_WIDTH:
                words = [cur_surf_words.pop()] + words
                surfs += [self.g.question_font.render(" ".join(cur_surf_words),
                                                    1,
                                                    QUESTION_FONT_COLOR)]
                cur_surf = pygame.Surface((1, 1))
                cur_surf_words = []
                continue


        surfs += [self.g.question_font.render(" ".join(cur_surf_words),
                                            1,
                                            QUESTION_FONT_COLOR)]

        return surfs


    """ Draws the current question number, and total questions, on the
        screen. This also generates the text surfaces, so should only be run
        once per frame. """
    def draw_cur_num(self):
        num = self.g.current_question + 1
        total = len(self.g.question_set.questions)

        #   Create text surfaces
        cur_num_render = self.g.cur_num_font.render(str(num), 1,
                                                    CUR_NUM_FONT_COLOR)
        tot_num_render = self.g.tot_num_font.render("of " + str(total), 1,
                                                    TOT_NUM_FONT_COLOR)

        #   Draw them on the screen
        self.g.screen.blit(cur_num_render,
                           (int(897 - cur_num_render.get_width()/2),
                            (int(101 - cur_num_render.get_height()/2))))
        self.g.screen.blit(tot_num_render, (945, 98))
        
        

    """ Draws the text for the question on the screen """
    def draw_question(self, surfs):
        line_height = surfs[0].get_height()
        y_spacing = QUESTION_Y_SPACING
        height = line_height * len(surfs) + y_spacing * (len(surfs) - 1)

        y = QUESTION_Y_POS - int(height/2)
        for surf in surfs:
            x = int(FRAME_WIDTH/2 - surf.get_width()/2)
            self.g.screen.blit(surf, (x, y))
            y += line_height + y_spacing


    """ Runs the behavior of the frame """
    def main(self):
        question = self.g.question_set.questions[self.g.current_question]
        question_text = question.question
        question_surfs = self.question_render(question_text)
        answers = question.answers
        background = self.g.load_image("images/background.png")

        #   Create button objects and set them in the right place
        buttons = [AnswerButton(text, self.g) for text in answers]
        for idx, button in enumerate(buttons):
            button.set_position_from_number(idx)

        submit_button = SubmitButton("SUBMIT", self.g)
        submit_button.set_position()
        buttons += [submit_button]

        then = time.time()
        self.g.screen.blit(background, (0, 0))
        self.draw_cur_num()
                           
        while True:

            #   Determine how long it has been since last loop
            now = time.time()
            dt = now - then
            then = now

            #   Do global updates and find mouse position
            events, dt = self.g.update_globals(dt)
            mpos = self.g.mouse_pos()

            #   Update event flags
            mouse_button_up = False
            one_button_selected = False
            for event in events:
                if event.type == pygame.MOUSEBUTTONUP:
                    mouse_button_up = True

            #   Draw the background
            self.g.screen.blit(background, (240, 240), (240, 240, 800, 480))

            #   Draw the question
            self.draw_question(question_surfs)

            #   Update and draw buttons
            for button in buttons:
                button.update(dt)
                button.check_hover(mpos)
                if mouse_button_up and button.hovered:
                    for b in buttons:
                        if button is not b and button is not submit_button:
                            b.selected = False
                    button.click()
                if button.selected:
                    one_button_selected = True
                button.draw(one_button_selected)

            if submit_button.selected:
                break

            #   Update screen
            self.g.display_screen()

        end_start = time.time()
        while True:

            #   Don't spend too long in the end phase
            if time.time() - end_start > 0.6:
                return

            #   Determine how long it has been since last loop
            now = time.time()
            dt = now - then
            then = now

            #   Do global updates and find mouse position
            events, dt = self.g.update_globals(dt)
            mpos = self.g.mouse_pos()

            #   Draw the background
            self.g.screen.blit(background, (240, 240), (240, 240, 800, 480))

            #   Draw the question
            self.draw_question(question_surfs)

            #   Update and draw buttons
            for button in buttons:
                button.update(dt)
                button.hovered = False
                if button.selected and button is not submit_button:
                    one_button_selected = True
                    button.move_to_center()
                else:
                    button.disappearing = True
                if time.time() - end_start > 0.3:
                    button.disappearing = True
                button.draw(one_button_selected)

            #   Update screen
            self.g.display_screen()
