##!/usr/bin/env python

import random
from constants import *

""" Data structure representing a question. It has the text for the question,
    text for each of the answer options, and memory of which of the
    answers is correct. """
class Question(object):

    """ Initialization method for the question object. The 'text' field should
    be a newline-separated string, where the first line is the text for the
    question and each subsequent line is text for each answer. The correct
    answer should have an astrisk as the first character, which is removed
    before it's displayed. """
    def __init__(self, text):
        self.parse_text(text)


    """ Parses the text for the question. """
    def parse_text(self, text):
        self.correct_answer = -1
        text = text.strip()         #   Removes whitespace from ends of string
        text = text.split("\n")     #   Breaks up the text into each line
        self.question = text[0]     #   First line is question
        self.answers = text[1:]     #   All other lines are answers

        #   Finds the correct answer by checking for asterisks
        for idx, answer in enumerate(self.answers):
            if answer[0] == "*":
                self.correct_answer = idx
                self.answers[idx] = answer[1:]  #   Remove the asterisk
                break

        #   Randomly shuffle the order of the answer options
        if RANDOMIZE_ANSWER_ORDER:
            random.shuffle(self.answers)

        #   If an answer is "all of the above" or "none of the above", make sure
        #   it's displayed last... otherwise it makes no sense!
        for (i, ans) in enumerate(self.answers):
            if ans.lower() == "all of the above" or \
                ans.lower() == "none of the above":
                    self.answers[-1], self.answers[i] = \
                    self.answers[i], self.answers[-1]


    """ Returns true if the answer choice is correct; otherwise, false """
    def is_correct(self, num):
        return (num == self.correct_answer)


    def __repr__(self):
        question = self.question + "\n"
        answers = "\n".join(self.answers) + "\n"
        return question + answers


""" Data structure for an ordered set of questions. """
class QuestionSet(object):

    """ Initialization method for QuestionSet. Makes a list of Question objects
        by reading from a file, located at 'text_path' """
    def __init__(self, text_path):
        file_obj = open(text_path, 'r')
        text = file_obj.read()
        file_obj.close()
        self.parse_all_questions(text)


    """ Parses the given text file to assemble a list of questions """
    def parse_all_questions(self, text):
        text = text.strip()
        text = text.split("\n\n")
        self.questions = []

        #   Assemble a list of questions from file
        for question_text in text:
            self.questions.append(Question(question_text))
