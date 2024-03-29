import numpy as np
from typing import List

from Constrain import Constrain, PlaneConstrain

GLOBAL_CONSTANT_FORCE = np.array([0, 0, -9.5], dtype=np.float64)  # Гравитация


class SoftBody:
    point_amount = 0
    point_position = np.empty((point_amount, 3), dtype=np.float64)
    point_velocity = np.empty((point_amount, 3), dtype=np.float64)
    point_next_position = np.empty((point_amount, 3), dtype=np.float64)
    point_force = np.empty((point_amount, 3), dtype=np.float64)
    point_mass = np.empty(point_amount, dtype=np.float64)
    point_is_free = np.empty(point_amount, dtype=np.bool_)

    connection_amount = 0
    connection = np.empty((connection_amount, 2), dtype=np.uintc)
    connection_idle_len = np.empty(connection_amount, dtype=np.uintc)
    connection_is_active = np.empty(connection_amount, dtype=np.bool_)

    iteration_count = 1
    breaking_coefficient = 3.5

    constrains: List[Constrain] = []

    def __init__(self,
                 _points,
                 _connections=None,
                 m=1.,
                 c=0.,
                 b=3.,
                 iters: int = 1):
        self.point_amount = len(_points)
        self.point_position = np.asarray(_points, dtype=np.float64)
        self.point_next_position = self.point_position.copy()
        self.point_velocity = np.zeros((self.point_amount, 3), dtype=np.float64)

        if type(m) in [np.float64, float]:
            self.point_mass = np.ones(self.point_amount, dtype=np.float64) * m
        else:
            self.point_mass = np.asarray(_points, dtype=np.float64)
        self.point_mass = self.point_mass[..., None]
        self.point_force = np.zeros((self.point_amount, 3), dtype=np.float64)
        self.point_is_free = np.ones(self.point_amount, dtype=np.bool_)

        self.connection_amount = 0 if _connections is None else len(_connections)
        self.connection = np.zeros((0, 2), dtype=np.uintc)
        if self.connection_amount:
            self.connection = np.asarray(_connections, dtype=np.uintc)

        _left_connections = np.take(self.point_position, (self.connection[:, 0] * 3,
                                                          self.connection[:, 0] * 3 + 1,
                                                          self.connection[:, 0] * 3 + 2)).T
        _right_connections = np.take(self.point_position, (self.connection[:, 1] * 3,
                                                           self.connection[:, 1] * 3 + 1,
                                                           self.connection[:, 1] * 3 + 2)).T
        _connections = _right_connections - _left_connections
        self.connection_idle_len = np.linalg.norm(_connections, axis=1)

        self.iteration_count = iters

        self.connection_is_active = np.ones(len(_connections), dtype=np.bool_)
        self.C = c
        self.breaking_coefficient = b if b else 3.5

    def fix_points(self, fix_points: List[int]):
        for p in fix_points:
            self.point_is_free[p] = False

    def add_constrain(self, constrain: Constrain):
        self.constrains.append(constrain)

    def _solve_constrains(self):
        self.last_collision_norm = np.zeros((self.point_amount, 3))
        for _ in range(self.iteration_count):
            self._iterate_constrains_connections()
            for c in self.constrains:
                c.iterate_constrain(self.point_next_position, self.last_collision_norm)

    def _iterate_constrains_connections(self):
        for index in range(self.connection_amount):
            if not self.connection_is_active[index]:
                continue
            i, j = self.connection[index][0], self.connection[index][1]
            direction = self.point_next_position[i] - self.point_next_position[j]
            if np.linalg.norm(direction) > self.connection_idle_len[index] * self.breaking_coefficient:
                self.connection_is_active[index] = False
                continue
            if np.linalg.norm(direction):
                offset = direction * (1 - self.connection_idle_len[index] / np.linalg.norm(direction))
                if not self.point_is_free[i] or not self.point_is_free[j]:
                    offset *= 2
                if self.point_is_free[i]:
                    self.point_next_position[i] -= offset / 2
                if self.point_is_free[j]:
                    self.point_next_position[j] += offset / 2

    def _calculate_forces(self):
        self.point_force = np.zeros((self.point_amount, 3), dtype=np.float64)
        self.point_force += GLOBAL_CONSTANT_FORCE * self.point_mass

    def calculate_next_positions(self, dt):
        self._calculate_forces()
        acc = self.point_force / self.point_mass

        self.point_velocity += acc * dt

        self.point_velocity *= 1 - self.C

        self.point_next_position = self.point_position + self.point_velocity * dt * self.point_is_free[..., None]

        self._solve_constrains()

        self.point_velocity = (self.point_next_position - self.point_position) / dt
        self.point_position = self.point_next_position

        for idx in range(self.point_amount):
            if np.linalg.norm(self.last_collision_norm[idx, :]) > -0.1:
                if np.dot(self.point_velocity[idx, :], self.last_collision_norm[idx, :]) < 0:
                    self.point_velocity[idx, :] -= (self.last_collision_norm[idx, :] *
                                                    np.dot(self.point_velocity[idx, :],
                                                           self.last_collision_norm[idx, :]))
                    self.point_velocity[idx, :] *= (1 - self.C) ** 2
                    self.point_velocity[idx, :] -= (self.last_collision_norm[idx, :] *
                                                    np.dot(self.point_velocity[idx, :],
                                                           self.last_collision_norm[idx, :]))
