import itertools
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

"""
Визуализация векторного поля демпинг случая

В аналитических решениях нам достаточно построить дифференциальное уравнение
Для пружины имеем F = x''(t) * m = -k * x + -b * x'(t)
Тогда получаем дифференциальное уравнение вида x = x''(t) * -m/k + x'(t) * -b/k
"""
x = sp.Function('x')
t, k, m, b = sp.symbols('t, k, m, b')
eq = sp.Eq(k*x(t), -m * x(t).diff(t,t) - b * x(t).diff(t))

sol_eq = sp.dsolve(eq).subs({k: 1, m: 1, b: 0.5})

sol_x = sol_eq.rhs
sol_dx = sp.diff(sol_x, t)
sol_ddx = sp.diff(sol_x, t, t)

x, y, dx, dy = [], [], [], []
for x0, dx0 in itertools.product(list(np.linspace(-10, 10, 40)), list(np.linspace(-10, 10, 40))):
    position = sp.solve([sol_x.subs(t, 0) - x0, sol_x.diff(t).subs(t, 0) - dx0])

    x.append(float(sol_x.subs(position).subs(t, 0)))
    y.append(float(sp.re(sol_dx.subs(position).subs(t, 0))))
    dx.append(float(sp.re(sol_dx.subs(position).subs(t, 0))))
    dy.append(float(sp.re(sol_ddx.subs(position).subs(t, 0))))

fig, ax = plt.subplots()
ax.quiver(x, y, dx, dy)
fig.set_figwidth(8)
fig.set_figheight(8)
plt.show()