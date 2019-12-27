import keyboard
import numpy as np


class Controller:
    timer = 0
    timeout = 0

    def check_press(self, cube, graphics):
        if self.timeout == 0:
            if keyboard.is_pressed('q'):
                self.timeout = 15
                cube.apply_thrust('lf')
            if keyboard.is_pressed('w'):
                self.timeout = 15
                cube.apply_thrust('rf')
            if keyboard.is_pressed('e'):
                self.timeout = 15
                cube.apply_thrust('lb')
            if keyboard.is_pressed('r'):
                self.timeout = 15
                cube.apply_thrust('rb')
            if keyboard.is_pressed('i'):
                self.timeout = 15
                cube.decide()

            if keyboard.is_pressed('v'):
                self.timeout = 15
                if graphics['displayWireframe']:
                    graphics['displayWireframe'] = False
                    for face in graphics['faces']:
                        graphics['faces'][face].set_data(0, 0)
                        graphics['faces'][face].set_3d_properties(0)
                else:
                    graphics['displayWireframe'] = True

            if keyboard.is_pressed('b'):
                self.timeout = 15
                if graphics['displayBody'] == True:
                    graphics['displayBody'] = False
                    graphics['poly'].set_verts([])
                else:
                    graphics['displayBody'] = True

            if keyboard.is_pressed('n'):
                self.timeout = 15
                if graphics['displayQuiver']:
                    graphics['displayQuiver'] = False
                    graphics['bodyQuiverNegative'].remove()
                    graphics['bodyQuiverPositive'].remove()

                else:
                    graphics['displayQuiver'] = True
                    x, y, z, u, v, w, nu, nv, nw = cube.quiver
                    graphics['bodyQuiverNegative'] = graphics['ax'].quiver(x, y, z, u, v, w,
                                                                           arrow_length_ratio=0.15,
                                                                           color='blue', lw=0.5, zorder=-100)
                    graphics['bodyQuiverPositive'] = graphics['ax'].quiver(x, y, z, nu, nv, nw,
                                                                           arrow_length_ratio=0.15,
                                                                           color='red', lw=0.5, zorder=-100)

            if keyboard.is_pressed('x'):
                self.timeout = 15
                if graphics['displayAV']:
                    graphics['displayAV'] = False
                    graphics['avText'].set_text('')
                else:
                    graphics['displayAV'] = True

            if keyboard.is_pressed('z'):
                self.timeout = 15
                if graphics['displayAxes']:
                    graphics['displayAxes'] = False
                    graphics['axesNegative'].remove()
                    graphics['axesPositive'].remove()
                else:
                    graphics['displayAxes'] = True
                    x, y, z = np.zeros((3, 3))
                    u, v, w = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
                    graphics['axesPositive'] = graphics['ax'].quiver(x, y, z, u, v, w, arrow_length_ratio=0.1,
                                                                     color='green',
                                                                     lw=0.75,
                                                                     linestyle='--')
                    u, v, w = np.array([[-1, 0, 0], [0, -1, 0], [0, 0, -1]])
                    graphics['axesNegative'] = graphics['ax'].quiver(x, y, z, u, v, w, arrow_length_ratio=0.1,
                                                                     color='orangered', lw=0.75,
                                                                     linestyle='--')
        self.timer += 1
        if self.timer > self.timeout:
            self.timer = 0
            self.timeout = 0


print("Use Keyboard to apply thrust for rotation:\n"
      "Q: Left-Front\n"
      "W: Right-Front\n"
      "E: Left-Back\n"
      "R: Right-Back\n"
      "I: Automatic")
