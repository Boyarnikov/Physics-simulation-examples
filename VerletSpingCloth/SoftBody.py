import numpy as np
from typing import List

GLOBAL_CONSTANT_FORCE = np.array([0, 0, -9.5], dtype=np.float64)  # Гравитация

class SoftBody:
    point_amount = 0
    point_position = np.empty((point_amount, 3), dtype=np.float64)
    point_old_position = np.empty((point_amount, 3), dtype=np.float64)
    point_force = np.empty((point_amount, 3), dtype=np.float64)
    point_mass = np.empty(point_amount, dtype=np.float64)
    point_is_free = np.empty(point_amount, dtype=np.bool_)

    connection_amount = 0
    connection = np.empty((connection_amount, 2), dtype=np.uintc)
    connection_idle_len = np.empty(connection_amount, dtype=np.uintc)
    connection_k = np.empty(connection_amount, dtype=np.float64)
    connection_is_active = np.empty(connection_amount, dtype=np.bool_)

    def __init__(self,
                 _points,
                 _old_points=None,
                 _connections=None,
                 m=1.,
                 c=30,
                 k=1.):
        self.point_amount = len(_points)
        self.point_position = np.asarray(_points, dtype=np.float64)
        if _old_points:
            self.point_old_position = np.asarray(_old_points),
        else:
            self.point_old_position = self.point_position.copy()

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

        if type(k) in [np.float64, float]:
            self.connection_k = np.ones(self.connection_amount, dtype=np.float64) * k
        else:
            self.connection_k = np.asarray(k, dtype=np.float64)

        self.connection_is_active = np.ones(self.point_amount, dtype=np.bool_)
        self.C = c

    def fix_points(self, fix_points: List[int]):
        for p in fix_points:
            self.point_is_free[p] = False

    def _calculate_forces(self):
        self.point_force = np.zeros((self.point_amount, 3), dtype=np.float64)

        _left_connections = np.take(self.point_position, (self.connection[:, 0] * 3,
                                                          self.connection[:, 0] * 3 + 1,
                                                          self.connection[:, 0] * 3 + 2)).T
        _right_connections = np.take(self.point_position, (self.connection[:, 1] * 3,
                                                           self.connection[:, 1] * 3 + 1,
                                                           self.connection[:, 1] * 3 + 2)).T
        direction = _right_connections - _left_connections
        length = np.linalg.norm(direction, axis=1)

        offset_scal = (np.ones(self.connection_amount) - self.connection_idle_len / length) / 2 * self.connection_k
        np.expand_dims(offset_scal, 0)

        offset = direction * offset_scal[..., None]

        for i in range(self.connection_amount):
            self.point_force[self.connection[i][0]] += offset[i]
            self.point_force[self.connection[i][1]] -= offset[i]

        self.point_force += GLOBAL_CONSTANT_FORCE * self.point_mass

    def calculate_next_positions(self, dt):
        self._calculate_forces()
        acc = self.point_force / self.point_mass
        old_position = self.point_position.copy()

        self.point_position += ((1 - self.C / self.point_mass / 2 * dt * dt) * (
                self.point_position - self.point_old_position) + acc * dt * dt) * self.point_is_free[..., None]
        self.point_old_position = old_position