from geometry import origin


class Thruster:
    def __init__(self, name, location=origin):
        active = False
        self.name = name
        self.location = location
        self.thrustDirection = [-l / 1000 for l in location]


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
