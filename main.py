import matplotlib

from controller import check_press

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
from matplotlib.animation import FuncAnimation

from cubesat import CubeSat
from plotter import faces, thrusterPoints, avText, fps, fig, reset_thruster_img, fire_thruster_img, poly

print(str(p3)[0:0])  # bug fix


def update_animation(i, cube):
    if cube.atc == cube.atcm:
        reset_thruster_img(cube.activeThruster)
    if (cube.activeThruster != None) and (cube.atc == 1):
        for thruster in thrusterPoints:
            reset_thruster_img(thruster)
        fire_thruster_img(cube.activeThruster, cube.thrusters[thruster][2])

    cube.rotate()

    for face in cube.faces:
        x, y, z = cube.wire_frame(face)
        faces[face].set_data(x, y)
        faces[face].set_3d_properties(z)

    for thruster in cube.thrusters:
        x, y, z = cube.thrusters[thruster]
        thrusterPoints[thruster].set_data(x, y)
        thrusterPoints[thruster].set_3d_properties(z)

    check_press(cube)
    orientation = cube.avc
    avText.set_text(orientation)
    poly.set_verts(cube.verts)


Cube = CubeSat(randomInit=True)

line_ani = FuncAnimation(fig, update_animation, fargs=[Cube], interval=1000 / fps)
plt.show()
