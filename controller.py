import time

import keyboard


def check_press(cube):
    if keyboard.is_pressed('q'):
        cube.apply_thrust('lf')
        time.sleep(0.025)
    if keyboard.is_pressed('w'):
        cube.apply_thrust('rf')
        time.sleep(0.025)
    if keyboard.is_pressed('e'):
        cube.apply_thrust('lb')
        time.sleep(0.025)
    if keyboard.is_pressed('r'):
        cube.apply_thrust('rb')
        time.sleep(0.025)
    if keyboard.is_pressed('i'):
        cube.decide()


print("Use Keyboard to apply thrust for rotation:\n"
      "Q: Left-Front\n"
      "W: Right-Front\n"
      "E: Left-Back\n"
      "R: Right-Back\n"
      "I: Automatic")

