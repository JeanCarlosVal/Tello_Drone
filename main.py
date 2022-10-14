# import sys
# import time
# import traceback
# import pygame
# import tellopy
# import pygame.locals
# import pygame.key
#
# help(tellopy)
#
# # Define some colors.
# BLACK = pygame.Color('black')
# WHITE = pygame.Color('white')
#
#
# class XboxController:
#     # # d-pad
#     UP = None  # UP
#     DOWN = None  # DOWN
#     ROTATE_LEFT = None # LEFT
#     ROTATE_RIGHT = None  # RIGHT
#
#     # bumper triggers
#     TAKEOFF = 5  # RB
#     LAND = 4  # LB
#     # UNUSED = 7 #RT
#     # UNUSED = 6 #LT
#
#     # buttons
#     FORWARD = 3  # Y
#     BACKWARD = 0  # A
#     LEFT = 2  # X
#     RIGHT = 1  # B
#
#     # axis
#     LEFT_X = 0
#     LEFT_Y = 1
#     RIGHT_X = 2
#     RIGHT_Y = 3
#     LEFT_X_REVERSE = 1.0
#     LEFT_Y_REVERSE = -1.0
#     RIGHT_X_REVERSE = 1.0
#     RIGHT_Y_REVERSE = -1.0
#     DEADZONE = 0.08
#
#
# class PS4controller:
#     # d-pad
#     UP = 11  # UP
#     DOWN = 12  # DOWN
#     ROTATE_LEFT = 13  # LEFT
#     ROTATE_RIGHT = 14  # RIGHT
#
#     # bumper triggers
#     TAKEOFF = 10  # R1
#     LAND = 9  # L1
#     # UNUSED = 7 #R2
#     # UNUSED = 6 #L2
#
#     # buttons
#     FORWARD = 0  # TRIANGLE
#     BACKWARD = 3  # CROSS
#     LEFT = 2  # SQUARE
#     RIGHT = 1  # CIRCLE
#
#     # axis
#     LEFT_X = 0
#     LEFT_Y = 1
#     RIGHT_X = 2
#     RIGHT_Y = 3
#     LEFT_X_REVERSE = 1.0
#     LEFT_Y_REVERSE = -1.0
#     RIGHT_X_REVERSE = 1.0
#     RIGHT_Y_REVERSE = -1.0
#     DEADZONE = 0.09
#
#
# prev_flight_data = None
# run_recv_thread = True
# new_image = None
# flight_data = None
# log_data = None
# buttons = None
# speed = 100
# throttle = 0.0
# yaw = 0.0
# pitch = 0.0
# roll = 0.0
#
#
# def handler(event, sender, data, **args):
#     global prev_flight_data
#     global flight_data
#     global log_data
#     drone = sender
#     if event is drone.EVENT_FLIGHT_DATA:
#         if prev_flight_data != str(data):
#             print(data)
#             prev_flight_data = str(data)
#         flight_data = data
#     elif event is drone.EVENT_LOG_DATA:
#         log_data = data
#     else:
#         print('event="%s" data=%s' % (event.getname(), str(data)))
#
#
# def update(old, new, max_delta=0.3):
#     if abs(old - new) <= max_delta:
#         res = new
#     else:
#         res = 0.0
#     return res
#
#
# def handle_input_event(drone, e):
#     global speed
#     global throttle
#     global yaw
#     global pitch
#     global roll
#     if e.type == pygame.locals.JOYAXISMOTION:
#         # ignore small input values (Deadzone)
#         if -buttons.DEADZONE <= e.value <= buttons.DEADZONE:
#             e.value = 0.0
#         if e.axis == buttons.LEFT_Y:
#             throttle = update(throttle, e.value * buttons.LEFT_Y_REVERSE)
#             drone.set_throttle(throttle)
#         if e.axis == buttons.LEFT_X:
#             yaw = update(yaw, e.value * buttons.LEFT_X_REVERSE)
#             drone.set_yaw(yaw)
#         if e.axis == buttons.RIGHT_Y:
#             pitch = update(pitch, e.value *
#                            buttons.RIGHT_Y_REVERSE)
#             drone.set_pitch(pitch)
#         if e.axis == buttons.RIGHT_X:
#             roll = update(roll, e.value * buttons.RIGHT_X_REVERSE)
#             drone.set_roll(roll)
#     elif e.type == pygame.locals.JOYHATMOTION:
#         if e.value[0] < 0:
#             drone.counter_clockwise(speed)
#         if e.value[0] == 0:
#             drone.clockwise(0)
#         if e.value[0] > 0:
#             drone.clockwise(speed)
#         if e.value[1] < 0:
#             drone.down(speed)
#         if e.value[1] == 0:
#             drone.up(0)
#         if e.value[1] > 0:
#             drone.up(speed)
#     elif e.type == pygame.locals.JOYBUTTONDOWN:
#         if e.button == buttons.LAND:
#             drone.land()
#         elif e.button == buttons.UP:
#             drone.up(speed)
#         elif e.button == buttons.DOWN:
#             drone.down(speed)
#         elif e.button == buttons.ROTATE_RIGHT:
#             drone.clockwise(speed)
#         elif e.button == buttons.ROTATE_LEFT:
#             drone.counter_clockwise(speed)
#         elif e.button == buttons.FORWARD:
#             drone.forward(speed)
#         elif e.button == buttons.BACKWARD:
#             drone.backward(speed)
#         elif e.button == buttons.RIGHT:
#             drone.right(speed)
#         elif e.button == buttons.LEFT:
#             drone.left(speed)
#     elif e.type == pygame.locals.JOYBUTTONUP:
#         if e.button == buttons.TAKEOFF:
#             if throttle != 0.0:
#                 print('###')
#                 print('### throttle != 0.0 (This may hinder the drone from taking off)')
#                 print('###')
#             drone.takeoff()
#         elif e.button == buttons.UP:
#             drone.up(0)
#         elif e.button == buttons.DOWN:
#             drone.down(0)
#         elif e.button == buttons.ROTATE_RIGHT:
#             drone.clockwise(0)
#         elif e.button == buttons.ROTATE_LEFT:
#             drone.counter_clockwise(0)
#         elif e.button == buttons.FORWARD:
#             drone.forward(0)
#         elif e.button == buttons.BACKWARD:
#             drone.backward(0)
#         elif e.button == buttons.RIGHT:
#             drone.right(0)
#         elif e.button == buttons.LEFT:
#             drone.left(0)
#
#
# def main():
#     global buttons
#     global run_recv_thread
#     global new_image
#     pygame.init()
#     pygame.joystick.init()
#
#     try:
#         js = pygame.joystick.Joystick(0)
#         js.init()
#         js_name = js.get_name()
#         print('Joystick name: ' + js_name)
#         if js_name in 'PS4 Controller':
#             buttons = PS4controller
#         elif js_name in 'Controller (Xbox One For Windows)':
#             buttons = XboxController
#     except pygame.error:
#         pass
#
#     if buttons is None:
#         print('no supported joystick found')
#         return
#
#     drone = tellopy.Tello()
#     drone.connect()
#     drone.subscribe(drone.EVENT_FLIGHT_DATA, handler)
#
#     try:
#         while 1:
#             # loop with pygame.event.get() is too much tight w/o some sleep
#             time.sleep(0.01)
#             for e in pygame.event.get():
#                 handle_input_event(drone, e)
#     except KeyboardInterrupt as e:
#         print(e)
#     except Exception as e:
#         exc_type, exc_value, exc_traceback = sys.exc_info()
#         traceback.print_exception(exc_type, exc_value, exc_traceback)
#         print(e)
#
#     drone.quit()
#     exit(1)
#
#
# if __name__ == '__main__':
#     main()


# --------------------------------------------------------------------------------------------
# Code Below is for troubleshooting controller input

import pygame
from djitellopy import Tello

# Define some colors.
BLACK = pygame.Color('black')
WHITE = pygame.Color('white')


# This is a simple class that will help us print to the screen.
class TextPrint(object):
    def __init__(self):
        self.line_height = None
        self.y = None
        self.x = None
        self.reset()
        self.font = pygame.font.Font(None, 20)

    def tprint(self, screen, textString):
        textBitmap = self.font.render(textString, True, BLACK)
        screen.blit(textBitmap, (self.x, self.y))
        self.y += self.line_height

    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15

    def indent(self):
        self.x += 10

    def unindent(self):
        self.x -= 10


def display_controller_input():
    # Get the name from the OS for the controller/joystick.
    name = joystick.get_name()
    textPrint.tprint(screen, "Joystick name: {}".format(name))

    try:
        guid = joystick.get_guid()
    except AttributeError:
        # get_guid() is an SDL2 method
        pass
    else:
        textPrint.tprint(screen, "GUID: {}".format(guid))

    # Usually axis run in pairs, up/down for one, and left/right for
    # the other.
    axes = joystick.get_numaxes()
    textPrint.tprint(screen, "Number of axes: {}".format(axes))
    textPrint.indent()

    for i in range(axes):
        axis = joystick.get_axis(i)
        textPrint.tprint(screen, "Axis {} value: {:>6.5f}".format(i, axis))
    textPrint.unindent()

    buttons = joystick.get_numbuttons()
    textPrint.tprint(screen, "Number of buttons: {}".format(buttons))
    textPrint.indent()

    for i in range(buttons):
        button = joystick.get_button(i)
        textPrint.tprint(screen,
                         "Button {:>2} value: {}".format(i, button))
    textPrint.unindent()


pygame.init()

# Set the width and height of the screen (width, height).
screen = pygame.display.set_mode((500, 700))

pygame.display.set_caption("My Game")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates.
clock = pygame.time.Clock()

# Initialize the joysticks.
pygame.joystick.init()

# Get ready to print.
textPrint = TextPrint()

# Getting Tello drone instance ready
# tello = Tello()
#
# tello.connect()

# -------- Main Program Loop -----------
while not done:

    for event in pygame.event.get():  # User did something.
        if event.type == pygame.QUIT:  # If user clicked close.
            done = True

    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(WHITE)
    textPrint.reset()

    # Get count of joysticks.
    joystick_count = pygame.joystick.get_count()

    # For each joystick:
    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()

        display_controller_input()

    pygame.display.flip()

    # Limit to 20 frames per second.
    clock.tick(20)

pygame.quit()