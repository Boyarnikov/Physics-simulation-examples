from manim import *
import bisect
import numpy as np
from scipy.integrate import solve_ivp
from matplotlib.animation import FuncAnimation
from matplotlib.pyplot import figure

w = 2 * np.pi
dt = 0.01
T = 10
iters = int(T / dt)


def simulate(d, x0):
    A = np.array([[0., 1], [-w ** 2, - 2 * d * w]])
    # %%  Forward Euler

    xF = np.zeros([2, iters], dtype=np.float64)
    tF = np.zeros([iters], dtype=np.float64)
    xF[:, 0] = x0
    tF[0] = 0

    for i in range(iters - 1):
        tF[i + 1] = i * dt
        xF[:, i + 1] = (np.eye(2) + A * dt).dot(xF[:, i])

    xB = np.zeros([2, iters], dtype=np.float64)
    tB = np.zeros([iters], dtype=np.float64)
    xB[:, 0] = x0
    tB[0] = 0
    for i in range(iters - 1):
        tB[i + 1] = i * dt
        xB[:, i + 1] = np.linalg.inv(np.eye(2) - A * dt).dot(xB[:, i])

    def spring(t, x):
        return A.dot(x)

    sol = solve_ivp(spring, [0, T], x0)

    return (list(tF), xF[0]), (list(tB), xB[0]), (list(sol.t), sol.y[0])


class EulerComparison(Scene):
    def construct(self):
        E, B, S = simulate(0, np.array([0.2, 0.]))

        ax = Axes(
            x_range=[0, T], y_range=[-2, 2], axis_config={"include_tip": False, "stroke_width": 1}
        )
        labels = ax.get_axis_labels(x_label="t", y_label="x")
        t = ValueTracker(0)

        title = Tex(r"Spring with damping friction").shift(3 * UP)
        func = MathTex(r"d = \frac{c}{2 \sqrt{km}}, \omega_0 = \sqrt{\frac{k}{m}}", color=WHITE).next_to(title, DOWN)
        self.play(Write(title, run_time=0.5), FadeIn(func, shift=DOWN))
        self.wait(1)
        formula = MathTex(r"\Ddot{x} + 2d\omega_0\dot{x} + \omega_0^2 x = 0", color=WHITE).next_to(func, DOWN)
        self.play(FadeIn(formula, shift=DOWN))
        self.wait(1)
        second_formula = MathTex(r"""\dot{z} =""", r"""
                                                \begin{bmatrix}
                                                    0 & 1 \\
                                                    -\omega_0^2 & -2d\omega_0 \\
                                                \end{bmatrix}""", r"""
                                                \cdot z = A \cdot z""",
                                 color=WHITE).next_to(formula, DOWN)
        self.wait(2)
        self.play(FadeIn(second_formula, shift=DOWN))
        self.wait(5)
        self.play(FadeOut(func), FadeOut(formula), second_formula.animate.move_to(func))
        self.wait(1)
        framebox1 = SurroundingRectangle(second_formula[1], buff=.1)
        self.play(
            Transform(title, Tex(r"This is our main matrix").shift(3 * UP)),
            Create(framebox1),
        )
        self.wait(3)
        self.play(
            Transform(title, Tex(r"Let's see how things look when d = 0").shift(3 * UP)),
        )
        self.wait(3)

        self.play(Write(ax), Write(labels), FadeOut(framebox1),
                  Transform(title, Tex(r"This is Euler").shift(3 * UP)),
                  Transform(second_formula,
                            MathTex(r"z_{k+1} = (I + A\cdot\Delta t)\cdot z_k = F\cdot z_k", color=MAROON).next_to(
                                title, DOWN)))
        graphEuler = ax.plot(lambda x: np.interp(x, E[0], E[1]), color=MAROON)

        self.play(Write(graphEuler, run_time=3))

        graphBackwardEuler = ax.plot(lambda x: np.interp(x, B[0], B[1]), color=BLUE)
        self.play(Transform(title, Tex(r"This is Backward Euler").shift(3 * UP)),
                  Transform(second_formula,
                            MathTex(r"z_{k+1} = (I - A\cdot\Delta t)^{-1}\cdot z_k = B\cdot z_k", color=BLUE).next_to(
                                title, DOWN)))
        self.play(Write(graphBackwardEuler), run_time=3)

        graphSolveIVP = ax.plot(lambda x: np.interp(x, S[0], S[1]), color=GREEN)
        self.play(Transform(title, Tex("This is a solution from scipy solve ivp").shift(3 * UP)),
                  Transform(second_formula, MathTex(r"\dot{z} = A \cdot z", color=GREEN).next_to(title, DOWN)))
        self.play(Write(graphSolveIVP), run_time=3)

        self.wait(2)

        self.play(
            Transform(title, Tex(r"Euler gains energy, Backward Euler loose").shift(3 * UP)),
        )
        self.wait(5)
        self.play(
            Transform(title,
                      Tex(r"Now let's look at d bigger then zero:").shift(3 * UP)),
            FadeOut(second_formula)
        )
        self.wait(5)

        positions = [(0.02, np.array([0.5, 0.])),
                     (0.1, np.array([2., 0.])),
                     (0.5, np.array([2., 0.])),
                     (1.0, np.array([2., 0.]))]

        for d, x0 in positions:
            E, B, S = simulate(d, x0)
            newGraphEuler = ax.plot(lambda x: np.interp(x, E[0], E[1]), color=MAROON)
            newGraphBackwardEuler = ax.plot(lambda x: np.interp(x, B[0], B[1]), color=BLUE)
            newGaphSolveIVP = ax.plot(lambda x: np.interp(x, S[0], S[1]), color=GREEN)
            self.play(Transform(title, Tex(rf"This is d={d}:").shift(3 * UP)),
                      Transform(graphEuler, newGraphEuler),
                      Transform(graphBackwardEuler, newGraphBackwardEuler),
                      Transform(graphSolveIVP, newGaphSolveIVP))

            self.wait(3)
