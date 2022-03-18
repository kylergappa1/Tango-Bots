# tkinter_app

import tkinter as tk
from tkinter import ttk

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

def makeKeyBindingFnc(fnc_name: str):
    def fnc(event: tk.Event):
        key = event.keysym
        print("Key Pressed: {} - {}".format(key, fnc_name))
    return fnc

class App(tk.Tk):

    # constructor
    def __init__(self):
        super().__init__()

        # title
        self.title('Tango Bot')

        # ttk styles
        self.style = ttk.Style(self)
        # root style determines the appearance of all widgets.
        self.style.configure('.', font=('Helvetica', 12))

        # bind keys
        for index, (key, value) in enumerate(KEY_BINDING_DICTIONARY.items()):
            self.bind(key, makeKeyBindingFnc(value))

    

# END
