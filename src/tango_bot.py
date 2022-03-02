# tango_bot.py

from .usb import serial, getUSB
from .log import log

class TangBotController:

    # properties
    usb:serial.Serial   = None
    cmd                 = None
    TARGET_CENTER:int   = 5896
    WAIST_VAL:int       = TARGET_CENTER
    HEAD_TILT_VAL:int   = TARGET_CENTER     # This is the up/down value
    HEAD_TURN_VAL:int   = TARGET_CENTER     # This is the left/right value
    LEFT_MOTOR:int      = 0                 # This is the current speed of the motor
    RIGHT_MOTOR:int     = 0                 # This is the current speed of the motor
    SPEED:int           = 200               # This is the current update to the motor

    # constructor
    def __init__(self):
        self.usb = getUSB()
        # TODO: the following it just temporary
        target = 5896
        # Build command
        lsb = target &0x7F
        msb = (target >> 7) & 0x7F
        self.cmd = chr(0xaa) + chr(0xC) + chr(0x04) + chr(0x02) + chr(lsb) + chr(msb)
        self.writeCmd()

    # write out command to usb
    def writeCmd(self):
        # Check if usb is not None
        command = self.cmd.encode('utf-8')
        log.debug('Writing USB Command: "%s"', command)
        if self.usb is not None:
            self.usb.write(command)
        else:
            log.critical('Unable to write to USB - USB not connected')

    def moveWaistLeft(self):
        self.WAIST_VAL += self.SPEED
        # TODO: write update to USB

    def moveWaistRight(self):
        self.WAIST_VAL -= self.SPEED
        # TODO: write update to USB

    def moveHeadUp(self):
        self.HEAD_TILT_VAL += self.SPEED  # Check that this moves up not down
        # TODO: write update to USB

    def moveHeadDown(self):
        self.HEAD_TILT_VAL -= self.SPEED  # Check that this moves down not up
        # TODO: write update to USB

    def moveHeadLeft(self):
        self.HEAD_TURN_VAL += self.SPEED  # Check that this moves left not right
        # TODO: write update to USB

    def moveHeadRight(self):
        self.HEAD_TURN_VAL -= self.SPEED  # Check that this moves right not left
        # TODO: write update to USB

# END
