# usb.py

import serial
from .log import log

def getUSB():
    usb = None
    usb_name = '/dev/ttyACM0'
    try:
        usb = serial.Serial(usb_name)
    except:
        log.debug('Unable to get USD: %s', usb_name)
        usb = None
    if usb is None:
        usb_name = '/dev/ttyACM1'
        try:
            usb = serial.Serial(usb_name)
        except:
            log.debug('Unable to get USD: %s', usb_name)
            usb = None
    if usb is not None:
        log.info('USB:\n- name: "%s"\n- baudrate: "%s"', usb.name, usb.baudrate)
    else:
        log.critical('Unable to get USB Serial')
    # return usb (serial)
    return usb

# END
