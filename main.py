"""
River Kelly
Alex Fischer
Kyler Gappa
CSCI-455: Embedded Systems (Robotics)
Spring 2022
"""

import sys

from src import KeyBindings, TangBotController

botController = None
keyBindings = None

botController = TangBotController()
keyBindings = KeyBindings(botController)
keyBindings.thread.start()

while True:
    input = input('Press "q" to quit > ')
    if input != "q":
        continue
    keyBindings.stop()
    if keyBindings.thread:
        keyBindings.thread.join()
    break
sys.exit(0)

# END main.py
