from manim import *
import bisect
import numpy as np
from scipy.integrate import solve_ivp
from matplotlib.animation import FuncAnimation
from matplotlib.pyplot import figure

# some global constants
T = 100  # Сколько секунд симулируем
sun = np.array([0., 0., 0.])  # Координаты массивного тела
sun_mass = 10  # Масса массивного тела
G = 6.673  # Гравитационная константа
T_lim = 10 ** 3  # Предел при выходе за который прекращаем симуляцию

# При очень маленьких dt у нас получатся сильно гладкие кривые на рендере, что не не делает визуализацию
# понятнее, но сильно жрёт производительность. Константа даёт контроль над тем с какого момента мы
# начинаем "срезать" некоторые точки и использовать только какую-то долю для визуализации
# (симуляция при этом идёт с чистым dt)
# значение до 1/10 в целом дают ок картинку
RENDER_LINE_CLUMP = 1 / 50


def simulate_euler(x0, v0, dt):
    """
    Симулирует метод Эйлера для стартовой позиции x0 и скорости v0 с шагом dt.
    Возвращает набор времён, позиций и скоростей.
    Ускорение берёт из F/m = mMG/r*r*m = MG/r^2.
    """
    iters = int(T / dt)

    xF = np.zeros([3, iters], dtype=np.float64)
    vF = np.zeros([3, iters], dtype=np.float64)
    tF = np.zeros([iters], dtype=np.float64)

    xF[:, 0] = x0
    vF[:, 0] = v0
    tF[0] = 0

    for i in range(iters - 1):
        distance = np.linalg.norm(xF[:, i] - sun)
        if distance > T_lim:
            tF = tF[:i]
            xF = xF[:, :i]
            vF = vF[:, :i]
            break

        if distance == 0:
            acc_m = 0
            acc = np.array([0., 0., 0.])
        else:
            acc_m = G * sun_mass / (distance ** 2)
            acc = (sun - xF[:, i]) / distance * acc_m

        xF[:, i + 1] = xF[:, i] + vF[:, i] * dt
        vF[:, i + 1] = vF[:, i] + acc * dt

    return tF, xF, vF


def simulate_half_euler(x0, v0, dt):
    """
    Симулирует метод Полу-Эйлера для стартовой позиции x0 и скорости v0 с шагом dt.
    Возвращает набор времён, позиций и скоростей.
    Ускорение берёт из F/m = mMG/r*r*m = MG/r^2.
    """
    iters = int(T / dt)

    xF = np.zeros([3, iters], dtype=np.float64)
    vF = np.zeros([3, iters], dtype=np.float64)
    tF = np.zeros([iters], dtype=np.float64)

    xF[:, 0] = x0
    vF[:, 0] = v0
    tF[0] = 0

    for i in range(iters - 1):
        distance = np.linalg.norm(xF[:, i] - sun)
        if distance > T_lim:
            tF = tF[:i]
            xF = xF[:, :i]
            vF = vF[:, :i]
            break

        if distance == 0:
            acc_m = 0
            acc = np.array([0., 0., 0.])
        else:
            acc_m = G * sun_mass / (distance ** 2)
            acc = (sun - xF[:, i]) / distance * acc_m

        vF[:, i + 1] = vF[:, i] + acc * dt
        xF[:, i + 1] = xF[:, i] + vF[:, i + 1] * dt

    return tF, xF, vF


class EulerTrajectory(ThreeDScene):
    def construct(self):
        """Сцена с объяснением откуда берутся методы и их визуализацией"""

        # Объяснение Эйлера
        title = Tex(r"Now let's compare Eulerian And Semi-Eulerian methods").shift(2 * UP + [0., 0., 1.])
        func1 = MathTex(r"x_{i+1} = x_{i} + v_{i} * dt", r"\\", r"v_{i+1} = v_{i} + a * dt", color=RED).next_to(title,
                                                                                                                DOWN)
        self.play(Write(title, run_time=1))
        self.wait(1)
        self.play(FadeIn(func1, shift=DOWN))
        self.wait(2)

        explanation = Tex(r"In Eulerian we use position and velocity \\ to calculate next position").next_to(func1,
                                                                                                             DOWN)
        framebox = SurroundingRectangle(func1[0], buff=.1, color=WHITE)
        self.play(Write(explanation, run_time=2), FadeIn(framebox))
        self.wait(2)
        explanation2 = Tex(
            r"Then we calculate new velocity from old velocity \\ and acceleration at this point and time").next_to(
            explanation, DOWN)
        self.play(Write(explanation2, run_time=2),
                  Transform(framebox, SurroundingRectangle(func1[2], buff=.1, color=WHITE)))
        self.wait(5)
        short_func = (MathTex(r"x_{i+1} = x_{i} + v_{i} * dt,", r"v_{i+1} = v_{i} + a * dt", color=RED)
                      .next_to(title, DOWN))
        self.play(FadeOut(explanation),
                  FadeOut(explanation2),
                  FadeOut(framebox),
                  Transform(func1[0], short_func[0]),
                  Transform(func1[2], short_func[1]))
        func2 = (MathTex(r"x_{i+1} = x_{i} + v_{i} * dt", r", ", r"v_{i+1} = v_{i} + a * dt", color=BLUE)
                 .next_to(func1, DOWN))
        self.play(FadeIn(func2, shift=DOWN))

        # Объяснение откуда берётся Полу-Эйлер
        explanation = Tex(r"Now let's see how we can get Semi-Eulerian").next_to(func2, DOWN)
        self.play(Write(explanation, run_time=2))
        self.wait(2)
        explanation2 = Tex(r"The order of those two equations\\does not change the result").next_to(
            explanation, DOWN)
        new_func2 = MathTex(r"v_{i+1} = v_{i} + a * dt", r", ", r"x_{i+1} = x_{i} + v_{i} * dt", color=BLUE).next_to(
            func1, DOWN)
        self.play(Transform(func2[0], new_func2[2]),
                  Transform(func2[2], new_func2[0]),
                  Transform(func2[1], new_func2[1]),
                  Write(explanation2, run_time=3))
        self.wait(3)
        new_func2 = MathTex(r"v_{i+1}", r" = v_{i} + a * dt, x_{i+1} = x_{i} + ", r"v_{i}", " * dt",
                            color=BLUE).next_to(func1, DOWN)
        explanation3 = Tex(r"But if we calculate velocity first,\\we can update position with a new velocity").next_to(
            explanation2, DOWN)
        framebox = SurroundingRectangle(new_func2[0], buff=.1, color=WHITE)
        self.play(FadeOut(func2), FadeIn(new_func2), FadeIn(framebox), Write(explanation3, run_time=2))
        func2 = new_func2
        self.wait(2)
        new_func2 = (MathTex(r"v_{i+1}", r" = v_{i} + a * dt, x_{i+1} = x_{i} + ", r"v_{i+1}", " * dt",
                             color=BLUE)
                     .next_to(func1, DOWN))
        self.play(Transform(framebox, SurroundingRectangle(func2[2], buff=.1, color=WHITE)))
        self.play(Transform(func2, new_func2),
                  Transform(framebox, SurroundingRectangle(new_func2[2], buff=.1, color=WHITE)))

        new_func2 = MathTex(r"v_{i+1}", r" = v_{i} + a * dt, x_{i+1} = x_{i} + ", r"(v_{i} + a * dt)", " * dt",
                            color=BLUE).next_to(func1, DOWN)
        self.wait(2)
        self.play(Transform(func2, new_func2),
                  Transform(framebox, SurroundingRectangle(new_func2[2], buff=.1, color=WHITE)))
        self.wait(1)
        self.play(FadeOut(explanation), FadeOut(explanation2), FadeOut(explanation3), FadeOut(framebox))

        explanation = Tex(r"This is how we get Semi-Eulerian method").next_to(func2, DOWN)
        self.play(Write(explanation, run_time=2))
        explanation2 = Tex(r"Let's compare this two \\with some dt values").next_to(explanation, DOWN)
        self.play(Write(explanation2, run_time=2))
        self.wait(2)

        # Переход в 3д для визуализации
        phi, theta, focal_distance, gamma, distance_to_origin = self.camera.get_value_trackers()
        axes = ThreeDAxes()
        sphere = Sphere(center=sun, radius=0.2, resolution=(18, 18))
        sphere.set_color(YELLOW)

        rect_e = Rectangle(width=3.0, height=1.2, fill_opacity=0.2).shift(np.array([2., 5., -0.99]))
        text_e = Tex(f"Euler", color=RED).shift(np.array([2., 5., -1.]))

        rect_se = Rectangle(width=3.0, height=1.2, fill_opacity=0.2).shift(np.array([2., 3.5, -0.99]))
        text_se = Tex(f"Semi-Euler", color=BLUE).shift(np.array([2., 3.5, -1.]))

        self.play(phi.animate.set_value(40 * DEGREES),
                  theta.animate.set_value(-60 * DEGREES),
                  FadeOut(explanation),
                  FadeOut(explanation2),
                  FadeOut(title),
                  Transform(func1, text_e),
                  Transform(func2, text_se),
                  FadeIn(sphere),
                  FadeIn(axes),
                  FadeIn(rect_e),
                  FadeIn(rect_se))

        def trajectory(x0, v0, dt, color=RED, f=simulate_euler):
            """
            Собирает анимационную группу кривой по входным данным и функции симуляции
            """
            tF, xF, vF = f(x0, v0, dt)

            curve = []

            for i in range(0, len(tF) - 1, max(1, int(RENDER_LINE_CLUMP / dt))):
                curve.append(Line(start=np.array(xF[:, i]),
                                  end=np.array(xF[:, min(i + max(1, int(RENDER_LINE_CLUMP / dt)), len(tF) - 1)]),
                                  color=color))

            curve = VGroup(*curve)
            return curve

        # dt на которых запускам симуляции
        dts = [1, 0.5, 0.25, 0.1, 0.05, 0.01, 0.001]
        #dts = [1, 0.9]

        c = [trajectory(np.array([2., 0., 2.]), np.array([0., 5., 0.]), dt) for dt in dts]

        h = [trajectory(np.array([2., 0., 2.]), np.array([0., 5., 0.]), dt, f=simulate_half_euler, color=BLUE) for dt in
             dts]

        # Индикатор для смены dt
        rect = Rectangle(width=3.0, height=1.2, fill_opacity=0.2).shift(np.array([2., -2., -0.99]))
        dt_counter = Tex(f"dt = ", f"{dts[0]}").shift(np.array([2., -2., -1.]))
        self.wait(1)
        self.play(Write(dt_counter), FadeIn(rect))
        self.wait(1)
        self.play(Write(c[0], lag_ratio=1), Write(h[0], lag_ratio=1))
        for i in range(0, len(c) - 1):
            self.play(FadeOut(c[i]),
                      FadeOut(h[i]))
            self.play(Wiggle(rect, run_time=0.5),
                      Transform(dt_counter, Tex(f"dt = ", f"{dts[i + 1]}").shift(np.array([2., -2., -1.])),
                                run_time=0.5))
            self.wait(1)
            self.play(Write(c[i + 1], lag_ratio=1, run_time=4), Write(h[i + 1], lag_ratio=1, run_time=4))
            self.wait(2)

        self.wait(5)
        # Завершающей мысли нет, картинка говорит сама за себя :D
