# key_bindings.py

import tkinter as tk
from .tango_bot import TangBotController
from .log import log

class KeyBindings:

    # properties
    win : tk.Tk = None
    bot: TangBotController = None

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
        self.win.bind('<1>', self.speed)        # key code: 49
        self.win.bind('<2>', self.speed)        # key code: 50
        self.win.bind('<3>', self.speed)        # key code: 51
        # start tkinter window
        self.win.mainloop()

    def arrows(self, event):
        keycode = event.keycode
        if keycode == 111:
            log.debug('Key Pressed: "%s"', 'Up')
        elif keycode == 116:
            log.debug('Key Pressed: "%s"', 'Down')
        elif keycode == 113:
            log.debug('Key Pressed: "%s"', 'Left')
        elif keycode == 114:
            log.debug('Key Pressed: "%s"', 'Right')

    def waist(self, event):
        keycode = event.keycode
        if keycode == 52:
            log.debug('Key Pressed: "%s"', '<Z>')
            self.bot.moveWaistLeft()
        elif keycode == 54:
            log.debug('Key Pressed: "%s"', '<C>')
            self.bot.moveWaistRight()

    def head(self, event):
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
        if keycode == 51:
            log.debug('Key Pressed: "%s"', '<1>')
            self.bot.SPEED = 400
        if keycode == 50:
            log.debug('Key Pressed: "%s"', '<2>')
            self.bot.SPEED = 200
        if keycode == 49:
            log.debug('Key Pressed: "%s"', '<3>')
            self.bot.SPEED = 100

    def stop(self, event=None):
        self.win.destroy()

# END
