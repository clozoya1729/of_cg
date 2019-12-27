import numpy as np
from scipy.spatial.transform import Rotation as R

from geometry import origin, Coordinate

r = R.from_quat([0, 0, np.sin(np.pi / 4), np.cos(np.pi / 4)])


class Thruster:
    def __init__(self, name, location=origin):
        active = False
        self.name = name
        self.location = Coordinate(*location)
        self.thrustForce = 1 / 1000

    @property
    def thrustDirection(self):
        f = self.face
        if f == 'lfc':
            return 0, 0, 0 - self.thrustForce
        if f == 'rbc':
            return 0, 0, 0 - self.thrustForce
        if f == 'lbc':
            return 0, 0, self.thrustForce
        if f == 'rfc':
            return 0, 0, self.thrustForce
        return 0, 0, 0

    @property
    def face(self):
        x, y, z = self.location.as_list()
        if x > 0:
            cx = 'r'
        elif x < 0:
            cx = 'l'
        else:
            cx = 'c'
        if y > 0:
            cy = 'f'
        elif y < 0:
            cy = 'b'
        else:
            cy = 'c'
        if z > 0:
            cz = 'u'
        elif z < 0:
            cz = 'd'
        else:
            cz = 'c'
        return '{}{}{}'.format(cx, cy, cz)


configurations = {
    '1u-1d-z-4': [Thruster('rf', [0.5, 0.25, 0]),
                  Thruster('rb', [0.5, -0.25, 0]),
                  Thruster('lf', [-0.5, 0.25, 0]),
                  Thruster('lb', [-0.5, -0.25, 0])],
    '1u-2d-xy-4': [Thruster('rf', [0.25, 0.25, -0.5]),
                   Thruster('rb', [0.25, -0.25, -0.5]),
                   Thruster('lf', [-0.25, 0.25, -0.5]),
                   Thruster('lb', [-0.25, -0.25, -0.5])]
}
