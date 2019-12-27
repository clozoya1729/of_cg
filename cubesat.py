from geometry import Cube, origin


class CubeSat(Cube):
    d = {
        '-2': 'lb',
        '-1': 'rf',
        '-0': 'lf',
        '0': 'rb',
        '1': 'lb',
        '2': 'rb'
    }
    activeThruster = None
    activeThrusterCounter = 0
    activeThrusterCounterMaximum = 10

    def __init__(self, dimension=1, centroid=origin, mass=1, thrusters=None, randomAV=False):
        super(CubeSat, self).__init__(dimension, centroid, mass, randomAV)
        self.thrusters = {thruster.name: thruster for thruster in thrusters}

    def apply_thrust(self, thruster):
        self.activeThruster = thruster
        x, y, z = self.thrusters[thruster].thrustDirection
        self._angularVelocity.x = round(self._angularVelocity.x + x, 5)
        self._angularVelocity.y = round(self._angularVelocity.y + y, 5)
        self._angularVelocity.z += round(self._angularVelocity.z + z, 5)

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
