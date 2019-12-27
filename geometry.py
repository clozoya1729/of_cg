import random
from math import cos, sin, sqrt

origin = [0, 0, 0]
unitDims = [1, 1, 1]


class Coordinate:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.high = 2
        self.current = -1

    def as_list(self):
        return self.x, self.y, self.z

    # def __iter__(self):
    #     return self
    #
    # def __next__(self):
    #     self.current += 1
    #     if self.current <= self.high:
    #         return self.as_list()[self.current]
    #     self.current = -1
    #     return StopIteration


class Quaternion:
    def __init__(self, w, x=0, y=0, z=0):
        self.w = w
        self.x = x
        self.y = y
        self.z = z
        if w == 'random':
            self.w = 0
            self.x = 0.1 + random.randint(-2, 1) / 50
            self.y = random.randint(-2, 1) / 50
            self.z = random.randint(-2, 1) / 50

    def __add__(self, other):
        return Quaternion(self.w + other.w,
                          self.x + other.x,
                          self.y + other.y,
                          self.z + other.z)

    def __mul__(self, other):
        return ''

    @property
    def norm(self):
        return sqrt(self.w ** 2 + self.x ** 2 + self.y ** 2 + self.z ** 2)


def spin(q, w):
    return 0.5 * w * q


class Cube:
    _angularVelocity = Quaternion(0, 0, 0, 0)
    faces = {
        'up': ['lfu', 'rfu', 'rbu', 'lbu', 'lfu'],
        'down': ['lfd', 'rfd', 'rbd', 'lbd', 'lfd'],
        'left': ['lfu', 'lfd', 'lbd', 'lbu', 'lfu'],
        'right': ['rfu', 'rfd', 'rbd', 'rbu', 'rfu'],
        'back': ['lbu', 'rbu', 'rbd', 'lbd', 'lbu'],
        'front': ['lfu', 'rfu', 'rfd', 'lfd', 'lfu'],
    }

    def __init__(self, dimension=1, centroid=origin, mass=1, randomAV=False):
        '''
        r=right, l=left, f=front, b=back, u=up, d=down
        '''
        x = dimension / 2
        y = dimension / 2
        z = dimension / 2
        self.dimension = dimension
        self.centroid = centroid
        self.mass = mass
        if randomAV:
            self._angularVelocity = Quaternion('random')

        self._vertices = {
            'rfu': Coordinate(x, y, z),
            'rbu': Coordinate(x, -y, z),
            'rfd': Coordinate(x, y, -z),
            'rbd': Coordinate(x, -y, -z),
            'lfu': Coordinate(-x, y, z),
            'lbu': Coordinate(-x, -y, z),
            'lfd': Coordinate(-x, y, -z),
            'lbd': Coordinate(-x, -y, -z),
        }
        r = self.dimension / 4
        self.quiverP = [[r, 0, 0], [0, r, 0], [0, 0, r]]
        self.quiverN = [[-r, 0, 0], [0, -r, 0], [0, 0, -r]]

    @property
    def inertia(self):
        return (1 / 6) * self.mass * (self.dimension ** 2)

    @property
    def vertices(self):
        return [self._vertices[v] for v in self._vertices]

    def wf(self, face):
        """
        Wire Frame
        face: str
        return:
        """
        v = self._vertices
        w = ([v[point] for point in self.faces[face]])
        return [c.x for c in w], [c.y for c in w], [c.z for c in w]

    @property
    def avc(self):
        """
        Angular Velocity Components
        return: list of float - [x, y, z]
        """
        return self._angularVelocity.x, self._angularVelocity.y, self._angularVelocity.z

    def rotate(self):
        ox, oy, oz = self.centroid
        aX, aY, aZ = self.avc
        for name, prop in [('_vertices', self._vertices)]:
            results = {}
            for k in prop:
                c = prop[k]
                px, py, pz = c.as_list()
                qx, qy = rotate_point(aZ, ox, oy, px, py)  # rotate about z-axis
                qy, qz = rotate_point(aX, oy, oz, qy, pz)  # rotate about x-axis
                qx, qz = rotate_point(aY, ox, oz, qx, qz)  # rotate about y-axis
                results[k] = Coordinate(qx, qy, qz)
            setattr(self, name, results)
        for name, prop in [('thrusters', self.thrusters)]:
            for k in prop:
                c = prop[k].location
                px, py, pz = c.as_list()
                qx, qy = rotate_point(aZ, ox, oy, px, py)  # rotate about z-axis
                qy, qz = rotate_point(aX, oy, oz, qy, pz)  # rotate about x-axis
                qx, qz = rotate_point(aY, ox, oz, qx, qz)  # rotate about y-axis
                prop[k].location = Coordinate(qx, qy, qz)
        for name, prop in [('quiverP', self.quiverP), ('quiverN', self.quiverN)]:
            results = []
            for k in prop:
                px, py, pz = k
                qx, qy = rotate_point(-aZ, ox, oy, px, py)  # rotate about z-axis
                qy, qz = rotate_point(-aX, oy, oz, qy, pz)  # rotate about x-axis
                qx, qz = rotate_point(-aY, ox, oz, qx, qz)  # rotate about y-axis
                results.append([qx, qy, qz])
            setattr(self, name, results)
        if self.activeThruster != None:
            self.activeThrusterCounter += 1
            if self.activeThrusterCounter > self.activeThrusterCounterMaximum:
                self.activeThrusterCounter = 0
                self.activeThruster = None

    @property
    def verts(self):
        rfu = self._vertices['rfu'].as_list()
        lfu = self._vertices['lfu'].as_list()
        rbu = self._vertices['rbu'].as_list()
        lbu = self._vertices['lbu'].as_list()
        rfd = self._vertices['rfd'].as_list()
        lfd = self._vertices['lfd'].as_list()
        rbd = self._vertices['rbd'].as_list()
        lbd = self._vertices['lbd'].as_list()
        v = [
            [lfu, rfu, rbu, lbu],
            [lfd, rfd, rbd, lbd],
            [rfu, rfd, rbd, rbu],
            [lfu, lfd, lbd, lbu],
            [lfu, rfu, rfd, lfd],
            [lbu, rbu, rbd, lbd]
        ]
        return v

    @property
    def quiver(self):
        x, y, z = self.centroid
        u, v, w = self.quiverP
        nu, nv, nw = self.quiverN
        return x, y, z, u, v, w, nu, nv, nw


def rotate_point(t, o1, o2, p1, p2):
    q1 = o1 + cos(t) * (p1 - o1) - sin(t) * (p2 - o2)
    q2 = o2 + sin(t) * (p1 - o1) + cos(t) * (p2 - o2)
    return q1, q2
