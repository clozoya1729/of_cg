import random
from math import cos, sin

origin = [0, 0, 0]
unitDims = [1, 1, 1]


class Cube:
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

    def __init__(self, dimensions=unitDims, centroid=origin, mass=1, randomAV=False):
        '''
        r=right, l=left, f=front, b=back, u=up, d=down
        '''
        x = dimensions[0] / 2
        y = dimensions[1] / 2
        z = dimensions[2] / 2
        self.centroid = centroid
        if randomAV:
            self._angularVelocity = {
                'x': 0.1 + random.randint(-2, 1) / 5,
                'y': random.randint(-2, 1) / 5,
                'z': 0  # random.randint(-1, 1) / 10,
            }

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

    @property
    def vertices(self):
        return [self._vertices[v] for v in self._vertices]

    @property
    def splitVertices(self):
        v = self.vertices
        return [c[0] for c in v], [c[1] for c in v], [c[2] for c in v]

    def wf(self, face):
        """
        Wire Frame
        face: str
        return:
        """
        v = self._vertices
        w = ([v[point] for point in self.faces[face]])
        return [c[0] for c in w], [c[1] for c in w], [c[2] for c in w]

    @property
    def avc(self):
        """
        Angular Velocity Components
        return: list of float - [x, y, z]
        """
        return self._angularVelocity['x'], self._angularVelocity['y'], self._angularVelocity['z']

    def rotate(self):
        ox, oy, oz = self.centroid
        aX, aY, aZ = self.avc
        for name, prop in [('_vertices', self._vertices)]:
            results = {}
            for k in prop:
                px, py, pz = prop[k]
                qx, qy = rotate_point(aZ, ox, oy, px, py)  # rotate about z-axis
                qy, qz = rotate_point(aX, oy, oz, qy, pz)  # rotate about x-axis
                qx, qz = rotate_point(aY, ox, oz, qx, qz)  # rotate about y-axis
                results[k] = [qx, qy, qz]
            setattr(self, name, results)
        for name, prop in [('thrusters', self.thrusters)]:
            for k in prop:
                px, py, pz = prop[k].location
                qx, qy = rotate_point(aZ, ox, oy, px, py)  # rotate about z-axis
                qy, qz = rotate_point(aX, oy, oz, qy, pz)  # rotate about x-axis
                qx, qz = rotate_point(aY, ox, oz, qx, qz)  # rotate about y-axis
                prop[k].location = [qx, qy, qz]
        if self.activeThruster != None:
            self.activeThrusterCounter += 1
            if self.activeThrusterCounter > self.activeThrusterCounterMaximum:
                self.activeThrusterCounter = 0
                self.activeThruster = None

    @property
    def verts(self):
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


def rotate_point(t, o1, o2, p1, p2):
    q1 = o1 + cos(t) * (p1 - o1) - sin(t) * (p2 - o2)
    q2 = o2 + sin(t) * (p1 - o1) + cos(t) * (p2 - o2)
    return q1, q2
