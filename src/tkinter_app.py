# tkinter_app

import tkinter as tk
from tkinter import ttk
from .tango_bot import TangBotController
from .log import log

KEY_BINDING_DICTIONARY = {
    '<Up>': 'increaseWheelSpeed',
    '<Down>': 'decreaseWheelSpeed',
    '<Left>': 'turnLeft',
    '<Right>': 'turnRight',
    '<q>': 'stop',
    '<w>': 'moveHeadUp',
    '<s>': 'moveHeadDown',
    '<a>': 'moveHeadLeft',
    '<d>': 'moveHeadRight',
    '<z>': 'moveWaistLeft',
    '<x>': 'centerWaist',
    '<c>': 'moveWaistRight',
    '<j>': 'setSpeedLevelOne',
    '<k>': 'setSpeedLevelTwo',
    '<l>': 'setSpeedLevelThree'
}

# makeKeyBindingFnc() - Helper function for key binding
# This helps in binding keys command callbacks directly to
def makeKeyBindingFnc(bot_attr):
    def fnc(event: tk.Event):
        log.debug('Key Pressed: "%s"', event.keysym)
        bot_attr()
    return fnc

class App(tk.Tk):

    bot: TangBotController

    # constructor
    def __init__(self, bot: TangBotController):
        super().__init__()
        self.bot = bot
        # title
        self.title('Tango Bot')
        # ttk styles
        self.style = ttk.Style(self)
        # root style determines the appearance of all widgets.
        self.style.configure('.', font=('Helvetica', 12))
        # key bindings
        self.__setup_key_bindings()


    def stop(self, event: tk.Event = None):
        try:
            self.destroy()
        except tk.TclError as err:
            print(err)
        self.bot.stop()

    """ Key Bindings
        Instead of having internal methods for the key bindings,
        the following loop binds the key bindings directly to
        TangBotController class atrributes.

        See: KEY_BINDING_DICTIONARY for further specs
    """
    def __setup_key_bindings(self):
        # bind space bar to quit the tkinter app
        self.bind('<space>', self.stop)
        # loop through KEY_BINDING_DICTIONARY
        for index, (key, value) in enumerate(KEY_BINDING_DICTIONARY.items()):
            # check if TangBotController class has the attribute
            if hasattr(self.bot, value):
                # get the TangBotController class attribute
                bot_fnc = getattr(self.bot, value)
                # bind the key directly to the TangBotController attribute (method)
                self.bind(key, makeKeyBindingFnc(bot_fnc))
            else:
                # TangBotController class attribute does not exist, show warning error
                log.warn("Could not bind key to TangBotController class method.\n Key: '%s'\n Method: '%s'\n", key, value)

# END
