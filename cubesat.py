from geometry import Cube, unitDims, origin


class CubeSat(Cube):
    d = {
        '-0': 'lf',
        '-1': 'rf',
        '0': 'rb',
        '1': 'lb',
    }
    activeThruster = None
    activeThrusterCounter = 0
    activeThrusterCounterMaximum = 10

    def __init__(self, dimensions=unitDims, centroid=origin, mass=1, thrusters=None, randomAV=False):
        super(CubeSat, self).__init__(dimensions, centroid, mass, randomAV)
        x = dimensions[0] / 2
        y = dimensions[1] / 2
        z = dimensions[2] / 2
        self.thrusters = {thruster.name: thruster for thruster in thrusters}
        self.unitThrustForce = mass

    def apply_thrust(self, thruster):
        self.activeThruster = thruster
        x, y, z = self.thrusters[thruster].thrustDirection
        x, y, z = x * self.unitThrustForce, y * self.unitThrustForce, z * self.unitThrustForce
        self._angularVelocity['x'] = round(self._angularVelocity['x'] + x, 5)
        self._angularVelocity['y'] = round(self._angularVelocity['y'] + y, 5)
        self._angularVelocity['z'] += round(self._angularVelocity['z'] + z, 5)

    def decide(self):
        avc = self.avc
        if avc != (0, 0, 0):
            setsd = [abs(_) for _ in avc]
            criticalIndex = setsd.index(max(setsd))
            criticalValue = avc[criticalIndex]
            decision = str('{}{}'.format('-' if criticalValue < 0 else '', criticalIndex))
            self.apply_thrust(self.d[decision])

    @property
    def atc(self):
        return self.activeThrusterCounter

    @property
    def atcm(self):
        return self.activeThrusterCounterMaximum

    def print_info(self):
        print(self.activeThruster,
              self._angularVelocity['x'],
              self._angularVelocity['y'],
              self._angularVelocity['z'])
