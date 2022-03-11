import pynput,time

from pynput.keyboard import Key,Controller

keyboard = Controller()

while 1==1:
    keyboard.press(Key.ctrl)
    keyboard.release(Key.ctrl)
    time.sleep(180)

