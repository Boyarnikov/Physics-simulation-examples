import numpy as np


def p_3d_to_flat(j, i, k, h, w, d):
    return k + j*d + i*d*w

def create_cube(h, w, d, starting_point=np.array([0., 0., 1.]), h_vec=np.array([1., 0., 0.]),
                w_vec=np.array([0., 1., 0.]), d_vec=np.array([0., 1., 0.])):
    points = [starting_point + i / (w - 1) * w_vec + j / (h - 1) * h_vec + k / (d - 1) * d_vec
              for j in range(h) for i in range(w) for k in range(d)]
    connections = []
    for i in range(w):
        for j in range(h):
            for k in range(d):
                if i < w - 1:
                    connections.append((p_3d_to_flat(i, j, k, h, w, d), p_3d_to_flat(i + 1, j, k, h, w, d)))
                if j < h - 1:
                    connections.append((p_3d_to_flat(i, j, k, h, w, d), p_3d_to_flat(i, j + 1, k, h, w, d)))
                if k < d - 1:
                    connections.append((p_3d_to_flat(i, j, k, h, w, d), p_3d_to_flat(i, j, k + 1, h, w, d)))
                    if i < w - 1 and j < h - 1:
                        connections.append((p_3d_to_flat(i, j, k, h, w, d), p_3d_to_flat(i + 1, j + 1, k + 1, h, w, d)))
                    if i > 0 and j < h - 1:
                        connections.append((p_3d_to_flat(i, j, k, h, w, d), p_3d_to_flat(i - 1, j + 1, k + 1, h, w, d)))
                    if i < w - 1 and j > 0:
                        connections.append((p_3d_to_flat(i, j, k, h, w, d), p_3d_to_flat(i + 1, j - 1, k + 1, h, w, d)))
                    if i > 0 and j > 0:
                        connections.append((p_3d_to_flat(i, j, k, h, w, d), p_3d_to_flat(i - 1, j - 1, k + 1, h, w, d)))


    return points, connections
