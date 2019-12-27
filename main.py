import matplotlib

from controller import Controller

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
from matplotlib.animation import FuncAnimation

from cubesat import CubeSat
from plotter import ax, faces, thrusterPoints, fps, fig, reset_thruster_img, fire_thruster_img, poly, \
    bodyQuiverPositive, bodyQuiverNegative, axesNegative, axesPositive
from thruster import configurations

print(str(p3)[0:0])  # bug fix
print(str(bodyQuiverPositive)[0:0])  # bug fix
print(str(bodyQuiverNegative)[0:0])  # bug fix


def update_animation(i, cube, graphics):
    if cube.atc == cube.atcm:
        reset_thruster_img(cube.activeThruster)
    if (cube.activeThruster != None) and (cube.atc == 1):
        for thruster in thrusterPoints:
            reset_thruster_img(thruster)
        fire_thruster_img(cube.activeThruster, cube.thrusters[cube.activeThruster].location.z)

    cube.rotate()

    if graphics['displayWireframe']:
        for face in cube.faces:
            x, y, z = cube.wf(face)
            faces[face].set_data(x, y)
            faces[face].set_3d_properties(z)

    for thruster in cube.thrusters:
        x, y, z = cube.thrusters[thruster].location.as_list()
        thrusterPoints[thruster].set_data(x, y)
        thrusterPoints[thruster].set_3d_properties(z)
    x, y, z, u, v, w, nu, nv, nw = cube.quiver
    if graphics['displayQuiver']:
        graphics['bodyQuiverNegative'].remove()
        graphics['bodyQuiverPositive'].remove()
        graphics['bodyQuiverNegative'] = ax.quiver(x, y, z, u, v, w, arrow_length_ratio=0.15, color='blue', lw=0.5)
        graphics['bodyQuiverPositive'] = ax.quiver(x, y, z, nu, nv, nw, arrow_length_ratio=0.15, color='red', lw=0.5)
    controller.check_press(cube, graphics)

    if graphics['displayAV']:
        orientation = cube.avc
        graphics['avText'].set_text("Angular Velocity: {}".format(orientation))
    if graphics['displayBody']:
        poly.set_verts(cube.verts)


line_ani = None
controller = Controller()


def run(displayAV=False,
        displayAxes=True,
        randomAV=False,
        thrusterConfig=configurations['1u-1d-z-4'],
        displayBody=True,
        displayQuiver=False,
        displayWireframe=False):
    Cube = CubeSat(randomAV=randomAV, thrusters=thrusterConfig)
    avText = ax.text(-1, -1, -1, '')
    graphics = {
        'ax': ax,
        'faces': faces,
        'poly': poly,
        'avText': avText,
        'axesNegative': axesNegative,
        'axesPositive': axesPositive,
        'displayAxes': displayAxes,
        'displayAV': displayAV,
        'displayBody': displayBody,
        'displayQuiver': displayQuiver,
        'displayWireframe': displayWireframe,
        'bodyQuiverNegative': bodyQuiverNegative,
        'bodyQuiverPositive': bodyQuiverPositive,
    }
    fargs = [Cube, graphics]
    global line_ani
    line_ani = FuncAnimation(fig, update_animation, fargs=fargs, interval=1000 / fps)
    plt.show()


run(
    # thrusterConfig=configurations['1u-2d-xy-4']
)
