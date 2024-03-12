import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

from SoftBody import SoftBody
from AnimateSoftBody import AnimateSoftBody
from ClothShapes import create_rect_x, create_heart_x, create_cylinder_x

# from matplotlib import rc
# rc('animation', html='jshtml')

import matplotlib

matplotlib.rcParams['animation.embed_limit'] = 20000

DT = 1 / 60
h, w = 20, 10
"""
points, connections = create_rect_x(h, w,
                                    starting_point=np.array([0.2, 0.2, 0.6]),
                                    h_vec=np.array([0.6, 0.6, 0.4]),
                                    w_vec=np.array([0.2, 0.1, -0.5]))

sb = SoftBody(_points=points, _connections=connections, k=200, m=0.1, c=60)
sb.fix_points([j for j in range(h // 5)])
sb.fix_points([j for j in range(h // 5 * 4, h)])
"""
points, connections = create_heart_x(h, w)
sb = SoftBody(_points=points, _connections=connections, k=200, m=0.1, c=60)
sb.fix_points([j for j in range(h)])

asb = AnimateSoftBody(soft_body=sb, dt=DT)

ani = animation.FuncAnimation(
    asb.fig, asb.animation_func, 10, fargs=(asb,),
    interval=10)

plt.show()

