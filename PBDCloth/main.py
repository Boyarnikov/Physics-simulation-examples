import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

from SoftBody import SoftBody
from AnimateSoftBody import AnimateSoftBody
from ClothShapes import create_rect_x
from Constrain import PlaneConstrain

# from matplotlib import rc
# rc('animation', html='jshtml')

import matplotlib

matplotlib.rcParams['animation.embed_limit'] = 20000

DT = 1 / 60
h, w = 10, 10
points, connections = create_rect_x(h, w,
                                    starting_point=np.array([0.1, 0.1, 1.0]),
                                    h_vec=np.array([0.8, 0.0, 0.0]),
                                    w_vec=np.array([0.0, 0.8, 0.0]))

sb = SoftBody(_points=points, _connections=connections, iters=3, m=0.1, c=60)
sb.fix_points([0])
sb.fix_points([h - 1])

floor = PlaneConstrain(np.zeros(3), np.array([1.0, 0.0, 0.0]), np.array([0.0, 1.0, 0.0]))
sb.add_constrain(floor)
wall = PlaneConstrain(np.zeros(3), np.array([0.0, 1.0, 0.0]), np.array([0.0, 0.0, 1.0]))
sb.add_constrain(wall)
wall = PlaneConstrain(np.zeros(3), np.array([0.0, 0.0, 1.0]), np.array([1.0, 0.0, 0.0]))
sb.add_constrain(wall)

asb = AnimateSoftBody(soft_body=sb, dt=DT)

ani = animation.FuncAnimation(
    asb.fig, asb.animation_func, 10, fargs=(asb,),
    interval=10)

plt.show()
