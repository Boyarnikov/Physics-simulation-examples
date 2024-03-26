import math
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

from SoftBody import SoftBody
from AnimateSoftBody import AnimateSoftBody
from ClothShapes import create_rect_with_strong_edges, create_rect_x
from BodyShapes import create_cube_rigid
from Constrain import PlaneConstrain

# from matplotlib import rc
# rc('animation', html='jshtml')

import matplotlib

matplotlib.rcParams['animation.embed_limit'] = 20000

DT = 1 / 60

h, w = 10, 10
points, connections = create_rect_x(h, w,
                                    starting_point=np.array([0.1, 0.5, 1.0]),
                                    h_vec=np.array([0.8, 0.001, 0.0]),
                                    w_vec=np.array([0.0, 0.0, -0.8]))

i = 1
c = 0.01

sb = SoftBody(_points=points, _connections=connections, iters=i, m=0.1, c=c, b=2)
sb.fix_points([0])
sb.fix_points([h - 1])

t = 0


def pass_func():
    global t
    t += 0.02
    sb.point_position[h - 1][2] -= math.cos(t) * 0.01
    sb.point_position[h - 1][0] -= math.cos(t) * 0.01

    sb.point_position[0][2] -= math.cos(t) * 0.01
    sb.point_position[0][1] -= math.cos(t) * 0.02


'''
h, w, d = 2, 2, 2
points, connections = create_cube_rigid(h, w, d,
                                    starting_point=np.array([0.2, 0.2, 0.2]),
                                    h_vec=np.array([0.3, 0.0, 0.0]),
                                    w_vec=np.array([0.0, 0.3, 0.0]),
                                    d_vec=np.array([0.0, 0.0, 0.3]))

i = 1
c = 0.04
sb = SoftBody(_points=points, _connections=connections, iters=i, m=0.01, c=c)

sb.point_velocity[0] = np.array([80, 30, 50])
'''

floor = PlaneConstrain(np.zeros(3), np.array([1.0, 0.0, 0.0]), np.array([0.0, 1.0, 0.0]))
sb.add_constrain(floor)

wall = PlaneConstrain(np.zeros(3), np.array([0.0, 1.0, 0.0]), np.array([0.0, 0.0, 1.0]))
sb.add_constrain(wall)

wall = PlaneConstrain(np.zeros(3), np.array([0.0, 0.0, 1.0]), np.array([1.0, 0.0, 0.0]))
sb.add_constrain(wall)

wall = PlaneConstrain(np.array([0.0, 1.0, 0.0]), np.array([1.0, 0.0, 0.0]), np.array([0.0, 0.0, 1.0]))
sb.add_constrain(wall)

wall = PlaneConstrain(np.array([1.0, 0.0, 0.0]), np.array([0.0, 0.0, 1.0]), np.array([0.0, 1.0, 0.0]))
sb.add_constrain(wall)

frames = 400
asb = AnimateSoftBody(soft_body=sb, dt=DT, frames=frames, pass_func=pass_func)

ani = animation.FuncAnimation(
    asb.fig, asb.animation_func, frames, fargs=(asb,),
    interval=10)

writer = animation.PillowWriter(fps=30, bitrate=1800)
ani.save(f'bin/Cloth_with_physics_in_a_box.gif', writer=writer)

plt.show()
