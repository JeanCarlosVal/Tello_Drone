import sys

import pygame

from pygame.locals import *

# basic pygame initialization
pygame.init()
pygame.display.set_caption('game base')
screen = pygame.display.set_mode((500, 500), 0, 32)
clock = pygame.time.Clock()

# Initializing controller objects....
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]

# infinite loop until exit happens
while True:

    for event in pygame.event.get():
        if event.type == JOYBUTTONDOWN:
            # Implement some kind of button mapping below.....
            print(event)
        if event.type == JOYAXISMOTION:
            if event.axis == 1:
                if event.value >= 1:
                    print("left joystick down")
                    # Move backwards code below...

                if event.value <= -1:
                    print("left joystick up")
                    # Move forward code below....

            if event.axis == 0:
                if event.value >= 1:
                    print("left joystick right")
                    # Move to right code below...

                if event.value <= -1:
                    print("left joystick left")
                    # Move to left code below...

            if event.axis == 2:
                if event.value >= 1:
                    print("right Joystick right")
                    # Rotate right code below...

                if event.value <= -1:
                    print("right Joystick left")
                    # Rotate left code below...

            if event.axis == 3:
                if event.value >= 1:
                    print("right joystick down")
                    # Decrease height code below...

                if event.value <= -1:
                    print("right joystick up")
                    # Increase height code below....

        if event.type == JOYHATMOTION:
            print(event)
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
