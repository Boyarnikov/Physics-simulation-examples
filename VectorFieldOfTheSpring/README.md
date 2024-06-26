
# Визуализация векторного поля стандартного случая и демпинга
  
В аналитических решениях нам достаточно построить дифференциальное уравнение. 
Для пружины имеем:
$F = x''(t) * m = -k * x$
  
Не теряя общности, предположим, что m/k = 1.  
Тогда получаем дифференциальное уравнение вида x = x''(t)  
  
$k \frac{d^{2}}{d t^{2}} x{\left(t \right)} = - m x{\left(t \right)}$

$x{\left(t \right)} = C_{1} e^{- i t} + C_{2} e^{i t}$ для $k/m = 1$

Для демпинга исходная пружина будет выглядеть как:
$F = x''(t) * m = -k * x + -b * x'(t)$

Получим 
$k x{\left(t \right)} = - b \frac{d}{d t} x{\left(t \right)} - m \frac{d^{2}}{d t^{2}} x{\left(t \right)}$

$x{\left(t \right)} = C_{1} e^{\frac{t \left(-0.5 + 1.93649167310371 i\right)}{2}} + C_{2} e^{- \frac{t \left(0.5 + 1.93649167310371 i\right)}{2}}$
 
 StandartCaseSpring.py и DampingCaseSpring.py рендерит векторные пространства из X, X'. Пример без демпинга даёт круговые траектории, так как без демпинга система будет колебаться бесконечно переводя энергию из кинетической в потенциальную. Во втором случае это спираль сходящаяся к центру, так как мы в явном виде симулируем потерю энергии в системе. (Генерация изображение занимает до двух минут, так как функция просчитывается во всех точках дискретного подпространства)

Случай без демпинга
![Случай без демпинга](bin/StandartCaseSpring.png)

Случай с демпингом
![Случай с демпингом](bin/DempingCaseSpring.png)
