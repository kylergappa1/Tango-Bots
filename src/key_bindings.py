# key_bindings.py

import sys
import threading
import tkinter as tk

from .log import log
from .tango_bot import TangBotController


class KeyBindings:

    # properties
    win: tk.Tk                   = None
    bot: TangBotController       = None

    # constructor
    def __init__(self, bot: TangBotController):
        self.bot = bot
        self.win = tk.Tk()
        # setup keybindings
        self.win.bind('<Up>', self.arrows)      # key code: 111
        self.win.bind('<Down>', self.arrows)    # key code: 116
        self.win.bind('<Left>', self.arrows)    # key code: 113
        self.win.bind('<Right>', self.arrows)   # key code: 114
        self.win.bind('<space>', self.stop)     # key code: 65
        self.win.bind('<w>', self.head)         # key code: 25
        self.win.bind('<s>', self.head)         # key code: 39
        self.win.bind('<a>', self.head)         # key code: 38
        self.win.bind('<d>', self.head)         # key code: 40
        self.win.bind('<z>', self.waist)        # key code: 52
        self.win.bind('<c>', self.waist)        # key code: 54
        self.win.bind('<x>', self.waist)        # key code: 54
        self.win.bind('<m>', self.speed)        # key code: 58
        self.win.bind('<j>', self.speed)        # key code: 44
        self.win.bind('<k>', self.speed)        # key code: 45
        self.win.bind('<l>', self.speed)        # key code: 46
        self.win.bind('<q>', self.stopRobot)

        def run(win: tk.Tk):
            try:
                win.mainloop()
            except RuntimeError:
                log.debug('Calling Tcl from different apartment')

        self.thread = threading.Thread(name="KeyBindings", target=run, args=[self.win], daemon=True)

    def stop(self, event=None):
        try:
            self.win.destroy()
            log.debug('KeyBindings: tkinter window destroyed.')
        except tk.TclError:
            log.debug('KeyBindings::stop() - Can\'t invoke "destroy" command: application has been destroyed')
        self.bot.stop()
        sys.exit(0)

    def stopRobot(self, event):
        if event.char == 'q':
            log.debug('Key Pressed: "%s"', 'Q')
            self.bot.stopMoving()

    def arrows(self, event=None):
        if event.keycode == 111:
            log.debug('Key Pressed: "%s"', 'Up')
            self.bot.increaseWheelSpeed()
        elif event.keycode == 116:
            log.debug('Key Pressed: "%s"', 'Down')
            self.bot.decreaseWheelSpeed()
        elif event.keycode == 113:
            log.debug('Key Pressed: "%s"', 'Left')
            self.bot.turnLeft()
        elif event.keycode == 114:
            log.debug('Key Pressed: "%s"', 'Right')
            self.bot.turnRight()

    def waist(self, event=None):
        if event.char == 'z':
            log.debug('Key Pressed: "%s"', '<Z>')
            self.bot.moveWaistLeft()
        elif event.char == 'c':
            log.debug('Key Pressed: "%s"', '<C>')
            self.bot.moveWaistRight()
        elif event.char == 'x':
            log.debug('Key Pressed: "%s"', '<x>')
            self.bot.centerWaist()

    def head(self, event=None):
        if event.char == 'w':
            log.debug('Key Pressed: "%s"', '<W>')
            self.bot.moveHeadUp()
        elif event.char == 's':
            log.debug('Key Pressed: "%s"', '<S>')
            self.bot.moveHeadDown()
        elif event.char == 'a':
            log.debug('Key Pressed: "%s"', '<A>')
            self.bot.moveHeadLeft()
        elif event.char == 'd':
            log.debug('Key Pressed: "%s"', '<D>')
            self.bot.moveHeadRight()

    def speed(self, event=None):
        if event.char == 'j':
            log.debug('Key Pressed: "%s"', '<j>')
            self.bot.setSpeed(100)
        elif event.char == 'k':
            log.debug('Key Pressed: "%s"', '<k>')
            self.bot.setSpeed(500)
        elif event.char == 'l':
            log.debug('Key Pressed: "%s"', '<l>')
            self.bot.setSpeed(800)
        elif event.char == 'm':
            log.debug('Key Pressed: "%s"', '<m>')
            self.bot.stopMoving()


# END
