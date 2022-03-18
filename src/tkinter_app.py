# tkinter_app

from pyclbr import Function
import tkinter as tk
from tkinter import ttk
from .tango_bot import TangBotController

KEY_BINDING_DICTIONARY = {
    '<Up>': 'increaseWheelSpeed',
    '<Down>': 'decreaseWheelSpeed',
    '<Left>': 'turnLeft',
    '<Right>': 'turnRight',
    '<q>': 'stopMoving',
    '<w>': 'moveHeadUp',
    '<s>': 'moveHeadDown',
    '<a>': 'moveHeadLeft',
    '<d>': 'moveHeadRight',
    '<z>': 'moveWaistLeft',
    '<x>': 'centerWaist',
    '<c>': 'moveWaistRight',
}

def makeKeyBindingFnc(fnc_name: str, bot_attr: Function):
    def fnc(event: tk.Event):
        key = event.keysym
        print("Key Pressed: {} - {}".format(key, fnc_name))
        bot_attr()
    return fnc

class App(tk.Tk):

    bot: TangBotController

    # constructor
    def __init__(self):
        super().__init__()

        self.bot = TangBotController()

        # title
        self.title('Tango Bot')

        # ttk styles
        self.style = ttk.Style(self)
        # root style determines the appearance of all widgets.
        self.style.configure('.', font=('Helvetica', 12))

        # bind keys
        for index, (key, value) in enumerate(KEY_BINDING_DICTIONARY.items()):
            if hasattr(self.bot, value):
                bot_fnc = getattr(self.bot, value)
                self.bind(key, makeKeyBindingFnc(value, bot_fnc))
            else:
                print("Error: Bot does not have attribute '{}' for key binding '{}'".format(value, key))
            # self.bind(key, makeKeyBindingFnc(value, self.bot))

        self.bind('<space>', self.stop)

    def stop(self, event: tk.Event = None):
        try:
            self.destroy()
        except tk.TclError as err:
            print(err)
        self.bot.stop()

# END
