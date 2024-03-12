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


def create_cylinder(h, w, starting_point=np.array([0.5, 0.5, 1.]), w_vec=np.array([0., 0., -0.5]), r=0.3):
    return [starting_point + np.sin((j / (h)) * np.pi * 2) * r * np.array([1., 0., 0.]) + np.cos(
        (j / (h)) * np.pi * 2) * r * np.array([0., 1., 0.]) + i / (w - 1) * w_vec for i in range(w) for j in
            range(h)], []


def create_cylinder_x(h, w, starting_point=np.array([0.5, 0.5, 1.]), w_vec=np.array([0., 0., -0.5]), r=0.3):
    r, _ = create_cylinder(h, w, starting_point, w_vec, r)
    connections = []
    connections.extend([(i * h + j, i * h + (j + 1) % h) for i in range(w) for j in range(h)])
    connections.extend([(i * h + j, i * h + j + h) for i in range(w - 1) for j in range(h)])
    connections.extend([(i * h + j, i * h + (j + 1) % h + h) for i in range(w - 1) for j in range(h)])
    connections.extend([(i * h + j, i * h + (j - 1) % h + h) for i in range(w - 1) for j in range(h)])
    return r, connections


def create_heart_x(h, w, starting_point=np.array([0.5, 0.5, 1.]), w_vec=np.array([0., 0., -0.5]), r=0.02):
    r = [starting_point + 16 * np.sin(t) ** 3 * np.array([1., 0., 0.]) * r + (
                13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t)) * np.array([0., 1., 0.]) * r + i / (
                 w - 1) * w_vec for i in range(w) for t in [(j / h) * np.pi * 2 for j in range(h)]]
    connections = []
    connections.extend([(i * h + j, i * h + (j + 1) % h) for i in range(w) for j in range(h)])
    connections.extend([(i * h + j, i * h + j + h) for i in range(w - 1) for j in range(h)])
    connections.extend([(i * h + j, i * h + (j + 1) % h + h) for i in range(w - 1) for j in range(h)])
    connections.extend([(i * h + j, i * h + (j - 1) % h + h) for i in range(w - 1) for j in range(h)])
    return r, connections
