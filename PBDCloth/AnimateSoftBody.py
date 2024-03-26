import time

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Line3D, Poly3DCollection
from mpl_toolkits.mplot3d.axes3d import Axes3D
from typing import List
from SoftBody import SoftBody
import Constrain


class AnimateSoftBody:
    time = 0
    fig = None
    ax: Axes3D = None
    soft_body = None
    actor_points: Line3D = None
    actor_connections: List[Line3D] = []
    actor_constrains: List[Poly3DCollection] = None

    draw_connections = True

    animation_func = None

    dt = 1 / 60

    frames = -1

    def __init__(self, soft_body: SoftBody, dt, draw_connections=True, frames=-1, pass_func=None):
        self.dt = dt
        self.time = 0
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(projection="3d")
        self.ax.set(xlim3d=(0, 1), xlabel='X')
        self.ax.set(ylim3d=(0, 1), ylabel='Y')
        self.ax.set(zlim3d=(0, 1), zlabel='Z')

        self.frames = frames

        self.soft_body = soft_body
        self.draw_connections = draw_connections

        self.actor_points = self.ax.plot3D(*self.soft_body.point_position.T, 'o', c='green')[0]

        if self.draw_connections:
            self._draw_connections()

        def animate(frame, animator: AnimateSoftBody):
            if pass_func:
                pass_func()
            if self.frames != -1 and frame < self.frames:
                if (frame // (self.frames // 10)) < (frame + 1) // (self.frames // 10):
                    print(f"{(frame + 1) // (self.frames // 10) * 10}%")

            animator._simulate_soft_body()
            animator._draw_constrains()
            animator._draw_points()
            if animator.draw_connections:
                animator._draw_connections()

            return self.actor_points, self.actor_connections

        self.animation_func = animate

    def _simulate_soft_body(self):
        self.soft_body.calculate_next_positions(self.dt)

    def _draw_constrains(self):
        if not self.actor_constrains:
            self.actor_constrains = [None] * len(self.soft_body.constrains)
            for i, c in enumerate(self.soft_body.constrains):
                if isinstance(c, Constrain.PlaneConstrain):
                    u = c.v_start / 2 + np.linspace(0, 1, 4).reshape((4, 1)) * c.v1.reshape((1, 3))
                    v = c.v_start / 2 + np.linspace(0, 1, 4).reshape((4, 1)) * c.v2.reshape((1, 3))
                    points = v[:, None, :] + u[None, :, :]
                    points.reshape((points.shape[0] * points.shape[1], points.shape[2]))
                    self.actor_constrains[i] = self.ax.plot_surface(points[:, :, 0], points[:, :, 1], points[:, :, 2],
                                                                    alpha=0.1)

    def _draw_connections(self):
        _left_connections = np.take(self.soft_body.point_position, (self.soft_body.connection[:, 0] * 3,
                                                                    self.soft_body.connection[:, 0] * 3 + 1,
                                                                    self.soft_body.connection[:, 0] * 3 + 2)).T
        _right_connections = np.take(self.soft_body.point_position, (self.soft_body.connection[:, 1] * 3,
                                                                     self.soft_body.connection[:, 1] * 3 + 1,
                                                                     self.soft_body.connection[:, 1] * 3 + 2)).T

        if not self.actor_connections:
            self.actor_connections = [
                self.ax.plot3D(*np.concatenate((_left_connections[i], _right_connections[i])).reshape((2, 3)).T,
                               c='red')[0]
                for i in range(self.soft_body.connection_amount)
            ]
        else:
            for i, actor in enumerate(self.actor_connections):
                if not self.soft_body.connection_is_active[i]:
                    actor.set_data([0], [0])
                    actor.set_3d_properties(0)
                    continue

                p1 = self.soft_body.point_position[self.soft_body.connection[i, 0]]
                p2 = self.soft_body.point_position[self.soft_body.connection[i, 1]]
                if np.linalg.norm(p1 - p2) > self.soft_body.connection_idle_len[i] * 1.1:
                    actor.set(color="r")
                else:
                    actor.set(color="b")

                actor.set_data(np.column_stack((p1, p2))[:2])
                actor.set_3d_properties(np.column_stack((p1, p2))[2], "z")

    def _draw_points(self):
        self.actor_points.set_data(*self.soft_body.point_position.T[:2])
        self.actor_points.set_3d_properties(self.soft_body.point_position.T[2], "z")
