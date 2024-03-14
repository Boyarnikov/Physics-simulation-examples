import numpy as np


class Constrain:
    def iterate_constrain(self, point_position: np.array, point_velocity: np.array):
        pass


class PlaneConstrain(Constrain):
    v_start = np.zeros(3)
    v1 = np.array([1., 0., 0., ])
    v2 = np.array([0., 1., 0., ])
    n_hat = None

    def __init__(self, v_start=None, v1=None, v2=None):
        if v_start is not None:
            self.v_start = v_start
        if v1 is not None:
            self.v1 = v1
        if v2 is not None:
            self.v2 = v2

        n_hat = np.cross(self.v1, self.v2)
        self.n_hat = n_hat / np.sqrt(np.dot(n_hat, n_hat))

    def iterate_constrain(self, point_position: np.array, point_velocity: np.array):

        result = np.zeros(point_position.shape[0])
        for idx in range(point_position.shape[0]):
            result[idx] = np.dot(self.n_hat, point_position[idx, :] - self.v_start)
            if result[idx] < 0:
                point_position[idx, :] -= self.n_hat * result[idx]
                point_velocity[idx, :] -= 2 * np.dot(point_velocity[idx, :], self.n_hat)
