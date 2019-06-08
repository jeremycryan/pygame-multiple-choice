##!/usr/bin/env python

import pygame
from constants import *

class AnswerButton(object):

    """ Initialize method for AnswerButton """
    def __init__(self, text, globals):
        self.g = globals
        self.text = text

        #   Load image files for button in different combinations of being
        #   currently selected and being hovered by the mouse.
        self.surf = self.g.load_image("images/unselected_button.png")
        self.hover_surf = self.g.load_image("images/unselected_button_hover.png")
        self.sel_surf = self.g.load_image("images/selected_button.png")
        self.hover_sel_surf = self.g.load_image("images/selected_button_hover.png")

        #   Set a position to render and save width and height. The position is
        #   defined as the location of the center of the button, in
        #   pixels from the origin.
        self.pos = (0, 0)
        self.target_pos = self.pos
        self.w = self.surf.get_width()
        self.h = self.surf.get_height()

        #   Booleans for being hovered or selected
        self.hovered = False
        self.selected = False
        self.scale = 1.0
        self.target_scale = 1.0
        self.scale_p = 8
        self.visible = False
        self.disappearing = False

        #   Time since creation
        self.time = 0
        self.appear_time = 99999999 #   When option should appear

        self.text_render = self.g.answer_font.render(text,
                                                    1,
                                                    ANSWER_FONT_COLOR)

        self.text_render_sel = self.g.answer_font.render(text,
                                                    1,
                                                    ANSWER_FONT_COLOR_SELECT)

    """ Draws the button onto the screen attribute of self.g """
    def draw(self, obs = False):

        if not self.visible: return

        #   Determine which surface to draw based on state of button
        surf = self.surf
        if self.hovered and self.selected:
            surf = self.hover_sel_surf
        if self.hovered and not self.selected:
            surf = self.hover_surf
        if not self.hovered and self.selected:
            surf = self.sel_surf

        #   Draw the text onto the button
        text_surf = self.text_render
        if self.selected:
            text_surf = self.text_render_sel
        surf.blit(text_surf,
            (int(self.w/2 - text_surf.get_width()/2),
            int(self.h/2 - text_surf.get_height()/2)))

        #   Draw that surface on the screen
        surf = pygame.transform.scale(surf,
            (int(surf.get_width() * self.scale),
            int(surf.get_height() * self.scale)))

        self.g.screen.blit(surf,
            (self.pos[0] - int(surf.get_width()/2),
            self.pos[1] - int(surf.get_height()/2)))

    """ Determines the color of the font based on whether button is selected """
    def answer_font_color(self):
        if self.selected:
            return ANSWER_FONT_COLOR_SELECT
        return ANSWER_FONT_COLOR

    """ Takes in the current mouse position and determines whether that
        lies within the bounds of the button; then, updates self.hovered
        accordingly. """
    #TODO account for screen scaling with mouse position
    def check_hover(self, mpos):

        if not self.visible:
            return False

        mx = mpos[0]
        my = mpos[1]
        x = self.pos[0]
        y = self.pos[1]

        #   Don't check for hovering in the very early life of button
        if self.time < 0.8:
            return

        #   Not hovered if x is outside button bounds
        if mx < x - self.w*self.scale/2 + BBORD_SLOP or \
        mx > x + self.w*self.scale/2 - BBORD_SLOP:
            self.hovered = False
            self.target_scale = 1.0
            return

        #   Not hovered if y is outside button bounds
        if my < y - self.h*self.scale/2 + BBORD_SLOP or \
        my > y + self.h*self.scale/2 - BBORD_SLOP:
            self.hovered = False
            self.target_scale = 1.0
            return

        #   If you made it this far, the mouse is over the button.
        self.target_scale = 1.02
        if self.h < 125:
            self.target_scale = 1.1
        self.hovered = True

    """ Sets the button's position, based on what number that button is as an
        option. For instance, the number 0 answer button will be at the top
        left. """
    def set_position_from_number(self, n):

        #   Set x position
        x = int(FRAME_WIDTH/2 - self.w/2 - BUTTON_BORDER/2)
        if n%2 == 1:
            x = int(FRAME_WIDTH/2 + self.w/2 + BUTTON_BORDER/2)

        #   Set y position
        y = int(FRAME_HEIGHT/2 + self.h/2 + BUTTON_Y_OFFSET)
        if (n//2)%2 == 1:
            y = int(FRAME_HEIGHT/2 + BUTTON_Y_OFFSET + 3*self.h/2 + BUTTON_BORDER)

        self.pos = (x, y)
        self.target_pos = self.pos
        self.appear_time = n * 0.2

    """ Toggles the value of the selected attribute, such as when mouse is
        clicked. """
    def toggle_select(self):
        self.selected = not self.selected

    def click(self):
        self.selected = True
        self.scale = 1.10

    """ Update the button """
    def update(self, dt):

        #   Update scale with proportional control
        if self.disappearing:
            self.scale_p = 10
            self.target_scale = -0.05
        ds = self.target_scale - self.scale
        delta = ds * dt * self.scale_p
        if abs(delta) > abs(ds):
            delta = ds
        self.scale += delta
        if not self.visible:
            self.scale = 0
        if self.scale < 0:
            self.scale = 0

        #   Update position with proportional control
        dx = self.target_pos[0] - self.pos[0]
        dy = self.target_pos[1] - self.pos[1]

        speed = 10
        deltax = dx * dt * speed
        deltay = dy * dt * speed
        if abs(deltax) > abs(dx): deltax = dx
        if abs(deltay) > abs(dy): deltay = dy

        self.pos = (self.pos[0] + deltax, self.pos[1] + deltay)

        #   Update internal time, and appear if necessary
        self.time += dt
        if self.time > self.appear_time and not self.visible and self.appear_time < 1000:
            self.visible = True

    def move_to_center(self):
        self.target_pos = (int(FRAME_WIDTH/2), int(FRAME_HEIGHT/2) + 80)

""" Class for the submit button """
class SubmitButton(AnswerButton):

        """ Initialize method for SubmitButton """
        def __init__(self, text, globals):
            self.g = globals
            self.text = text

            #   Load image files for button in different combinations of being
            #   currently selected and being hovered by the mouse.
            self.surf = self.g.load_image("images/submit_button.png")
            self.hover_surf = self.g.load_image("images/submit_button_hover.png")

            #   Set a position to render and save width and height. The position is
            #   defined as the location of the top left corner of the button, in
            #   pixels from the origin.
            self.pos = (0, 0)
            self.target_pos = self.pos
            self.w = self.surf.get_width()
            self.h = self.surf.get_height()
            self.scale = 1.0
            self.target_scale = 1.0
            self.scale_p = 15

            #   Booleans for being hovered or selected
            self.hovered = False
            self.selected = False
            self.visible = False
            self.disappearing = False

            self.time = 0
            self.appear_time = 99999999

            self.text_render = self.g.submit_font.render(text, 1,
                                                    SUBMIT_FONT_COLOR)

        """ Draws the button onto the screen attribute of self.g """
        def draw(self, obs = False):

            self.visible = obs

            #   Don't do anything if button isn't visible
            if not self.visible: return

            #   Determine which surface to draw based on state of button
            surf = self.surf
            if self.hovered:
                surf = self.hover_surf

            #   Draw the text onto the button
            surf.blit(self.text_render,
                (int(self.w/2 - self.text_render.get_width()/2),
                int(self.h/2 - self.text_render.get_height()/2)))

            #   Scale the button as necessary
            surf = pygame.transform.scale(surf,
                (int(surf.get_width() * self.scale),
                int(surf.get_height() * self.scale)))

            #   Draw that surface on the screen
            self.g.screen.blit(surf,
                (self.pos[0] - int(surf.get_width()/2),
                self.pos[1] - int(surf.get_height()/2)))

        """ Sets the submit button to where it should be """
        def set_position(self):
            x = int(FRAME_WIDTH/2)
            y = FRAME_HEIGHT - self.h/2 + SUBMIT_BUTTON_Y_OFFSET
            self.pos = x, y
            self.target_pos = self.pos

        """ Keep this button as True as long as it has been clicked """
        def toggle_select(self):
            self.selected = True


class ContinueButton(SubmitButton):

        """ Initialize method for ContinueButton """
        def __init__(self, text, globals):
            self.g = globals
            self.text = text

            #   Load image files for button in different combinations of being
            #   currently selected and being hovered by the mouse.
            self.surf = self.g.load_image("images/score_button.png")
            self.hover_surf = self.g.load_image("images/score_button_hover.png")

            #   Set a position to render and save width and height. The position is
            #   defined as the location of the top left corner of the button, in
            #   pixels from the origin.
            self.pos = (0, 0)
            self.target_pos = self.pos
            self.w = self.surf.get_width()
            self.h = self.surf.get_height()
            self.scale = 1.0
            self.target_scale = 1.0
            self.scale_p = 15

            #   Booleans for being hovered or selected
            self.hovered = False
            self.selected = False
            self.visible = False
            self.disappearing = False

            self.time = 0
            self.appear_time = 0.5

            self.text_render = self.g.continue_font.render(text, 1,
                                                    CONTINUE_FONT_COLOR)

    
        def draw(self):
            SubmitButton.draw(self, True)
