# Симуляция тканей при помощи PBD

***Position Based Dynamics*** как метод основывается на описании и поддержании "ограничений" системы

Основной подход выглядит так: [(референс)](https://matthias-research.github.io/pages/publications/posBasedDyn.pdf)

```
forall vertices i
  initialize xi = x, vi = v
endfor
loop
  forall vertices i do vi ← vi +∆twifext(xi)
  dampVelocities(v1,...,vN)
  forall vertices i do pi ← xi +∆tvi
  forall vertices i do generateCollisionConstraints(xi → pi)
  loop solverIterations times
    projectConstraints(C1,...,CM+Mcoll ,p1,...,pN)
  endloop
  forall vertices i
    vi ← (pi −xi)/∆t
    xi ← pi
  endfor
  velocityUpdate(v1,...,vN)
endloop
```

В данном методе перед Полу-Эйлером применяется некоторый солвер констрайнов - метод который итерирует через все ограничения и наивно их разрешает. 
После нескольких итераций управление передаётся Полу-Эйлеру, и, в самом конце, вызывается *velocityUpdate*, который модифицирует вектор скоростей
на основе информации из солвера констрейнов (например можно добавлять упругий отскок для материальных точек)

Такой подход позволяет описать как расстояние между частицами (которое мы используме для симуляции поверхностей и тел), так и колижены, в явном
виде указав что частица не должна находиться внутри тела и в случае проникновения - проецировалась на поверхность.
