# key_bindings.py

import tkinter as tk
from .tango_bot import TangBotController
from .log import log
import threading, sys

class KeyBindings:

    # properties
    win:tk.Tk                   = None
    bot:TangBotController       = None

    # constructor
    def __init__(self, bot:TangBotController):
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
        self.win.bind('<m>', self.speed)        # key code: 74
        self.win.bind('<j>', self.speed)        # key code: 75
        self.win.bind('<k>', self.speed)        # key code: 76
        self.win.bind('<l>', self.speed)        # key code: 77

        def run(win:tk.Tk):
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

    def arrows(self, event=None):
        keycode = event.keycode
        if keycode == 111:
            log.debug('Key Pressed: "%s"', 'Up')
            self.bot.increaseWheelSpeed()
        elif keycode == 116:
            log.debug('Key Pressed: "%s"', 'Down')
            self.bot.decreaseWheelSpeed()
        elif keycode == 113:
            log.debug('Key Pressed: "%s"', 'Left')
        elif keycode == 114:
            log.debug('Key Pressed: "%s"', 'Right')

    def waist(self, event=None):
        keycode = event.keycode
        if keycode == 52:
            log.debug('Key Pressed: "%s"', '<Z>')
            self.bot.moveWaistLeft()
        elif keycode == 54:
            log.debug('Key Pressed: "%s"', '<C>')
            self.bot.moveWaistRight()

    def head(self, event=None):
        keycode = event.keycode
        if keycode == 25:
            log.debug('Key Pressed: "%s"', '<W>')
            self.bot.moveHeadUp()
        elif keycode == 39:
            log.debug('Key Pressed: "%s"', '<S>')
            self.bot.moveHeadDown()
        elif keycode == 38:
            log.debug('Key Pressed: "%s"', '<A>')
            self.bot.moveHeadLeft()
        elif keycode == 40:
            log.debug('Key Pressed: "%s"', '<D>')
            self.bot.moveHeadRight()

    def speed(self, event):
        keycode = event.keycode
        if keycode == 74:
            log.debug('Key Pressed: "%s"', '<j>')
            self.bot.SPEED = 400
        if keycode == 75:
            log.debug('Key Pressed: "%s"', '<k>')
            self.bot.SPEED = 200
        if keycode == 76:
            log.debug('Key Pressed: "%s"', '<l>')
            self.bot.SPEED = 100
        if keycode == 77:
            log.debug('Key Pressed: "%s"', '<m>')
            self.bot.stop()


# END
