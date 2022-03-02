# key_bindings.py

import tkinter as tk
from .tango_bot import TangBotController

class KeyBindings:

    # properties
    win : tk.Tk = None
    bot: TangBotController = None

    # constructor
    def __init__(self, bot:TangBotController):
        self.bot = bot
        self.win = tk.Tk()
        # setup keybindings
        self.win.bind('<Up>', self.arrows)   # key code: 111
        self.win.bind('<Down>', self.arrows) # key code: 116
        self.win.bind('<Left>', self.arrows) # key code: 113
        self.win.bind('<Right>', self.arrows) # key code: 114
        self.win.bind('<space>', self.stop) # key code: 65
        self.win.bind('<w>', self.head) # key code: 25
        self.win.bind('<s>', self.head) # key code: 39
        self.win.bind('<a>', self.head) # key code: 38
        self.win.bind('<d>', self.head) # key code: 40
        self.win.bind('<z>', self.waist) # key code: 52
        self.win.bind('<c>', self.waist) # key code: 54
        # start tkinter window
        self.win.mainloop()

    def arrows(self, event):
        keycode = event.keycode
        if keycode == 111:
            print("Up Arrow")
        elif keycode == 116:
            print("Down Arrow")
        elif keycode == 113:
            print("Left Arrow")
        elif keycode == 114:
            print("Right Arrow")

    def waist(self, event):
        keycode = event.keycode
        if keycode == 52:
            print("Z (Left)")
        elif keycode == 54:
            print("C (Right)")

    def head(self, event):
        keycode = event.keycode
        if keycode == 25:
            print("Head Up")
        elif keycode == 39:
            print("Head Down")
        elif keycode == 38:
            print("Head Left")
        elif keycode == 40:
            print("Head Right")

    def stop(self, event=None):
        self.win.destroy()

# END
