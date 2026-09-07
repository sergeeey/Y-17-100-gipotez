# Archive: skeptic-sweep part 2 (5th, 6th, 7th passes + H-B3-1m power fix)

Archived 2026-09-07 from `.claude/memory/activeContext.md` to keep that file under the
Checkpoint Fidelity line budget. Full detail lives in the referenced ADRs (`.claude/memory/decisions.md`)
and each experiment's own `decision.md`/`null_results/` entry — this file preserves the
condensed narrative that was in activeContext.md before archival.

---

**[WS: пятый skeptic-проход подряд, самый строгий] H-B2-1h REJECTED (ADR-054):** skeptic на
**математический факт**: для нильпотентного N (N⁸=0), M1(c) ДОКАЗУЕМО полином степени ≤7 —
истинная экспонента алгебраически НЕВОЗМОЖНА. Уже задокументированное замедление отношений
(3.76→1.80) оказалось эмпирической сигнатурой именно этого факта, не второстепенной оговоркой.
Вердикт CONFIRMED→REJECTED, статус confirmed→killed. Практически важный вопрос pearl impact 9
переоткрыт — этот скан тестировал другой, более узкий вопрос. Итог 5 подряд skeptic-проходов:
5/5 нашли реальные проблемы, разброс от мягкого до математически безапелляционного.
**[WS: fifth skeptic pass] CLOSED.**

**[WS: шестой skeptic-проход, первый на мосте B3] H-B3-1l дальше WEAKENED (ADR-055):** skeptic
на H-B3-1l (peak-tau TDA vs classical). Нашёл 2: (1) правдоподобный механизм для конфаунда
негативных контролей (argmax структурно смещён к раннему индексу, РАЗНО для гладких classical и
«дёрганых» TDA-статистик) — не подтверждён эмпирически; (2) **независимо проверено против
committed data**: `classical_ac1_peak_date=1999.25` — ДО `tda_betti_peak_date=2000.5` — AC1
САМ ПО СЕБЕ уже обходит TDA, скрыто асимметричным правилом выбора classical-статистики
(oracle-informed для позитивного случая, «раньше из двух» для негативных). Вердикт WEAKENED
сильнее, чем оригинальный самопойманный конфаунд подразумевал. 2 новых pearl-записи. Итог 6
подряд skeptic-проходов: 6/6 нашли реальные проблемы на ДВУХ разных мостах (B2 и B3) — не
специфично одному стилю эксперимента. **[WS: sixth skeptic pass] CLOSED.**

**[WS: седьмой, ПОСЛЕДНИЙ skeptic-проход] H-B3-1m CRITERION_INVALID → UNRESOLVED AT CURRENT
POWER (ADR-056):** skeptic на H-B3-1m (two-part tau+Pettitt rule). Самая серьёзная находка всего
скана, независимо перепроверена вычислением: claim.md's механизм-обоснование («Pettitt ловит
level-shift, не тренд») ЛОЖНО — K=n²/4 точно для чистого монотонного тренда без шума (n=30 →
K=225.0=предсказание, p≈3.7e-5), AND-gate не даёт заявленной специфичности. Плюс: reps=30 даёт
95%-CI±18пп, порог 50% внутри шума — Loch Leven (53.3%) vs Windermere (33.3%) неразличимы;
общий seed=0 коррелирует суррогаты трёх озёр. graph.yaml evidence→CONFLICT, kill_criterion
переписан. **Итог СЕМИ подряд skeptic-проходов: 7/7 нашли реальные проблемы**, диапазон от
мягкого до математически/вычислительно безапелляционного, на ОБОИХ мостах (B2, B3). Систематический
skeptic-скан флагованных экспериментов ЗАВЕРШЁН. **[WS: seventh and final skeptic pass] CLOSED.**

**[WS: H-B3-1m power-фикс, прямое следствие ADR-056] REJECT финально (ADR-057):** установлен
`pyhomogeneity`, `pettitt_test` сверена — K/U совпадает точно на 7 случаях, реализация без ошибок
(Finding 5 DISMISSED); побочно — ВТОРОЕ независимое подтверждение Finding 1 (сторонний пакет тоже
помечает чистый тренд как значимый). `run.py`: reps 30→500, раздельный seed на озеро. Floor
резолвится чисто: Lower Zurich 44.0%, Windermere 42.8%, Loch Leven 41.6% (все CI<50%) — но именно
это открыло Step 2 критерия впервые: Loch Leven реально two-part-crosses на СВОИХ данных (не
только AR(1)-нуле) — истинный false positive. Вердикт UNRESOLVED→**REJECT**. Kill Analysis,
`null_results/H-B3-1m-…md`, graph.yaml status killed/evidence VERIFIED-REAL. **ЗАКРЫВАЕТ ВСЕ 3
пункта Relaxation Map H-B3-1b окончательно** (Row1 REJECT, Row2 REJECT, Row3 CONFIRMED-с-
конфаундом) — ни один чистый PROMOTE. **[WS: H-B3-1m power fix] CLOSED.**
