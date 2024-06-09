import keyboard
from time import sleep

to_exit = False
while not to_exit:
    keyboard.on_press_key("return", lambda _: globals().update(to_exit=True))
    print("loop")
    sleep(0.1)

print("success")
