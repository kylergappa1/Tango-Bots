# tango_bot.py

import threading
import time
from enum import Enum

from .log import log
from .usb import serial, getUSB


class BotServos(Enum):
    LeftWheel = 0x00
    RightWheel = 0x01
    Waist = 0x02
    HeadPan = 0x03
    HeadTilt = 0x04


class TangBotController:

    # properties
    usb: serial.Serial   = None
    cmd                 = None
    TARGET_CENTER: int   = 5896
    SPEED_START: int     = 6000              # No Motor Movement ????
    WAIST_VAL: int       = TARGET_CENTER
    HEAD_TILT_VAL: int   = TARGET_CENTER     # This is the up/down value
    HEAD_TURN_VAL: int   = TARGET_CENTER     # This is the left/right value
    LEFT_MOTOR: int      = TARGET_CENTER     # This is the current speed of the motor
    RIGHT_MOTOR: int     = TARGET_CENTER     # This is the current speed of the motor
    WHEEL_SPEED: int     = SPEED_START       # When the robot is going forward/backward, the wheel speed is the same
    SPEED: int           = 300               # This is the current update to the motor
    SPEED_CEILING: int   = 7500              # Upper limit for wheel speed
    SPEED_FLOOR: int     = 4500              # Lower limit for wheel speed
    

    running:bool        = None
    lock:threading.Lock = None

    direction_state = None
    turning_timeout = 2
    turning_left = None
    turning_left_start_time = None
    turning_right = None
    turning_right_start_time = None

    # constructor
    def __init__(self):
        self.usb = getUSB()
        # if self.usb is not None:
        #     self.usb.write_timeout = 0.5  # TEST THIS
        self.running = True
        self.lock = threading.Lock()
        # Exit Safe Start
        # Note: something I found online
        # TODO: see if we need this
        if self.usb is not None:
            self.usb.write(chr(0x83).encode())

        self.writeCmd(BotServos.RightWheel.value, self.SPEED_START)
        self.writeCmd(BotServos.LeftWheel.value, self.SPEED_START)
        # center waist
        time.sleep(.5)
        self.writeCmd(BotServos.Waist.value, self.TARGET_CENTER)
        time.sleep(.5)
        self.writeCmd(BotServos.HeadTilt.value, self.TARGET_CENTER)
        time.sleep(.5)
        self.writeCmd(BotServos.HeadPan.value, self.TARGET_CENTER)

    # Stop the robot
    def stop(self):
        self.running = False
        self.stopMoving()

    def writeCmd(self, chr_val, target: int = TARGET_CENTER):
        # Build command
        lsb = target & 0x7F
        msb = (target >> 7) & 0x7F
        self.cmd = chr(0xaa) + chr(0xC) + chr(0x04) + chr(chr_val) + chr(lsb) + chr(msb)
        command = self.cmd.encode('utf-8')
        log.debug('Writing USB Command: "%s"', command)
        # Check if usb is not None
        if self.usb is not None:
            self.usb.write(command)
        else:
            log.critical('Unable to write to USB - USB not connected')

    # write out command to usb
    def setSpeed(self, speed: int):
        self.SPEED = speed

    def stopMoving(self):
        # print('Trying to stop motors')
        self.writeCmd(BotServos.RightWheel.value, self.SPEED_START)
        self.writeCmd(BotServos.LeftWheel.value, self.SPEED_START)

    def moveWaistLeft(self):
        self.WAIST_VAL += self.SPEED
        log.debug('Move Waist Left - Value: "%s"', self.WAIST_VAL)
        self.writeCmd(BotServos.Waist.value, self.WAIST_VAL)
        time.sleep(.2)

    def moveWaistRight(self):
        self.WAIST_VAL -= self.SPEED
        log.debug('Move Waist Right - Value: "%s"', self.WAIST_VAL)
        self.writeCmd(BotServos.Waist.value, self.WAIST_VAL)

    def centerWaist(self):
        self.WAIST_VAL = self.TARGET_CENTER
        log.debug('Center - Value: "%s"', self.WAIST_VAL)
        self.writeCmd(BotServos.Waist.value, self.WAIST_VAL)


    def moveHeadUp(self):
        self.HEAD_TILT_VAL += self.SPEED
        log.debug('Move Head Up - Value: "%s"', self.HEAD_TILT_VAL)
        self.writeCmd(BotServos.HeadTilt.value, self.HEAD_TILT_VAL)
        time.sleep(.2)

    def moveHeadDown(self):
        self.HEAD_TILT_VAL -= self.SPEED
        log.debug('Move Head Down - Value: "%s"', self.HEAD_TILT_VAL)
        self.writeCmd(BotServos.HeadTilt.value, self.HEAD_TILT_VAL)
        time.sleep(.2)

    def moveHeadLeft(self):
        self.HEAD_TURN_VAL += self.SPEED
        log.debug('Move Head Left - Value: "%s"', self.HEAD_TURN_VAL)
        self.writeCmd(BotServos.HeadPan.value, self.HEAD_TURN_VAL)
        time.sleep(.2)

    def moveHeadRight(self):
        self.HEAD_TURN_VAL -= self.SPEED
        log.debug('Move Head Right - Value: "%s"', self.HEAD_TURN_VAL)
        self.writeCmd(BotServos.HeadPan.value, self.HEAD_TURN_VAL)
        time.sleep(.2)

    def increaseWheelSpeed(self):

        if self.direction_state != 'f':
            self.stopMoving()
            self.WHEEL_SPEED = self.SPEED_START
        self.direction_state = 'f'


        self.WHEEL_SPEED -= self.SPEED
        # make sure wheel speed does not exceed the upper limit
        if self.WHEEL_SPEED < self.SPEED_FLOOR:
            # set wheel speed to lower limit for wheels
            self.WHEEL_SPEED = self.SPEED_FLOOR
        # Reset robot to make sure it doesn't confuse itself
        # self.writeCmd(BotServos.RightWheel.value, 6000)
        # self.writeCmd(BotServos.LeftWheel.value, 6000)
        # time.sleep(.2)  # Forces robot to finish clearing itself, so it doesn't write incorrectly
        self.writeCmd(BotServos.RightWheel.value, self.WHEEL_SPEED)
        self.writeCmd(BotServos.LeftWheel.value, self.WHEEL_SPEED)
        # time.sleep(.2)

    def decreaseWheelSpeed(self):

        if self.direction_state != 'b':
            self.stopMoving()
            self.WHEEL_SPEED = self.SPEED_START
        self.direction_state = 'b'

        self.WHEEL_SPEED += self.SPEED
        # make sure wheel speed does not exceed the lower limit
        if self.WHEEL_SPEED > self.SPEED_CEILING:
            # set wheel speed to upper limit for wheels
            self.WHEEL_SPEED = self.SPEED_CEILING
        # Reset motors to make sure it doesn't confuse itself
        # self.writeCmd(BotServos.RightWheel.value, 6000)
        # self.writeCmd(BotServos.LeftWheel.value, 6000)
        # time.sleep(0.5)  # Forces robot to finish clearing itself, so it doesn't write incorrectly
#        self.writeCmd(BotServos.RightWheel.value, self.WHEEL_SPEED)
        self.writeCmd(BotServos.LeftWheel.value, self.WHEEL_SPEED)
        # time.sleep(.2)

    def turnLeft(self):
        if self.direction_state != 'l':
            self.stopMoving()
            self.WHEEL_SPEED = self.SPEED_START
        self.direction_state = 'l'
        # make sure wheel speed does not exceed the upper limit
        if self.WHEEL_SPEED - self.SPEED < self.SPEED_FLOOR:
            # set wheel speed to lower limit for wheels
            self.WHEEL_SPEED = self.SPEED_FLOOR
        if self.WHEEL_SPEED + self.SPEED > self.SPEED_CEILING:
            # set wheel speed to upper limit for wheels
            self.WHEEL_SPEED = self.SPEED_CEILING
        # self.writeCmd(BotServos.RightWheel.value, 6000)
        # self.writeCmd(BotServos.LeftWheel.value, 6000)
        # time.sleep(.2)
        self.writeCmd(BotServos.RightWheel.value, 7400)
        time.sleep(.2)
        self.stopMoving()
        # time.sleep(.2)
#        self.writeCmd(BotServos.LeftWheel.value,  7000)  # self.WHEEL_SPEED + self.SPEED)

    def turnRight(self):
        if self.direction_state != 'r':
            self.stopMoving()
            self.WHEEL_SPEED = self.SPEED_START
        self.direction_state = 'r'


        self.writeCmd(BotServos.RightWheel.value, 4600)
        time.sleep(.2)
        self.stopMoving()

        return

        self.stopMoving()
        self.turning_right = True
        self.turning_right_start_time = time.time()

        while self.turning_right_start_time + self.turning_timeout > time.time():
            self.writeCmd(BotServos.RightWheel.value, 5000)
            time.sleep(.2)
            self.stopMoving()
        return



        # make sure wheel speed does not exceed the lower limit
        if self.WHEEL_SPEED - self.SPEED < self.SPEED_FLOOR:
            # set wheel speed to lower limit for wheels
            self.WHEEL_SPEED = self.SPEED_FLOOR
        if self.WHEEL_SPEED + self.SPEED > self.SPEED_CEILING:
            # set wheel speed to upper limit for wheels
            self.WHEEL_SPEED = self.SPEED_CEILING
        # self.writeCmd(BotServos.RightWheel.value, 6000)
        # self.writeCmd(BotServos.LeftWheel.value, 6000)
        # time.sleep(.2)
        while True:
            self.writeCmd(BotServos.RightWheel.value, 5000)
        time.sleep(.2)
        self.stopMoving()
        # time.sleep(.2)
#        self.writeCmd(BotServos.LeftWheel.value, 7000)
# END
