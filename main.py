"""
River Kelly
Alex Fischer
Kyler Gappa
CSCI-455: Embedded Systems (Robotics)
Spring 2022
"""

import sys
import argparse
from src import Speech2Text
from src import TkinterApp
from src import TangBotController
from src import Dialog


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Tango Bots')
    parser.add_argument('app', help='Application', type=str, choices=['tkinter-app', 'speech2text', 'dialog'])
    args = parser.parse_args()

    bot = TangBotController()

    if args.app == 'speech2text':
        s2t = Speech2Text(bot)
        s2t.start()
    elif args.app == 'tkinter-app':
        tk_app = TkinterApp(bot)
        tk_app.update_idletasks()
        tk_app.update()
        tk_app.mainloop()
    elif args.app == 'dialog':
        dialog = Dialog()
        try:
            dialog.run()
        except KeyboardInterrupt:
            pass

# END main.py
