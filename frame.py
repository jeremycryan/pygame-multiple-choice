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

class OpenFrame(Frame):

    def main(self):
        bkg = self.g.load_image("images/background.png")
        black = pygame.Surface(FRAME_SIZE)
        black.fill(BLACK)
        black_alpha = 255
        black.set_alpha(black_alpha)

        then = time.time() - 0.001
        while True:
            now = time.time()
            dt = now - then
            then = now

            self.g.update_globals(dt)

            black_alpha = max(0, black_alpha - 400 * dt)
            black.set_alpha(black_alpha)

            self.g.screen.blit(bkg, (0, 0))
            self.g.screen.blit(black, (0, 0))

            self.g.display_screen()

            if black_alpha == 0: return black

            

class HiScoreFrame(Frame):

    def main(self):
        black = pygame.Surface(FRAME_SIZE)
        black.fill((0, 0, 0))
        black_alpha = 255
        black.set_alpha(black_alpha)
        background = self.g.load_image("images/hi_score_background.png")
        title = self.g.question_font.render("High Scores", 1, QUESTION_FONT_COLOR)
        then = time.time() - 0.001
        buttons = [ContinueButton("START QUIZ", self.g)]
        buttons[0].visible = True
        buttons[0].pos = (int(FRAME_WIDTH/2), FRAME_HEIGHT - 100)
        buttons[0].target_pos = buttons[0].pos

        f = open("player_name.txt", 'r')
        playername = f.read() + " "*15
        f.close()
        self.g.hi_scores.push(playername[:15], self.g.correct_answers)
        
        while True:

            now = time.time()
            dt = now - then
            then = now

            events, dt = self.g.update_globals(dt)
            mpos = pygame.mouse.get_pos()

            black_alpha = max(0, black_alpha - (350 * dt))
            black.set_alpha(black_alpha)
            
            self.g.screen.blit(background, (0, 0))
            self.g.screen.blit(title, (int(FRAME_WIDTH/2 - title.get_width()/2), 115))

            for button in buttons:
                button.update(dt)
                button.check_hover(mpos)
                if button.hovered:
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONUP:
                            button.click()
                            button.disappearing = True
                button.draw()

            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        buttons[0].click()

            if buttons[0].selected:
                break

            self.g.hi_scores.draw()
            
            self.g.screen.blit(black, (0, 0))
            self.g.display_screen()

        while True:
            now = time.time()
            dt = now - then
            then = now

            events, dt = self.g.update_globals(dt)
            mpos = pygame.mouse.get_pos()

            black_alpha = min(255, black_alpha + (350 * dt))
            black.set_alpha(black_alpha)
            
            self.g.screen.blit(background, (0, 0))
            self.g.hi_scores.draw()
            self.g.screen.blit(title, (int(FRAME_WIDTH/2 - title.get_width()/2), 115))

            for button in buttons:
                button.update(dt)
                button.draw()
            
            self.g.screen.blit(black, (0, 0))
            self.g.display_screen()
            if black_alpha == 255:
                return black


class ScoreFrame(Frame):

    def __init__(self, globals):
        Frame.__init__(self, globals)

    def main(self):

        black = pygame.Surface(FRAME_SIZE)
        black.fill(BLACK)
        black_alpha = 0
        black.set_alpha(black_alpha)

        window = self.g.load_image("images/score_window.png")

        total_score_string = self.g.question_font.render("Total score", 1, QUESTION_FONT_COLOR)
        big_score = self.g.big_score_font.render(str(self.g.correct_answers), 1,
                                                     BIG_SCORE_FONT_COLOR)
        small_score = self.g.small_score_font.render("/ "+str(len(self.g.question_set.questions)), 1,
                                                     SMALL_SCORE_FONT_COLOR)


        score_width = big_score.get_width() + small_score.get_width() + SCORE_SPACING

        yoff = 110
        window.blit(big_score,
                (int(window.get_width()/2 - score_width/2), yoff))
        window.blit(small_score,
                (int(window.get_width()/2 + score_width/2 - small_score.get_width()),
                 int(yoff + big_score.get_height() * SMALL_SCORE_OFFSET)))
        window.blit(total_score_string,
                    (int(window.get_width()/2 - total_score_string.get_width()/2),
                     70))

        
        
        then = time.time() - 0.001

        buttons = [ContinueButton("CONTINUE", self.g)]

        window_y_target = int(FRAME_HEIGHT/2 - window.get_height()/2)
        window_y_off = 280
        window_y = -window.get_height() - window_y_off

        while True:

            #   Determine how long it has been since last loop
            now = time.time()
            dt = now - then
            then = now

            #   Do global updates and find mouse position
            events, dt = self.g.update_globals(dt)
            mpos = self.g.mouse_pos()

            dy = window_y_target - window_y
            p = 8
            if (dy * dt * p) > dy:
                window_y = window_y_target
            if (dy * dt * p > dt * 1200):
                window_y += dt * 2500
            else:
                window_y += dy * dt * p
            window_y_off = max(0, window_y_off - 500 * dt)

            do_break = False
            mouse_button_up = False
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        do_break = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    mouse_button_up = True

            black_alpha = min(150, black_alpha + 400 * dt)
            black.set_alpha(black_alpha)

            self.g.screen.blit(self.g.screen_cap, (0, 0))
            self.g.screen.blit(black, (0, 0))
            self.g.screen.blit(window,
                               (int(FRAME_WIDTH/2 - window.get_width()/2),
                                int(window_y + window_y_off)))
            
            for button in buttons:
                button.pos = int(FRAME_WIDTH/2), int(window_y + window_y_off + window.get_height())
                button.target_pos = button.pos
                button.update(dt)
                button.check_hover(mpos)
                if button.hovered and mouse_button_up:
                    do_break = True
                button.draw()

                
            self.g.display_screen()
            
            if do_break: break

        while True:

            #   Determine how long it has been since last loop
            now = time.time()
            dt = now - then
            then = now

            #   Do global updates and find mouse position
            events, dt = self.g.update_globals(dt)
            mpos = self.g.mouse_pos()

            dy = max(100, window_y_target - window_y)
            p = 8
            window_y = max(-window.get_height() - 100, window_y - (dy * dt * p))
            window_y_off = 0

            black_alpha = min(255, black_alpha + 200 * dt)
            black.set_alpha(black_alpha)

            self.g.screen.blit(self.g.screen_cap, (0, 0))
            self.g.screen.blit(black, (0, 0))
            self.g.screen.blit(window,
                               (int(FRAME_WIDTH/2 - window.get_width()/2),
                                int(window_y + window_y_off)))

            for button in buttons:
                button.pos = int(FRAME_WIDTH/2), int(window_y + window_y_off + window.get_height())
                button.target_pos = button.pos
                button.update(dt)
                button.check_hover(mpos)
                if button.hovered and mouse_button_up:
                    do_break = True
                button.draw()

            self.g.display_screen()
            if window_y <= -window.get_height() - 100:
                return black.copy()
            

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
        self.draw_question(question_surfs)
                           
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
            key_right = False
            key_left = False
            key_up = False
            key_down = False
            key_enter = False
            next_key = None
            for event in events:
                if event.type == pygame.MOUSEBUTTONUP:
                    mouse_button_up = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP: key_up = True
                    if event.key == pygame.K_DOWN: key_down = True
                    if event.key == pygame.K_LEFT: key_left = True
                    if event.key == pygame.K_RIGHT: key_right = True
                    if event.key == pygame.K_RETURN: key_enter = True

            #   Interpret keypresses
            if not any([button.selected for button in buttons]):
                if any([key_up, key_down, key_left, key_right]):
                    buttons[0].click()

            else:
                sel_idx = None
                for idx, b in enumerate(buttons):
                    if b.selected:
                        sel_idx = idx
                
                next_idx = sel_idx
                if key_up and sel_idx > 1: next_idx -= 2
                elif key_down and sel_idx < 2: next_idx += 2
                elif key_left and sel_idx%2: next_idx -= 1
                elif key_right and not sel_idx%2: next_idx += 1

                if not buttons[next_idx].selected:
                    next_key = buttons[next_idx]
                

            #   Draw the background
            self.g.screen.blit(background, (240, 290), (240, 290, 800, 480))

            #   Draw the question
            #self.draw_question(question_surfs)

            #   Update and draw buttons
            for button in buttons:
                button.update(dt)
                button.check_hover(mpos)
                if (mouse_button_up and button.hovered) or button is next_key:
                    for b in buttons:
                        if button is not b and button is not submit_button:
                            b.selected = False
                    button.click()
                if button.selected:
                    one_button_selected = True
                button.draw(one_button_selected)

            if submit_button.selected or (key_enter and one_button_selected):
                break

            #   Update screen
            self.g.display_screen()

        correct = False
        for b in buttons:
            if b.selected:
                if b.text == question.correct_answer:
                    correct = True

        if correct:
            self.g.correct_answers += 1
        
        end_start = time.time()            
        
        while True:

            #   Don't spend too long in the end phase
            if time.time() - end_start > 0.6:
                return self.g.screen.copy()

            #   Determine how long it has been since last loop
            now = time.time()
            dt = now - then
            then = now

            #   Do global updates and find mouse position
            events, dt = self.g.update_globals(dt)
            mpos = self.g.mouse_pos()

            #   Draw the background
            self.g.screen.blit(background, (240, 290), (240, 290, 800, 480))

            #   Draw the question
            #self.draw_question(question_surfs)

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
