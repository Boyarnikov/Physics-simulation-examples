# Симуляция тканей при помощи метода Верле
Вспомним метод Полу-Эйлера
```math
v_{i+1}  = v_{i} + {F/m} \cdot Δt
```
```math
x_{i+1}  = x_{i} + v_{i+1} \cdot Δt
```
Можем заметить что в действительности мы можем обойтись без $v_i$ если у нас сохранён $x_{i-1}$
```math
x_{i}  = x_{i-1} + v_{i} \cdot Δt
```
```math
v_{i}  = (x_{i} - x_{i-1}) / Δt
```
Воспользовавшись этим можем получить метод Верле 
```math
x_{i+1}  = x_{i} + v_{i+1} \cdot Δt
```
```math
x_{i+1}  = x_{i} + (v_{i} + {F/m} * Δt) \cdot Δt
```
```math
x_{i+1}  = x_{i} + ((x_{i} - x_{i-1}) / Δt + {F/m} \cdot Δt) \cdot Δt
```
```math
x_{i+1}  = 2x_{i} - x_{i-1} + {F/m} \cdot Δt^2
```
Или, в случае демпинга
```math
\dot{z} =
    \begin{bmatrix}
        0 & 1 \\
        -\omega_0^2 & -2d\omega_0 
    \end{bmatrix}
    \cdot z = A \cdot z
```
```math
z_{k+1} = (I + A\cdot\Delta t)\cdot z_k = F\cdot z_k
```
```math
x_{i+1}  = 2x_{i} - x_{i-1} + (- w^2 x_i - dw(x_i-x_{i-1} ))Δt^2
```
Для
```math
d = \frac{c}{2 \sqrt{km}},   \omega_0 = \sqrt{\frac{k}{m}}
```
Тогда, просуммировав по всем пружинам силы $F = -kΔx$  и собрав их в ускорение $a = F/m$ получим
```math
x_{i+1}  = 2x_{i} - x_{i-1} + (-k/m \cdot x_i -c/2m\cdot (x_i-x_{i-1} ))Δt^2
```
```math
x_{i+1}  = 2x_{i} - x_{i-1} + aΔt^2 - (c/2m\cdot (x_i-x_{i-1} ))Δt^2
```
```math
x_{i+1}  = 2x_{i} - x_{i-1} + aΔt^2 - (c/2m\cdot (x_i-x_{i-1} ))Δt^2
```
```math
x_{i+1}  = x_{i} +  (x_{i} - x_{i-1})(1 - c/2mΔt^2) + aΔt^2
```

# Ткань

Имея этот минимальный блок в виде материальной точки и пружин - мы уже можем собрать интересные симуляции! 
Для этого соберём "каркас" ткани в виде сетки точек, а затем соединим все четыре точки в ячейке. Результатом в пределе будет ткань, а при достаточном количестве точек - хорошая физическая аппроксимация.

Для симуляции силы тяжести можно ко всем точкам добавить $F = mg$

![pic](https://i.imgur.com/vYGJjvq.png)

Для построения визуализаций есть VerletSpringCloth.ipynb, в котором подробно описаны шаги и приведено несколько примеров. 

Так же есть более оптимизированный пример main.py на массивах numpy (всё ещё очень медленный из-за рендера, но демонстрирующий что всё вычисляется на матрицах точек)

![](https://github.com/Boyarnikov/physics_simulation_examples/blob/main/VerletSpingCloth/bin/Falling_clothes.gif)

Из интересного: метод всё ещё требует достаточно низкого $Δt$ чтобы сходиться. Однако при правильном подборе дампинга даже сложные замкнутые структуры не расходятся.

![](https://github.com/Boyarnikov/physics_simulation_examples/blob/main/VerletSpingCloth/bin/Clothes_in_cilinder_with_a_push.gif)

Можно так же добавить любые другие силы, например сила ветра $F(x, t)$ которая семплится из неприрывного 4d шума:
![](https://github.com/Boyarnikov/physics_simulation_examples/blob/main/VerletSpingCloth/bin/Clothes_with_wind.gif)

Все рендеры можно посмотреть в [/bin](https://github.com/Boyarnikov/physics_simulation_examples/tree/main/VerletSpingCloth/bin)
