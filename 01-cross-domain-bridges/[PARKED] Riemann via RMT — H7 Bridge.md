# [PARKED] Гипотеза Римана через RMT — H-7 Bridge Paper

**Статус:** PARKED — возобновить после GeoScan blind test (после 20.06.2026)  
**Оценка:** ⭐⭐⭐⭐⭐ потенциал в области, НЕ решение задачи Clay  
**Время на разведку:** 2-3 часа кода

---

## Идея

H-7 уже вычисляет r-статистику Вигнера-Дайсона на биологических матрицах.  
Нули Римана следуют GUE = то же распределение (Montgomery 1972, Odlyzko 1987).  
→ Сравнить напрямую. Найти Δ. Опубликовать bridge paper.

**Не "решить Римана" — а "найти новый класс систем с тем же спектральным поведением".**

---

## Конкретный план (2-3 часа)

```python
# Шаг 1: Скачать данные Odlyzko
# https://odlyzko.com/zeta_tables/ — первые 10^6 нулей, публично
# Файл: zeros1 (ASCII, ~8MB)

# Шаг 2: Вычислить r-статистику (тот же код что в H-7)
import numpy as np
zeros = np.loadtxt('zeros1')
spacings = np.diff(zeros)
# нормализовать на среднее
spacings_norm = spacings / spacings.mean()
r = np.minimum(spacings_norm[:-1], spacings_norm[1:]) / \
    np.maximum(spacings_norm[:-1], spacings_norm[1:])
r_mean = r.mean()  # GUE теория: ~0.6027

# Шаг 3: Сравнить с нашими Hi-C матрицами из H-7
# r_mean биологический vs r_mean Риман → Δ = ?

# Шаг 4: Если Δ интересный → статья
# "Wigner-Dyson universality in chromatin organization 
#  mirrors Riemann zero spacing statistics"
```

---

## Второй шаг (если первый красивый)

Написать Tom Lawrence — он работает с Yang-Mills (тоже Clay) через Covariant Compactification.  
Потенциал: соавторство bridge paper математика + биолога + физика.

---

## Связанные заметки
- [[knowledge/research/Задачи тысячелетия — связь с H-7 и RMT]] — полный анализ
- [[knowledge/people/Tom Lawrence]] — потенциальный соавтор
- [[projects/H-7 GeoSpectra Lab]] — исходный код r-статистики

---

*Создано: 2026-05-28 | PARKED до: после GeoScan blind test (20.06.2026)*  
*Причина паузы: GeoScan = первый клиент. Риман подождёт — он ждёт уже 165 лет.*
