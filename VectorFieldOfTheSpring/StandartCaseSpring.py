import itertools
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

"""
Визуализация векторного поля стандартного случая

В аналитических решениях нам достаточно построить дифференциальное уравнение
Для пружины имеем F = x''(t) * m = -k * x
Не теряя общности, предположим, что m/k = 1.
Тогда получаем дифференциальное уравнение вида x = x''(t)
"""

x = sp.Function('x')
t, k, m = sp.symbols('t, k, m')
eq = sp.Eq(x(t).diff(t, t) * k, x(t) * -m)

sol_eq = sp.dsolve(eq).subs({k: 1, m: 1})

sol_x = sol_l = sol_eq.rhs
sol_dx = sp.diff(sol_l, t)
sol_ddx = sp.diff(sol_l, t, t)


x, y, dx, dy = [], [], [], []
for x0, dx0 in itertools.product(list(np.linspace(-10, 10, 40)), list(np.linspace(-10, 10, 40))):
    position = sp.solve([sol_x.subs(t, 0) - x0, sol_x.diff(t).subs(t, 0) - dx0])

    x.append(float(sol_l.subs(position).subs(t, 0)))
    y.append(float(sp.re(sol_dx.subs(position).subs(t, 0))))
    dx.append(float(sp.re(sol_dx.subs(position).subs(t, 0))))
    dy.append(float(sp.re(sol_ddx.subs(position).subs(t, 0))))

fig, ax = plt.subplots()
ax.quiver(x, y, dx, dy)
fig.set_figwidth(8)
fig.set_figheight(8)

plt.show()
