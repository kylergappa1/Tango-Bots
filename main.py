"""
River Kelly
Alex Fischer
Kyler Gappa
CSCI-455: Embedded Systems (Robotics)
Spring 2022
"""

import argparse
from src import Speech2Text
from src import RunTkinterApp
from src import TangBotController
from src import Dialog

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Tango Bots')
    parser.add_argument('app', help='Application', type=str, choices=['gui', 'speech2text', 'dialog', 'game'])
    args = parser.parse_args()
    if args.app == 'speech2text':
        bot = TangBotController()
        s2t = Speech2Text(bot)
        s2t.start()
    elif args.app == 'gui':
        RunTkinterApp()
    elif args.app == 'dialog':
        dialog = Dialog()
        try:
            dialog.run()
        except KeyboardInterrupt:
            pass

# END main.py
