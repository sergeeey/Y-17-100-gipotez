---
title: Distribution-free bound (Markov / Chernoff) для Skeptic Engine
type: methodology
source: Bilinsky NGN radiotherapy paper (SSRN/Zenodo, 2026)
relevance: skeptic-engine-anomaly-layer
date: '2026-06-06'
tags:
  - methodology
  - skeptic-engine
  - statistics
  - concentration-inequalities
  - distribution-free
---
maturity: fleeting
# Distribution-free bound для Skeptic Engine

> Дистиллировано из NGN-статьи Lydia Bilinsky (2026-06-06).
> Главный переносимый приём для проекта Skeptic Engine.

---

## Источник приёма

Bilinsky выводит tumor control probability как TCP не меньше чем 1 минус Xf через НЕРАВЕНСТВО МАРКОВА. Явно подчёркивает: эта граница НЕ опирается на форму распределения финального числа клеток (не нужно предполагать Poisson или что-либо ещё).

То есть: гарантированная вероятностная граница БЕЗ модели распределения данных.

## Почему это прямо проблема Skeptic

В сессии 2026-06-05 golden-set harness показал [VERIFIED-REAL]:
- H24 Benford на синтетике AUC 0.978.
- H24 Benford на реальном credit card fraud AUC 0.586 (почти рандом).

Причина провала: Benford ПРЕДПОЛАГАЕТ конкретное распределение (закон первой цифры). На реальных данных распределение было другим, метод рухнул.

Distribution-free границы (Markov, Chebyshev, Chernoff) этой ошибки не делают по построению. Они верны при ЛЮБОМ распределении.

## Связка с собственным кодом

- Проект MarkovChains содержит chernoffpy с модулем certified.py - семейство концентрационных неравенств (Chernoff тоньше Маркова).
- Контур: Bilinsky показывает силу distribution-free границы. ChernoffPy даёт сертифицированную (более тугую) версию. Skeptic получает слой "насколько статистически невозможны эти данные" с доказуемой границей, устойчивый там, где Benford ломается.

## Trade-off (честно)

- Маркова граница самая слабая (часто бесполезно тугая). Сила только в distribution-free гарантии.
- Benford противоположный полюс: мощный, но хрупкий (нужно ровно то распределение).
- Выбор: "сильное предположение, хрупкий результат" против "слабое предположение, робастная граница".

## Следующий эксперимент

Добавить в Skeptic distribution-free anomaly layer на базе chernoffpy certified.py: граница "вероятность увидеть такое отклонение не больше X" без предположения о распределении. Прогнать на том же реальном fraud-датасете рядом с Benford.

- Гипотеза: distribution-free слой не упадёт до 0.586, потому что не зависит от формы распределения.
- Контроль: Benford на тех же данных.
- Опровергается если: distribution-free AUC не лучше 0.586.
- Estimand caveat: credit card fraud это чужая популяция для Skeptic. Правильный golden-set это реальный научный fraud (retracted статьи). Сначала достать его.

## Вторичные приёмы из той же статьи (слабее)

- Upper-envelope как консервативная граница: брать max по гетерогенным под-популяциям (слоям) даёт доказуемый верхний предел. Перенос на tier-структуру данных Skeptic.
- Рефрейм "два процесса в один": методологический first-principles приём, к Skeptic не привязывается напрямую.

---

## Связи

- [[Lydia Bilinsky]] — автор источника (NGN-статья), узел Ronin-сети.
- [[AI в науке — потолок и реальная сила 2026]] — общий контекст: где методы реально работают, а где theater.
- [[Nature 2026 — analytical robustness (multi-analyst)]] — про устойчивость выводов к выбору метода (тот же мотив: хрупкое предположение против робастной границы).
