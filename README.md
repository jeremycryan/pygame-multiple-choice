# Pygame Multiple Choice Test
A multiple choice test GUI demo for pygame.

![A screenshot from the demo. The question "What element has atomic number 6?" is displayed, along with four rectangular answer boxes containing the answers boron, magnesium, carbon, and oxygen, which is highlighted. Below the answer choices is a green "submit" button.](https://github.com/jeremycryan/pygame-multiple-choice/blob/master/images/sample_gui.png?raw=true)

## How to Use
### Install pygame
If you don't have pygame installed already, you can use pip to install it:
```python3 -m pip install -U pygame --user```

Alternatively, for Windows:
```py -m pip install -U pygame --user```

If you don't have pip set up, you can view [the pygame docs](https://www.pygame.org/wiki/GettingStarted) for instructions for compiling from source.


### Clone this repository
While in the directory you want to use, run the following command to make a local clone of this repository:

```git clone https://github.com/jeremycryan/pygame-multiple-choice```

Alternatively, you can fork this repository or download the files without cloning.

### Run the demo

In the newly-created ```pygame-multiple-choice``` file, you can run one of the following commands to run the demo test:

**Windows:**
```py -3 main.py```

**Linux:**
```python3 main.py```

### Input your own test
Now that you have an idea of how the program works, you can edit ```questions.txt``` to include your own multiple choice questions. It expects the syntax detailed below:

```What is the airspeed velocity of an unladen swallow?
*African or European?
Well... I don't know that
About 20 MPH
Pretty fast, I'd reckon
```

In each "paragraph," there should be exactly five newline-separated strings. 

The first of these is the question that will be displayed (in the example, "What is the airspeed velocity of an unladen swallow?"). There are no restrictions on how the question is formatted, as long as it contains no newlines or non-UTF-8 characters.

The other four lines contain, in any order:
- A *correct answer*, which starts with an asterisk (*).
- **Exactly** three *incorrect answers*, which are not permitted to start with an asterisk, although they can include an asterisk somewhere in the middle.

Currently, there is no support for questions with more or fewer than four answer choices.

Each of these "paragraphs," should be separated by two newline characters, as seen in the example ```questions.txt```.
