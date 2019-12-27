import matplotlib

from controller import check_press

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
from matplotlib.animation import FuncAnimation

from cubesat import CubeSat
from plotter import ax, faces, thrusterPoints, fps, fig, reset_thruster_img, fire_thruster_img, poly
from thruster import configurations

print(str(p3)[0:0])  # bug fix


def update_animation(i, cube, avText, displayBody, displayQuiver, displayWireframe):
    if cube.atc == cube.atcm:
        reset_thruster_img(cube.activeThruster)
    if (cube.activeThruster != None) and (cube.atc == 1):
        for thruster in thrusterPoints:
            reset_thruster_img(thruster)
        fire_thruster_img(cube.activeThruster, cube.thrusters[cube.activeThruster].location.z)

    cube.rotate()

    if displayWireframe:
        for face in cube.faces:
            x, y, z = cube.wf(face)
            faces[face].set_data(x, y)
            faces[face].set_3d_properties(z)

    for thruster in cube.thrusters:
        x, y, z = cube.thrusters[thruster].location.as_list()
        thrusterPoints[thruster].set_data(x, y)
        thrusterPoints[thruster].set_3d_properties(z)
    x, y, z, u, v, w, nu, nv, nw = cube.quiver
    if displayQuiver:
        global bodyQuiverNegative, bodyQuiverPositive
        bodyQuiverPositive.remove()
        bodyQuiverNegative.remove()
        bodyQuiverPositive = ax.quiver(x, y, z, u, v, w, arrow_length_ratio=0.15, color='blue', lw=0.5)
        bodyQuiverNegative = ax.quiver(x, y, z, nu, nv, nw, arrow_length_ratio=0.15, color='red', lw=0.5)
    check_press(cube)
    if avText:
        orientation = cube.avc
        avText.set_text("Angular Velocity: {}".format(orientation))
    if displayBody:
        poly.set_verts(cube.verts)


def run(displayAV=False, randomAV=False, thrusterConfig=configurations['1u-1d-z-4'], displayBody=True,
        displayQuiver=False, displayWireframe=False):
    Cube = CubeSat(randomAV=randomAV, thrusters=thrusterConfig)
    avText = ax.text(-1, -1, -1, "Angular Velocity: (0, 0, 0)") if displayAV else None
    fargs = [Cube, avText, displayBody, displayQuiver, displayWireframe]
    line_ani = FuncAnimation(fig, update_animation, fargs=fargs, interval=1000 / fps)
    plt.show()


run(
    displayBody=False,
    displayAV=True,
    displayQuiver=False,
    displayWireframe=True,
    randomAV=True,
    # thrusterConfig=configurations['1u-2d-xy-4']
)
