from math import cos, sin


def rotate_point(t, o1, o2, p1, p2):
    q1 = o1 + cos(t) * (p1 - o1) - sin(t) * (p2 - o2)
    q2 = o2 + sin(t) * (p1 - o1) + cos(t) * (p2 - o2)
    return q1, q2
