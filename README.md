# Коллекция примеров симуляции физики
Все  примеры реализованы на python и не претендуют на оптимальность выше чем асимптотическую. 
В каждом примере есть небольшое описание как запускать проект.
В репозитории есть несколько типов симуляций
 - Симуляции с использованием matplotlib. Для запуска достаточно импортировать нужные библиотеки из requairments.txt 
 - Симуляции с использованием Manim. О установке и запуске рендера на manim можно прочитать [тут](https://docs.manim.community/en/stable/installation.html) 
 
 К каждому примеру есть небольшой _jupyter notebook_, который при желании можно открыть и использовать отдельно от всего для демонстрации симуляций. Рендеры можно посмотреть в /bin соответствующей анимации

# VectorFieldOfTheSpring

Аналитическое решение задачи о теле на пружине. С визуализациями векторного пространства при и без демпинга.

<img src='https://github.com/Boyarnikov/physics_simulation_examples/blob/main/VectorFieldOfTheSpring/bin/StandartCaseSpring.png' width='400'> <img src='https://github.com/Boyarnikov/physics_simulation_examples/blob/main/VectorFieldOfTheSpring/bin/DempingCaseSpring.png' width='400'>

# EulerMethodVisualizations

Визуализация итеративного решения задачи симуляции материальной точки.

Сравнение Эйлера, Обратного-Эйлера, Полу-Ейлера. Влияние коофицента $Δt$ на сходимость, сравнение этого влияния на разные методы.

[![Euler Trajectory](https://img.youtube.com/vi/MI4oBvl97fQ/0.jpg)](https://www.youtube.com/watch?v=MI4oBvl97fQ) [![Euler Trajectory](https://img.youtube.com/vi/4lyrtohI2Qo/0.jpg)](https://www.youtube.com/watch?v=4lyrtohI2Qo)

# VerletSpingCloth

Вывод метода Верле из Полу-Эйлера. Симуляция ткани и мягких тел с использованием пружин и материальных точек.

<img src='https://github.com/Boyarnikov/physics_simulation_examples/blob/main/VerletSpingCloth/bin/Falling_clothes.gif' width='400'><img src='https://github.com/Boyarnikov/physics_simulation_examples/blob/main/VerletSpingCloth/bin/Clothes_in_cilinder_with_a_push.gif' width='400'><img src='https://github.com/Boyarnikov/physics_simulation_examples/blob/main/VerletSpingCloth/bin/Clothes_with_wind.gif' width='400'> <img src='https://github.com/Boyarnikov/physics_simulation_examples/blob/main/VerletSpingCloth/bin/Clothes_in_cilinder_with_wind.gif' width='400'>
