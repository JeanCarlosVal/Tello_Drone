import os
import boto3
import pygame
from djitellopy import Tello
from datetime import datetime
from random import *
from dotenv import find_dotenv, load_dotenv
from db.dynamo_db import DroneDb

# input fields status color
name_color = None
email_color = None
department_color = None

# user input Fields
user_email = pygame.Rect
user_name = pygame.Rect
user_department = pygame.Rect
submit_button = pygame.Rect

# checker if user has submitted information
user_info = False

# controller values to move drone
controller = None
up_down = 0
left_right = 0
forward_backward = 0
yaw = 0

# finding environment variable
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

# dynamodb references
client = boto3.client(
    'dynamodb',
    aws_access_key_id=os.getenv('DB_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('DB_SECRET_ACCESS_KEY_ID'),
    region_name='us-east-1'
)

dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id=os.getenv('DB_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('DB_SECRET_ACCESS_KEY_ID'),
    region_name='us-east-1'
)

ddb_exceptions = client.exceptions


# This is a class we are going to use to print the user prompts
class UserInputPrint(object):
    def __init__(self):
        self.line_height = None
        self.y = None
        self.x = None
        self.reset()
        self.font = pygame.font.Font(None, 20)

    def print_prompt(self, view, prompt):
        text = self.font.render(prompt, True, WHITE)
        view.blit(text, (self.x, self.y))
        self.y += self.line_height

    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 20


# We are going to use this class to render input fields in the screen
class Input(UserInputPrint):
    def __init__(self):
        super().__init__()
        self.border = 2
        self.name_active = False
        self.email_active = False
        self.department_active = False
        self.name_input = ''
        self.email_input = ''
        self.department_input = ''
        self.flight_id = None
        self.flight_time = None

        # Render user input coming from keyboard

    def render_input(self, view, rectangle, color, text):
        self.x += 10
        self.y += 10
        pygame.draw.rect(view, color, rectangle, self.border)
        text_surface = user.font.render(text, True, WHITE)
        screen.blit(text_surface, (rectangle.x + 5, rectangle.y + 5))
        self.x -= 10
        self.y += 50

        # Render the button to submit the information

    def render_button(self, view, rectangle, color, text):
        self.x += 50
        self.y += 10
        pygame.draw.rect(view, color, rectangle)
        text_surface = user.font.render(text, True, BLACK)
        screen.blit(text_surface, (rectangle.x + 5, rectangle.y + 5))


# class for XBOX controller button mapping
class XboxController:
    # Buttons
    TAKEOFF = 5
    LAND = 4

    # Joysticks
    LEFT_Y = 1  # forward -1 backwards 1
    LEFT_X = 0  # Left -1 Right 1
    RIGHT_Y = 3  # up -1 down 1
    RIGHT_X = 2  # Rotate left -1 Rotate right 1

    LEFT = -1
    UP = -1
    ROTATE_LEFT = -1
    FORWARD = -1

    # Joystick still have input if not moved
    DEAD_ZONE = 0.06

    # Controller is output is inverted by default
    INVERTED = -1


# Define some colors.
BLACK = pygame.Color('black')
WHITE = pygame.Color('white')


# This is a simple class that will help us print to the view.
class DroneInfoPrint(object):
    def __init__(self):
        self.line_height = None
        self.y = None
        self.x = None
        self.reset()
        self.font = pygame.font.Font(None, 20)

    def tprint(self, view, text_string):
        text_bitmap = self.font.render(text_string, True, BLACK)
        view.blit(text_bitmap, (self.x, self.y))
        self.y += self.line_height

    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15

    def indent(self):
        self.x += 10

    def unindent(self):
        self.x -= 10


# This displays what the controller is making the drone do along with some extra data that the drone is sending back
def display_controller_input():
    # Get the name from the OS for the controller/joystick.
    global controller
    global up_down
    global left_right
    global forward_backward
    global yaw

    name = joystick.get_name()  # get the name of the controller
    droneInfoPrint.tprint(screen, "Joystick name: {}".format(name))

    # If name of controller matches the string use xbox button mapping class
    if name == 'Controller (Xbox One For Windows)':
        controller = XboxController

    try:
        guid = joystick.get_guid()
    except AttributeError:
        # get_guid() is an SDL2 method
        pass
    else:
        droneInfoPrint.tprint(screen, "GUID: {}".format(guid))

    # printing drone liver status attributes into the screen
    battery = tello.get_battery()
    flight_time = tello.get_flight_time()
    temperature = tello.get_temperature()
    altitude = tello.get_height()
    droneInfoPrint.tprint(screen, "Drone Info:")
    droneInfoPrint.indent()
    droneInfoPrint.tprint(screen, "Battery ----> {}".format(battery))
    droneInfoPrint.tprint(screen, "Flight Time ----> {}s".format(flight_time))
    droneInfoPrint.tprint(screen, "Temperature ----> {}".format(temperature))
    droneInfoPrint.tprint(screen, "Altitude ----> {}".format(altitude))
    droneInfoPrint.unindent()

    # Usually axis run in pairs, up/down for one, and left/right for
    # the other.
    axes = joystick.get_numaxes()
    droneInfoPrint.tprint(screen, "Drone Movement:")
    droneInfoPrint.indent()

    # Printing the drone movement along with giving commands to drone using joysticks
    for num in range(axes):
        axis = joystick.get_axis(num)
        if num == controller.LEFT_X:
            if axis < (0 - controller.DEAD_ZONE):
                droneInfoPrint.tprint(screen, "Left: {:.0f}".format(axis * 100))

                left_right = int(axis * 100)

                tello.send_rc_control(left_right, forward_backward, up_down, yaw)
            elif axis > (0 + controller.DEAD_ZONE):
                droneInfoPrint.tprint(screen, "Right: {:.0f}".format(axis * 100))

                left_right = int(axis * 100)

                tello.send_rc_control(left_right, forward_backward, up_down, yaw)
        elif num == controller.LEFT_Y:
            if axis < (0 - controller.DEAD_ZONE):
                droneInfoPrint.tprint(screen, "Forward: {:.0f}".format((axis * 100) * controller.INVERTED))

                forward_backward = int((axis * 100) * controller.INVERTED)

                tello.send_rc_control(left_right, forward_backward, up_down, yaw)
            elif axis > (0 + controller.DEAD_ZONE):
                droneInfoPrint.tprint(screen, "Backwards: {:.0f}".format((axis * 100) * controller.INVERTED))

                forward_backward = int((axis * 100) * controller.INVERTED)

                tello.send_rc_control(left_right, forward_backward, up_down, yaw)
        elif num == controller.RIGHT_X:
            if axis < (0 - controller.DEAD_ZONE):
                droneInfoPrint.tprint(screen, "Yaw: {:.0f}".format(axis * 100))

                yaw = int(axis * 100)

                tello.send_rc_control(left_right, forward_backward, up_down, yaw)
            elif axis > (0 + controller.DEAD_ZONE):
                droneInfoPrint.tprint(screen, "Yaw: {:.0f}".format(axis * 100))

                yaw = int(axis * 100)

                tello.send_rc_control(left_right, forward_backward, up_down, yaw)
        elif num == controller.RIGHT_Y:
            if axis < (0 - controller.DEAD_ZONE):
                droneInfoPrint.tprint(screen, "Up: {:.0f}".format((axis * 100) * controller.INVERTED))

                up_down = int((axis * 100) * controller.INVERTED)

                tello.send_rc_control(left_right, forward_backward, up_down, yaw)
            elif axis > (0 + controller.DEAD_ZONE):
                droneInfoPrint.tprint(screen, "Down: {:.0f}".format((axis * 100) * controller.INVERTED))

                up_down = int((axis * 100) * controller.INVERTED)

                tello.send_rc_control(left_right, forward_backward, up_down, yaw)
    droneInfoPrint.unindent()

    # Getting the buttons reference from the controller
    buttons = joystick.get_numbuttons()
    droneInfoPrint.tprint(screen, "Drone Status:")
    droneInfoPrint.indent()

    # listening for any take off or land commands from the controller using the bumpers
    for input_ in range(buttons):
        button = joystick.get_button(input_)
        if input_ == controller.TAKEOFF:
            if button == 1:
                droneInfoPrint.tprint(screen, "Taking Off....")
                tello.takeoff()
        if input_ == controller.LAND:
            if button == 1:
                response = tello.send_command_with_return('land', timeout=7)
                droneInfoPrint.tprint(screen, "Landing......")

                if 'ok' in response.lower():
                    table.insert_item(user.flight_id, flight_time, user.name_input, user.email_input,
                                      user.department_input)

    droneInfoPrint.unindent()


# Activating input fields if user clicks into one and blocking the fields if user clicks on somthing else, also it will
# store whatever the user typed into variables
def user_input():
    # colors for textBoxes to display between active or inactive
    color_active = pygame.Color('lightskyblue3')
    color_passive = pygame.Color('gray15')

    global name_color
    global email_color
    global department_color
    global user_info

    # setting color values depending on if they are active or not
    if user.department_active:
        department_color = color_active
    else:
        department_color = color_passive

    if user.name_active:
        name_color = color_active
    else:
        name_color = color_passive

    if user.email_active:
        email_color = color_active
    else:
        email_color = color_passive

    # activating or deactivating input fields when clicked
    if event.type == pygame.MOUSEBUTTONDOWN:
        if user_name.collidepoint(event.pos):
            user.name_active = True
        else:
            user.name_active = False

        if user_email.collidepoint(event.pos):
            user.email_active = True
        else:
            user.email_active = False

        if user_department.collidepoint(event.pos):
            user.department_active = True
        else:
            user.department_active = False

        if submit_button.collidepoint(event.pos):
            user.flight_id = generate_flight_id()
            user_info = True
            print("name: {} Email: {} Department: {} Flight_ID: {}".format(user.name_input, user.email_input,
                                                                           user.department_input, user.flight_id))

    # Storing user information in variables
    if event.type == pygame.KEYDOWN:
        if user.name_active:
            if event.key == pygame.K_BACKSPACE:
                user.name_input = user.name_input[:-1]
            else:
                user.name_input += event.unicode

        if user.email_active:
            if event.key == pygame.K_BACKSPACE:
                user.email_input = user.email_input[:-1]
            else:
                user.email_input += event.unicode

        if user.department_active:
            if event.key == pygame.K_BACKSPACE:
                user.department_input = user.department_input[:-1]
            else:
                user.department_input += event.unicode


# Rendering the hole user input interface
def render_userinput():
    global user_email
    global user_name
    global user_department
    global submit_button

    # Rendering Prompts to user
    user.print_prompt(screen, "Name:")
    user_name = pygame.Rect(user.x, user.y, 240, 32)
    user.render_input(screen, user_name, name_color, user.name_input)

    user.print_prompt(screen, "Email")
    user_email = pygame.Rect(user.x, user.y, 240, 32)
    user.render_input(screen, user_email, email_color, user.email_input)

    user.print_prompt(screen, "Department")
    user_department = pygame.Rect(user.x, user.y, 240, 32)
    user.render_input(screen, user_department, department_color, user.department_input)

    submit_button = pygame.Rect(user.x, user.y, 100, 22)
    user.render_button(screen, submit_button, pygame.Color('white'), 'Submit')


# generating a flight id
def generate_flight_id():
    flight_id = datetime.today().strftime('%Y-%m-%d')
    flight_id += "."
    flight_id += str(randint(0, 1000))

    return flight_id


# initializing pygame
pygame.init()

# Set the width and height of the view (width, height).
screen = pygame.display.set_mode((1000, 1000))

pygame.display.set_caption("Drone_View")

# Loop until the user clicks the close button.
done = False

# Keep view black with user input until user is done submitting information
user = Input()

# Used to manage how fast the view updates.
clock = pygame.time.Clock()

# Initialize the joysticks.
pygame.joystick.init()

# Get ready to print.
droneInfoPrint = DroneInfoPrint()

# tello drone object
tello = Tello()

# connect to tello
tello.connect()

# dynamodb table object
table = DroneDb(dynamodb)

# -------- Main Program Loop -----------
while not done:

    for event in pygame.event.get():  # User did something.
        if event.type == pygame.QUIT:  # If user clicked close.
            done = True
        user_input()

    # First, clear the view to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    if not user_info:
        screen.fill(BLACK)
        user.reset()
        render_userinput()
    else:
        screen.fill(WHITE)
        droneInfoPrint.reset()

        # Get count of joysticks.
        joystick_count = pygame.joystick.get_count()

        # For each joystick:
        for i in range(joystick_count):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()

            display_controller_input()

    pygame.display.flip()

    # Limit to 20 frames per second.
    clock.tick(60)

pygame.quit()
