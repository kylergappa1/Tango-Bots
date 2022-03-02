# tango_bot.py

from .usb import serial, getUSB
from .log import log

class TangBotController:

    # properties
    usb : serial.Serial = None
    cmd = None

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

# END
