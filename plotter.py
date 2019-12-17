from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib import colors as mcolors

fps = 60
dimensions = (1, 1, 1)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ms = 10

avText = ax.text(-1, -1, -1, "(0, 0, 0)")
reach = 1
lims = (-reach, reach)
uFace, = ax.plot([], [], [])
dFace, = ax.plot([], [], [])
lFace, = ax.plot([], [], [])
rFace, = ax.plot([], [], [])
fFace, = ax.plot([], [], [])
bFace, = ax.plot([], [], [])

thrusterRF, = ax.plot([], [], [], 'b', marker='$rf$', markersize=ms)
thrusterRB, = ax.plot([], [], [], 'b', marker='$rb$', markersize=ms)
thrusterLF, = ax.plot([], [], [], 'b', marker='$lf$', markersize=ms)
thrusterLB, = ax.plot([], [], [], 'b', marker='$lb$', markersize=ms)

ax.set_xlim3d(lims)
ax.set_xlabel('x')
ax.set_ylim3d(lims)
ax.set_ylabel('y')
ax.set_zlim3d(lims)
ax.set_zlabel('z')
ax.set_title('OF-CG Attitude Control')
plt.locator_params(nbins=2)

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
    return mcolors.to_rgba(arg, alpha=0.25)

facecolors=[cc('g'), cc('g'), cc('b'), cc('b'), cc('y'), cc('y')]

def reset_thruster_img(thruster):
    thrusterPoints[thruster].set_color('b')
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



