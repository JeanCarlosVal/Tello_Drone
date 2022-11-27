import pygame

from djitellopy import Tello

controller = None
up_down = 0
left_right = 0
forward_backward = 0
yaw = 0


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
    global controller
    global up_down
    global left_right
    global forward_backward
    global yaw

    name = joystick.get_name()
    textPrint.tprint(screen, "Joystick name: {}".format(name))

    if name == 'Controller (Xbox One For Windows)':
        controller = XboxController

    try:
        guid = joystick.get_guid()
    except AttributeError:
        # get_guid() is an SDL2 method
        pass
    else:
        textPrint.tprint(screen, "GUID: {}".format(guid))

    battery = tello.get_battery()
    flight_time = tello.get_flight_time()
    temperature = tello.get_temperature()
    altitude = tello.get_height()
    textPrint.tprint(screen, "Drone Info:")
    textPrint.indent()
    textPrint.tprint(screen, "Battery ----> {}".format(battery))
    textPrint.tprint(screen, "Flight Time ----> {}s".format(flight_time))
    textPrint.tprint(screen, "Temperature ----> {}".format(temperature))
    textPrint.tprint(screen, "Altitude ----> {}".format(altitude))
    textPrint.unindent()

    # Usually axis run in pairs, up/down for one, and left/right for
    # the other.
    axes = joystick.get_numaxes()
    textPrint.tprint(screen, "Drone Movement:")
    textPrint.indent()

    for i in range(axes):
        axis = joystick.get_axis(i)
        if i == controller.LEFT_X:
            if axis < (0 - controller.DEAD_ZONE):
                textPrint.tprint(screen, "Left: {:.0f}".format(axis * 100))

                left_right = int(axis * 100)

                tello.send_rc_control(left_right, forward_backward, up_down, yaw)
            elif axis > (0 + controller.DEAD_ZONE):
                textPrint.tprint(screen, "Right: {:.0f}".format(axis * 100))

                left_right = int(axis * 100)

                tello.send_rc_control(left_right, forward_backward, up_down, yaw)
        elif i == controller.LEFT_Y:
            if axis < (0 - controller.DEAD_ZONE):
                textPrint.tprint(screen, "Forward: {:.0f}".format((axis * 100) * controller.INVERTED))

                forward_backward = int((axis * 100) * controller.INVERTED)

                tello.send_rc_control(left_right, forward_backward, up_down, yaw)
            elif axis > (0 + controller.DEAD_ZONE):
                textPrint.tprint(screen, "Backwards: {:.0f}".format((axis * 100) * controller.INVERTED))

                forward_backward = int((axis * 100) * controller.INVERTED)

                tello.send_rc_control(left_right, forward_backward, up_down, yaw)
        elif i == controller.RIGHT_X:
            if axis < (0 - controller.DEAD_ZONE):
                textPrint.tprint(screen, "Yaw: {:.0f}".format(axis * 100))

                yaw = int(axis * 100)

                tello.send_rc_control(left_right, forward_backward, up_down, yaw)
            elif axis > (0 + controller.DEAD_ZONE):
                textPrint.tprint(screen, "Yaw: {:.0f}".format(axis * 100))

                yaw = int(axis * 100)

                tello.send_rc_control(left_right, forward_backward, up_down, yaw)
        elif i == controller.RIGHT_Y:
            if axis < (0 - controller.DEAD_ZONE):
                textPrint.tprint(screen, "Up: {:.0f}".format((axis * 100) * controller.INVERTED))

                up_down = int((axis * 100) * controller.INVERTED)

                tello.send_rc_control(left_right, forward_backward, up_down, yaw)
            elif axis > (0 + controller.DEAD_ZONE):
                textPrint.tprint(screen, "Down: {:.0f}".format((axis * 100) * controller.INVERTED))

                up_down = int((axis * 100) * controller.INVERTED)

                tello.send_rc_control(left_right, forward_backward, up_down, yaw)
    textPrint.unindent()

    buttons = joystick.get_numbuttons()
    textPrint.tprint(screen, "Drone Status:")
    textPrint.indent()

    for i in range(buttons):
        button = joystick.get_button(i)
        if i == controller.TAKEOFF:
            if button == 1:
                textPrint.tprint(screen, "Taking Off....")
                tello.takeoff()
        if i == controller.LAND:
            if button == 1:
                textPrint.tprint(screen, "Landing......")
                tello.land()
    textPrint.unindent()


pygame.init()

# Set the width and height of the screen (width, height).
screen = pygame.display.set_mode((500, 700))

pygame.display.set_caption("Drone_View")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates.
clock = pygame.time.Clock()

# Initialize the joysticks.
pygame.joystick.init()

# Get ready to print.
textPrint = TextPrint()

# tello drone object
tello = Tello()

# connect to tello
tello.connect()

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
    clock.tick(60)

pygame.quit()