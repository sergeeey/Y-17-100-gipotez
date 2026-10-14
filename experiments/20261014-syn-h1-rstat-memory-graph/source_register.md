# source_register.md — FL Step -4 (Source Trace)

Дата: 2026-10-14. Метод: arXiv (search_papers, полные аннотации) + OpenAlex/Crossref (метаданные). **Читались аннотации, не полные тексты** → максимум `[VERIFIED-ABSTRACT]`, не `[VERIFIED-FULLTEXT]`. Firecrawl-поиск недоступен (402, кредиты).

| # | Claim отчёта / проекта | Статус | Источник (поисковый след) |
|---|---|---|---|
| 1 | Poisson ⟨r̃⟩=2ln2−1≈0.3863 | `[VERIFIED]` аналитически + моя симуляция 0.3852 | Atas et al., arXiv:1212.5611 (аннотация: распределение отношения зазоров, без зависимости от плотности состояний); симуляция N=400 |
| 2 | GOE ≈0.5307, GUE ≈0.5996 (large-N) | `[VERIFIED]` моей симуляцией: 0.5312 / 0.5992; surmise 3×3: 0.5359 / 0.6027 | Atas et al.; Buijsman arXiv:2508.14172 (аннотация: эталонные значения получены численно на больших конечных матрицах) |
| 3 | Спектр лапласиана сетей следует GOE; переход Poisson→GOE при росте случайности | `[VERIFIED-ABSTRACT]` | Jalan & Bandyopadhyay, cond-mat/0611735 («Random matrix analysis of network Laplacians»): random/scale-free/small-world → GOE; переход к GOE на small-world-переходе |
| 4 | Ratio-статистика на сетях | `[VERIFIED-ABSTRACT]` | Mishra, Raghav, Jalan, arXiv:2206.01418: ratio-статистика моделей сетей, GOE → Poisson при диагональном беспорядке |
| 5 | Poisson в разреженных сетях зависит от связности, не только от «структуры» | `[VERIFIED-ABSTRACT]` | Shekhar et al., arXiv:2609.04152: «In sparse networks, weak level repulsion produces Poisson statistics regardless of directionality… unfolding is unreliable, spacing-ratio statistics provide an unfolding-free characterization» |
| 6 | Ratio-статистика графа как детектор режима/событий | `[VERIFIED-ABSTRACT]` | тот же arXiv:2609.04152: применение к графам S&P 500, GOE→GUE кроссовер при крахах |
| 7 | Poisson→GOE переход зависит от размера матрицы | `[VERIFIED-ABSTRACT]` | Chavda, Deota, Kota, arXiv:1405.6321: параметр перехода Λ ∼ λ²d |
| 8 | Спектральные статистики геометрических графов (kNN-граф эмбеддингов — родственный объект) | `[VERIFIED-ABSTRACT]` | Dettmann, Georgiou, Knight, arXiv:1608.01154: зависящий от параметра переход Poisson↔GOE; зазоры «дают информацию о локализации, уровне сообществ, уровне случайности» |
| 9 | Спектральная/RMT-детекция отравления памяти или RAG | **не найдено** — `[WEAK]` (отсутствие) | 5 запросов arXiv (RAG poisoning × spectral/graph; agent memory poisoning × graph structure; RMT × text-embedding graph anomaly; spectral Laplacian × data poisoning); в выдаче много работ 2026 по отравлению памяти (ShadowMerge 2605.09033, Oracle Poisoning 2605.09822, 2606.04329, 2610.13267, …), ни одной со спектральным детектором. Поле плотное и быстрое → отсутствие слабое доказательство |
| 10 | «Frontier R&D Research Document» как источник | `[UNVERIFIED]` постоянно | `CLAUDE.md` проекта: нигде не найден, не строить выводы |
| 11 | «Детектирует на 2–3 шага раньше guardrails» | `[UNKNOWN]` — основания в отчёте нет, сравнений нет | — |

Следствие для эксперимента: пункты 3–8 подтверждают, что **режим ⟨r̃⟩ определяется связностью/разреженностью/структурой сообществ графа** — это не контраргумент, а прямая причина, по которой база S3 может зависеть от построения графа (A1). Пункт 5 предсказывает, что разреженный kNN-граф даст Poisson-подобную базу независимо от «семантики памяти».
