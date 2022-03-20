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
from src import App
from src import TangBotController


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Tango Bots')
    parser.add_argument('app', help='Application', type=str, choices=['tkinter-app', 'speech2text'])
    args = parser.parse_args()

    bot = TangBotController()

    if args.app == 'speech2text':
        s2t = Speech2Text(bot)
        s2t.start()
    elif args.app == 'tkinter-app':
        tk_app = App(bot)
        tk_app.mainloop()

# END main.py
