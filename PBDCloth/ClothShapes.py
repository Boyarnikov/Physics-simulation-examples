import numpy as np


def create_rect(h, w, starting_point=np.array([0., 0., 1.]), h_vec=np.array([1., 0., 0.]),
                w_vec=np.array([0., 1., 0.])):
    return [starting_point + i / (w - 1) * w_vec + j / (h - 1) * h_vec for i in range(w) for j in range(h)], []


def create_rect_x(h, w, starting_point=np.array([0., 0., 1.]), h_vec=np.array([1., 0., 0.]),
                  w_vec=np.array([0., 1., 0.])):
    r, _ = create_rect(h, w, starting_point, h_vec, w_vec)
    connections = []
    connections.extend([(i * h + j, i * h + j + 1) for i in range(w) for j in range(h - 1)])
    connections.extend([(i * h + j, i * h + j + h) for i in range(w - 1) for j in range(h)])
    connections.extend([(i * h + j, i * h + j + 1 + h) for i in range(w - 1) for j in range(h - 1)])
    connections.extend([(i * h + j, i * h + j - 1 + h) for i in range(w - 1) for j in range(1, h)])
    return r, connections
