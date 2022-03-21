# tkinter_app

import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
from turtle import down
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


class HeadControlsFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)

        up_button = ttk.Button(self, text="Up")
        up_button.grid(column=1, row=0)

        down_button = ttk.Button(self, text="Down")
        down_button.grid(column=1,row=2)

        left_button = ttk.Button(self, text="Left")
        left_button.grid(column=0, row=1)

        right_button = ttk.Button(self, text="Right")
        right_button.grid(column=2, row=1)

        center_button = ttk.Button(self, text="Center")
        center_button.grid(column=1, row=1)

class WaistControlsFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)

        left_button = ttk.Button(self, text="Left")
        left_button.grid(column=0, row=1)

        right_button = ttk.Button(self, text="Right")
        right_button.grid(column=2, row=1)

        center_button = ttk.Button(self, text="Center")
        center_button.grid(column=1, row=1)

class MainFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        options = {'padx': 5, 'pady': 5}
        # label
        # self.label = ttk.Label(self, text='Head')
        # self.label.pack(**options)
        # button
        # self.button = ttk.Button(self, text='Click Me')
        # self.button['command'] = self.button_clicked
        # self.button.pack(**options)

        head_ctrl_con = ttk.Frame(self)
        head_ctrl_label = ttk.Label(head_ctrl_con, text='Head')
        head_ctrl_label.grid(column=0, row=0, sticky=tk.W)
        head_ctrl_frame = HeadControlsFrame(head_ctrl_con)
        head_ctrl_frame.grid(column=0, row=1)
        head_ctrl_con.grid(column=0, row=0)


        waist_ctrl_con = ttk.Frame(self)
        waist_ctrl_label = ttk.Label(waist_ctrl_con, text='Waist')
        waist_ctrl_label.grid(column=0, row=0, sticky=tk.W)
        waist_ctrl_frame = WaistControlsFrame(waist_ctrl_con)
        waist_ctrl_frame.grid(column=0, row=1)
        waist_ctrl_con.grid(column=0, row=1)

        # show the frame on the container
        self.pack(**options)

    def button_clicked(self):
        showinfo(title='Information',
                 message='Hello, Tkinter!')

class TkinterApp(tk.Tk):

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
        # main frame
        self.main_frame = MainFrame(self)

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
