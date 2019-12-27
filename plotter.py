import numpy as np
from matplotlib import colors as mcolors
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

fps = 60
dimensions = (1, 1, 1)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ms = 10

thrusterColor = 'black'
reach = 1
lims = (-reach, reach)
uFace, = ax.plot([], [], [], lw=0.25)
dFace, = ax.plot([], [], [], lw=0.25)
lFace, = ax.plot([], [], [], lw=0.25)
rFace, = ax.plot([], [], [], lw=0.25)
fFace, = ax.plot([], [], [], lw=0.25)
bFace, = ax.plot([], [], [], lw=0.25)

thrusterRF, = ax.plot([], [], [], thrusterColor, marker='$rf$', markersize=ms)
thrusterRB, = ax.plot([], [], [], thrusterColor, marker='$rb$', markersize=ms)
thrusterLF, = ax.plot([], [], [], thrusterColor, marker='$lf$', markersize=ms)
thrusterLB, = ax.plot([], [], [], thrusterColor, marker='$lb$', markersize=ms)

ax.set_xlim3d(lims)
ax.set_xlabel('x')
ax.set_ylim3d(lims)
ax.set_ylabel('y')
ax.set_zlim3d(lims)
ax.set_zlabel('z')
ax.set_title('OF-CG Attitude Control')
plt.locator_params(nbins=2)
x, y, z = np.zeros((3, 3))
u, v, w = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
ax.quiver(x, y, z, u, v, w, arrow_length_ratio=0.1, color='green', lw=0.5, linestyle='-.')
u, v, w = np.array([[-1, 0, 0], [0, -1, 0], [0, 0, -1]])
ax.quiver(x, y, z, u, v, w, arrow_length_ratio=0.1, color='pink', lw=0.5, linestyle='-.')

bodyQuiverPositive = ax.quiver(x, y, z, x, y, z, arrow_length_ratio=0.15, color='blue', lw=0.5)
bodyQuiverNegative = ax.quiver(x, y, z, x, y, z, arrow_length_ratio=0.15, color='red', lw=0.5)

faces = {
    'up': uFace,
    'down': dFace,
    'left': lFace,
    'right': rFace,
    'back': bFace,
    'front': fFace,
}
thrusterPoints = {
    'rf': thrusterRF,
    'rb': thrusterRB,
    'lf': thrusterLF,
    'lb': thrusterLB,
}


def cc(arg):
    return mcolors.to_rgba(arg, alpha=0.05)


facecolors = [cc('g'), cc('g'), cc('b'), cc('b'), cc('y'), cc('y')]


def reset_thruster_img(thruster):
    thrusterPoints[thruster].set_color(thrusterColor)
    thrusterPoints[thruster].set_marker('${}$'.format(thruster))
    thrusterPoints[thruster].set_markersize(ms)


def fire_thruster_img(thruster, pos):
    thrusterPoints[thruster].set_color('r')
    if pos > 0:
        shape = "^"
    else:
        shape = "v"
    thrusterPoints[thruster].set_marker(shape)
    thrusterPoints[thruster].set_markersize(ms * 2)


poly = Poly3DCollection([], facecolors=facecolors)
ax.add_collection3d(poly, zs=range(6))
