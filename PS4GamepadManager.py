import time

from Gamepad import Controllers, Gamepad
from InputOscConverter import InputOSCConverter
from networking.UdpMsgSender import UdpMsgSender


class PS4GamepadManager:
    def __init__(self, converter: InputOSCConverter, sender: UdpMsgSender):
        assert converter is not None and sender is not None
        self.converter = converter
        self.sender = sender

        # this code is taken from EventExample.py
        # Gamepad settings
        self.gamepadType = Controllers.PS4

        # buttons
        self.buttonCross = 'CROSS'
        self.buttonSquare = 'SQUARE'
        self.buttonCircle = 'CIRCLE'
        self.buttonTriangle = 'TRIANGLE'
        self.buttonL1 = 'L1'
        self.buttonR1 = 'R1'
        self.buttonPS = 'PS'

        # axes
        self.joystickLeftX = 'LEFT-X'
        self.joystickLeftY = 'LEFT-Y'
        self.joystickRightX = 'RIGHT-X'
        self.joystickRightY = 'RIGHT-Y'
        self.triggerLeft = 'L2'
        self.triggerRight = 'R2'

        # dpad

        self.dpadX = 'DPAD-X'
        self.dpadY = 'DPAD-Y'

        # I'm using a dpad status because it would otherwise send 1 and -1, but
        # I want 1 to be sent on button press and 0 sent on release.
        self.dpadDown = "DPAD-DOWN"
        self.dpadUp = "DPAD-UP"
        self.dpadLeft = "DPAD-LEFT"
        self.dpadRight = "DPAD-RIGHT"

        self.dpad_status = {
            "down": False,
            "up": False,
            "left": False,
            "right": False
        }

        self.pollInterval = 0.2

        # Wait for a connection
        if not Gamepad.available():
            print('Please connect your Gamepad...')
            while not Gamepad.available():
                time.sleep(1.0)
        gamepad = self.gamepadType()
        print('Gamepad connected')

        # Set some initial state
        self.running = True
        self.speed = 0.0
        self.steering = 0.0

        # Start the background updating
        gamepad.startBackgroundUpdates()

        # Register the callback functions

        gamepad.addButtonChangedHandler(self.buttonCross, self.cross_button_changed)
        gamepad.addButtonChangedHandler(self.buttonSquare, self.square_button_changed)
        gamepad.addButtonChangedHandler(self.buttonTriangle, self.triangle_button_changed)
        gamepad.addButtonChangedHandler(self.buttonCircle, self.circle_button_changed)
        gamepad.addButtonChangedHandler(self.buttonL1, self.l1_button_changed)
        gamepad.addButtonChangedHandler(self.buttonR1, self.r1_button_changed)

        gamepad.addAxisMovedHandler(self.joystickLeftX, self.left_x_axis_moved)
        gamepad.addAxisMovedHandler(self.joystickLeftY, self.left_y_axis_moved)
        gamepad.addAxisMovedHandler(self.joystickRightX, self.right_x_axis_moved)
        gamepad.addAxisMovedHandler(self.joystickRightY, self.right_y_axis_moved)

        gamepad.addAxisMovedHandler(self.triggerLeft, self.left_trigger_moved)
        gamepad.addAxisMovedHandler(self.triggerRight, self.right_trigger_moved)

        gamepad.addAxisMovedHandler(self.dpadX, self.dpad_x_moved)
        gamepad.addAxisMovedHandler(self.dpadY, self.dpad_y_moved)

        # Keep running while joystick updates are handled by the callbacks
        try:
            while self.running and gamepad.isConnected():
                # Show the current speed and steering
                # print('%+.1f %% speed, %+.1f %% steering' % (self.speed * 100, self.steering * 100))

                # Sleep for our polling interval
                time.sleep(self.pollInterval)
        finally:
            # Ensure the background thread is always terminated when we are done
            gamepad.disconnect()

    def _send_message(self, message: bytearray):
        self.sender.send_message(message)

    def _send_button_message(self, button, status):
        message = self.converter.get_button_msg(button, status)
        self._send_message(message)

    def _send_axis_message(self, axis, position):
        message = self.converter.get_axis_msg(axis=axis, value=position)
        self._send_message(message)

    # What follows is spaghetti code:

    def cross_button_changed(self, new_value):
        self._send_button_message(self.buttonCross, int(new_value))

    def square_button_changed(self, new_value):
        self._send_button_message(self.buttonSquare, int(new_value))

    def triangle_button_changed(self, new_value):
        self._send_button_message(self.buttonTriangle, int(new_value))

    def circle_button_changed(self, new_value):
        self._send_button_message(self.buttonCircle, int(new_value))

    def l1_button_changed(self, new_value):
        self._send_button_message(self.buttonL1, int(new_value))

    def r1_button_changed(self, new_value):
        self._send_button_message(self.buttonR1, int(new_value))

    # AXES
    def left_x_axis_moved(self, position):
        self._send_axis_message(self.joystickLeftX, position)

    def left_y_axis_moved(self, position):
        self._send_axis_message(self.joystickLeftY, position)

    def right_x_axis_moved(self, position):
        self._send_axis_message(self.joystickRightX, position)

    def right_y_axis_moved(self, position):
        self._send_axis_message(self.joystickRightY, position)

    def left_trigger_moved(self, position):
        self._send_axis_message(self.triggerLeft, position)

    def right_trigger_moved(self, position):
        self._send_axis_message(self.triggerRight, position)

    def dpad_x_moved(self, position):
        # this is written such that we
        # send messages 1/0 on press/release
        if int(position) == 1:
            self._send_button_message(self.dpadRight, 1)
            self.dpad_status['right'] = True
        elif int(position) == -1:
            self._send_button_message(self.dpadLeft, 1)
            self.dpad_status['left'] = True
        else:
            if self.dpad_status['right']:
                self._send_button_message(self.dpadRight, 0)
                self.dpad_status['right'] = False
            if self.dpad_status['left']:
                self._send_button_message(self.dpadLeft, 0)
                self.dpad_status['left'] = False

    def dpad_y_moved(self, position):
        if int(position) == 1:
            self._send_button_message(self.dpadDown, 1)
            self.dpad_status['down'] = True
        elif int(position) == -1:
            self._send_button_message(self.dpadUp, 1)
            self.dpad_status['up'] = True
        else:
            if self.dpad_status['down']:
                self._send_button_message(self.dpadDown, 0)
                self.dpad_status['down'] = False
            if self.dpad_status['up']:
                self._send_button_message(self.dpadUp, 0)
                self.dpad_status['up'] = False
