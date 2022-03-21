# tango_bot.py

from .log import log
from .log import log_method_call
from .usb import serial
from .usb import getUSB
from enum import Enum
from time import sleep

class BotServos(Enum):
    LeftWheel = 0x00
    RightWheel = 0x01
    Waist = 0x02
    HeadPan = 0x03
    HeadTilt = 0x04

class DirectionState(Enum):
    Forwards = 'Forwards'
    Backwards = 'Backwards'
    LeftTurn = 'Left Turn'
    RightTurn = 'Right Turn'

class TangBotController:

    usb: serial.Serial
    _DIRECTION_STATE: DirectionState = None
    TARGET_CENTER: int  = 5896
    SPEED: int          = 300       # This is the current update to the motor
    SPEED_CEILING: int  = 7500      # Upper limit for wheel speed
    SPEED_FLOOR: int    = 4500      # Lower limit for wheel speed
    _HEAD_TILT: int = TARGET_CENTER # This is the up/down value
    _HEAD_TURN: int = TARGET_CENTER # This is the left/right value
    _WAIST: int = TARGET_CENTER
    _WHEEL_SPEED: int = TARGET_CENTER

    # constructor
    def __init__(self):
        self.usb = getUSB()
        self.centerHead()
        self.centerWaist()
        self.WHEEL_SPEED = self.TARGET_CENTER

    def writeCmd(self, bot_servo: BotServos, target: int = TARGET_CENTER):
        # Build command
        lsb = target & 0x7F
        msb = (target >> 7) & 0x7F
        servo_chr = bot_servo.value
        cmd = chr(0xaa) + chr(0xC) + chr(0x04) + chr(servo_chr) + chr(lsb) + chr(msb)
        command = cmd.encode('utf-8')
        # Check if usb is not None
        if self.usb is not None:
            log.debug('Writing USB Command: "%s"', command)
            self.usb.write(command)
            sleep(0.2)
        else:
            log.debug('Unable to write to USB - USB not connected')

    def stop(self):
        self.WHEEL_SPEED = self.TARGET_CENTER

    """
    Speed Movement Methods
    """

    def setSpeed(self, speed: int):
        self.SPEED = speed

    def setSpeedLevelOne(self):
        self.setSpeed(300)

    def setSpeedLevelTwo(self):
        self.setSpeed(500)

    def setSpeedLevelThree(self):
        self.setSpeed(800)

    """
    HEAD Movement Methods
    """

    @property
    def HEAD_TILT(self) -> int:
        return self._HEAD_TILT

    @HEAD_TILT.setter
    def HEAD_TILT(self, val: int):
        self._HEAD_TILT = val
        log.debug('Set HEAD_TILT: %s', self.HEAD_TILT)
        self.writeCmd(BotServos.HeadTilt, self.HEAD_TILT)

    def moveHeadUp(self):
        self.HEAD_TILT += self.SPEED

    def moveHeadDown(self):
        self.HEAD_TILT -= self.SPEED

    @property
    def HEAD_TURN(self) -> int:
        return self._HEAD_TURN

    @HEAD_TURN.setter
    def HEAD_TURN(self, val: int):
        self._HEAD_TURN = val
        log.debug('Set HEAD_TURN: %s', self.HEAD_TURN)
        self.writeCmd(BotServos.HeadPan, self.HEAD_TURN)

    def moveHeadLeft(self):
        self.HEAD_TURN += self.SPEED

    def moveHeadRight(self):
        self.HEAD_TURN -= self.SPEED

    def centerHead(self):
        self.HEAD_TURN = self.TARGET_CENTER
        self.HEAD_TILT = self.TARGET_CENTER

    """
    WAIST Movement Methods
    """

    @property
    def WAIST(self) -> int:
        return self._WAIST

    @WAIST.setter
    def WAIST(self, val: int):
        self._WAIST = val
        log.debug('Set WAIST: %s', self.WAIST)
        self.writeCmd(BotServos.Waist, self.WAIST)

    def centerWaist(self):
        self.WAIST = self.TARGET_CENTER

    def moveWaistLeft(self):
        self.WAIST += self.SPEED

    def moveWaistRight(self):
        self.WAIST -= self.SPEED

    """
    WHEEL Movement Methods
    """

    @property
    def WHEEL_SPEED(self) -> int:
        return self._WHEEL_SPEED

    @WHEEL_SPEED.setter
    def WHEEL_SPEED(self, val: int):
        # make sure wheel speed does not exceed the upper/lower limit
        if val < self.SPEED_FLOOR:
            # set wheel speed to upper limit for wheels
            val = self.SPEED_FLOOR
        elif val > self.SPEED_CEILING:
            # set wheel speed to lower limit for wheels
            val = self.SPEED_CEILING
        self._WHEEL_SPEED = val
        log.debug('Set WHEEL_SPEED: %s', self.WHEEL_SPEED)
        self.writeCmd(BotServos.RightWheel, self.WHEEL_SPEED)
        self.writeCmd(BotServos.LeftWheel, self.WHEEL_SPEED)

    @property
    def DIRECTION_STATE(self):
        return self._DIRECTION_STATE

    @DIRECTION_STATE.setter
    def DIRECTION_STATE(self, val: DirectionState):
        if isinstance(val, DirectionState) and isinstance(self._DIRECTION_STATE, DirectionState) and self._DIRECTION_STATE != val:
            self.WHEEL_SPEED = self.TARGET_CENTER
        self._DIRECTION_STATE = val

    def increaseWheelSpeed(self):
        self.DIRECTION_STATE = DirectionState.Forwards
        self.WHEEL_SPEED -= self.SPEED

    def decreaseWheelSpeed(self):
        self.DIRECTION_STATE = DirectionState.Backwards
        self.WHEEL_SPEED += self.SPEED
        self.writeCmd(BotServos.LeftWheel, self.WHEEL_SPEED)

    def turnLeft(self):
        self.DIRECTION_STATE = DirectionState.LeftTurn
        self.writeCmd(BotServos.RightWheel, 7400)
        self.stop()

    def turnRight(self):
        self.DIRECTION_STATE = DirectionState.RightTurn
        self.writeCmd(BotServos.RightWheel, 4600)
        self.stop()

# END
