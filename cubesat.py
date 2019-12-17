import random

from math_util import rotate_point


class CubeSat:
    origin = [0, 0, 0]
    _angularVelocity = {
        'x': 0.0,
        'y': 0.0,
        'z': 0.0,
    }
    faces = {
        'up': ['lfu', 'rfu', 'rbu', 'lbu', 'lfu'],
        'down': ['lfd', 'rfd', 'rbd', 'lbd', 'lfd'],
        'left': ['lfu', 'lfd', 'lbd', 'lbu', 'lfu'],
        'right': ['rfu', 'rfd', 'rbd', 'rbu', 'rfu'],
        'back': ['lbu', 'rbu', 'rbd', 'lbd', 'lbu'],
        'front': ['lfu', 'rfu', 'rfd', 'lfd', 'lfu'],
    }

    d = {
        '-0': 'lf',
        '-1': 'rf',
        '0': 'rb',
        '1': 'lb',
    }

    activeThruster = None
    activeThrusterCounter = 0
    activeThrusterCounterMaximum = 10

    def __init__(self, dimensions=(1, 1, 1), mass=1, randomInit=False):
        '''
        r=right, l=left, f=front, b=back, u=up, d=down
        '''
        if randomInit:
            self._angularVelocity = {
                'x': 0.1 + random.randint(-2, 1) / 5,
                'y':  random.randint(-2, 1) / 5,
                'z': 0  # random.randint(-1, 1) / 10,
            }
        x = dimensions[0] / 2
        y = dimensions[1] / 2
        z = dimensions[2] / 2
        self._vertices = {
            'rfu': [x, y, z],
            'rbu': [x, -y, z],
            'rfd': [x, y, -z],
            'rbd': [x, -y, -z],

            'lfu': [-x, y, z],
            'lbu': [-x, -y, z],
            'lfd': [-x, y, -z],
            'lbd': [-x, -y, -z],
        }

        self.thrusters = {
            'rf': [x / 2, y / 2, -z],
            'rb': [x / 2, -y / 2, -z],
            'lf': [-x / 2, y / 2, -z],
            'lb': [-x / 2, -y / 2, -z],
        }
        self.unitThrustForce = mass

        self.thrustDirections = {
            'rf': (0.01 * self.unitThrustForce,
                   0.01 * self.unitThrustForce,
                   0 * self.unitThrustForce),
            'rb': (-0.01 * self.unitThrustForce,
                   0.01 * self.unitThrustForce,
                   0 * self.unitThrustForce),
            'lf': (0.01 * self.unitThrustForce,
                   -0.01 * self.unitThrustForce,
                   0 * self.unitThrustForce),
            'lb': (-0.01 * self.unitThrustForce,
                   -0.01 * self.unitThrustForce,
                   0 * self.unitThrustForce),
        }

    @property
    def vertices(self):
        return [self._vertices[v] for v in self._vertices]

    @property
    def splitVertices(self):
        v = self.vertices
        return [c[0] for c in v], [c[1] for c in v], [c[2] for c in v]

    def wire_frame(self, face):
        v = self._vertices
        w = ([v[point] for point in self.faces[face]])
        return [c[0] for c in w], [c[1] for c in w], [c[2] for c in w]

    @property
    def angularVelocityComponents(self):
        return self._angularVelocity['x'], self._angularVelocity['y'], self._angularVelocity['z']

    @property
    def avc(self):
        return self.angularVelocityComponents

    def apply_thrust(self, thruster):
        self.activeThruster = thruster
        x, y, z = self.thrustDirections[thruster]
        x, y, z = x * self.unitThrustForce, y * self.unitThrustForce, z * self.unitThrustForce
        self._angularVelocity['x'] = round(self._angularVelocity['x'] + x , 5)
        self._angularVelocity['y'] = round(self._angularVelocity['y'] + y, 5)
        self._angularVelocity['z'] += round(self._angularVelocity['z'] + z, 5)

    def print_info(self):
        print(self.activeThruster,
              self._angularVelocity['x'],
              self._angularVelocity['y'],
              self._angularVelocity['z'])

    def rotate(self):
        ox, oy, oz = self.origin
        aX, aY, aZ = self.avc
        for name, prop in [('_vertices', self._vertices), ('thrusters', self.thrusters)]:
            results = {}
            for k in prop:
                px, py, pz = prop[k]
                qx, qy = rotate_point(aZ, ox, oy, px, py) # rotate about z-axis
                qy, qz = rotate_point(aX, oy, oz, py, pz)  # rotate about x-axis
                qx, qz = rotate_point(aY, ox, oz, px, qz) # rotate about y-axis
                results[k] = [qx, qy, qz]
            setattr(self, name, results)
        if self.activeThruster != None:
            self.activeThrusterCounter += 1
            if self.activeThrusterCounter > self.activeThrusterCounterMaximum:
                self.activeThrusterCounter = 0
                self.activeThruster = None

    @property
    def atc(self):
        return self.activeThrusterCounter

    @property
    def atcm(self):
        return self.activeThrusterCounterMaximum


    @property
    def verts(self):
        v = []
        for face in self.faces:
            res = []
            for vertex in self._vertices:
                res.append(self._vertices[vertex])
            v.append(res)
        rfu = self._vertices['rfu']
        lfu = self._vertices['lfu']
        rbu = self._vertices['rbu']
        lbu = self._vertices['lbu']
        rfd = self._vertices['rfd']
        lfd = self._vertices['lfd']
        rbd = self._vertices['rbd']
        lbd = self._vertices['lbd']
        v = [
            [lfu, rfu, rbu, lbu],
            [lfd, rfd, rbd, lbd],
            [rfu, rfd, rbd, rbu],
            [lfu, lfd, lbd, lbu],
            [lfu, rfu, rfd, lfd],
            [lbu, rbu, rbd, lbd]
        ]
        return v

    def decide(self):
        avc = self.avc
        if avc != (0, 0, 0):
            setsd = [abs(_) for _ in avc]
            criticalIndex = setsd.index(max(setsd))
            criticalValue = avc[criticalIndex]
            decision = str('{}{}'.format('-' if criticalValue < 0 else '', criticalIndex))
            self.apply_thrust(self.d[decision])
