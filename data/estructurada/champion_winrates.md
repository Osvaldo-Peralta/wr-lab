# Win rates del roster — wr-meta (Meta Overview)

> Bucket: **Diamond +** · Datos wr-meta: **Updated 18 OCT 2026 UTC 00:00** · Refrescado por el vigía: 18/10/2026
> Fuente: `wr-meta.com/{id}-{champ}.html` (bloque Meta Overview) vía
> `model/check_patch.py` paso 4 — el MISMO proceso que busca parches nuevos (cron 2×/día
> en `patch-watch.yml`, o manual: `python3 wrlab.py winrates`).
> **Los callouts "Estado Meta Actual" de los reportes se toman de aquí** (TEMPLATE §A.1);
> alerta del vigía si un campeón se mueve ≥ 2 pts de win rate.

| Campeón | Rol | Tier | Win % | Pick % | Ban % | Tendencia | Confianza |
|---|---|---|---|---|---|---|---|
| Ahri | MID | S | 51.38 | 4.45 | 0.14 | ↑ 2 | Confidence Med |
| Caitlyn | DUO | A | 49.85 | 16.30 | 6.21 | ↑ 2 | Confidence High |
| Cho'Gath | SOLO | S+ | 50.57 | 9.79 | 36.27 | ↑ 5 | Confidence High |
| Cho'Gath | JUNGLE | S | 50.15 | 8.52 | 36.27 | ↓ 1 | Confidence High |
| Diana | MID | B | 47.18 | 1.06 | 0.15 | ↓ 1 | Confidence Low |
| Diana | JUNGLE | A | 49.85 | 1.41 | 0.15 | ↓ 4 | Confidence Low |
| Heimerdinger | MID | A | 49.83 | 1.63 | 1.38 | ↓ 1 | Confidence Low |
| Jinx | DUO | S | 51.01 | 12.64 | 0.49 | ↑ 2 | Confidence High |
| Kalista | DUO | A | 50.79 | 6.27 | 8.10 | ↓ 1 | Confidence Med |
| Kalista | SOLO | S+ | 53.71 | 2.49 | 8.10 | 0 | Confidence Low |
| Karma | SUPPORT | A | 50.01 | 4.45 | 0.37 | ↓ 6 | Confidence Med |
| Malphite | SUPPORT | S+ | 51.63 | 9.28 | 41.74 | ↑ 1 | Confidence High |
| Malphite | SOLO | S+ | 54.78 | 7.17 | 41.74 | 0 | Confidence Med |
| Mordekaiser | SOLO | S | 51.00 | 11.07 | 30.66 | ↑ 1 | Confidence High |
| Nocturne | JUNGLE | S+ | 52.52 | 7.14 | 58.32 | ↓ 1 | Confidence Med |
| Norra | MID | A | 50.00 | 1.49 | 6.86 | ↑ 1 | Confidence Low |
| Orianna | MID | S | 51.98 | 4.37 | 0.30 | ↑ 9 | Confidence Med |
| Ornn | SOLO | A | 51.03 | 1.79 | 0.18 | ↓ 2 | Confidence Low |
| Ornn | SUPPORT | A | 49.78 | 1.26 | 0.18 | ↑ 6 | Confidence Low |
| Rammus | JUNGLE | S+ | 56.56 | 3.89 | 6.89 | 0 | Confidence Med |
| Senna | DUO | A | 49.08 | 1.01 | 22.45 | ↓ 9 | Confidence Low |
| Senna | SUPPORT | A | 49.41 | 8.08 | 22.45 | ↓ 10 | Confidence High |
| Seraphine | SUPPORT | A | 49.88 | 6.40 | 1.05 | ↑ 1 | Confidence Med |
| Shyvana | JUNGLE | B | 46.64 | 3.38 | 1.06 | ↑ 1 | Confidence Med |
| Sivir | DUO | B | 48.64 | 3.72 | 0.06 | ↓ 2 | Confidence Med |
| Syndra | MID | S+ | 51.87 | 5.91 | 19.15 | 0 | Confidence Med |
| Volibear | SOLO | A | 48.79 | 8.93 | 8.35 | ↓ 1 | Confidence High |
| Volibear | JUNGLE | A | 48.61 | 4.60 | 8.35 | ↓ 1 | Confidence Med |
| Xayah | DUO | A | 50.33 | 4.87 | 0.19 | ↑ 1 | Confidence Med |
| Yunara | DUO | A | 49.06 | 7.46 | 18.62 | ↓ 6 | Confidence Med |
| Yuumi | SUPPORT | A | 47.73 | 8.56 | 33.89 | ↓ 1 | Confidence High |

Roles wr-meta: SOLO = top (Baron Lane) · JUNGLE · MID · DUO = ADC (Dragon Lane) · SUPPORT.
Máquina: `champion_winrates.csv` (mismas filas) · BD: tabla `winrates` (`build_db.py`).
Dato de CONTEXTO meta (secundario): no cambia builds por sí solo — si un movimiento
coincide con un hotfix, el flujo es el de FRAMEWORK §E (triage/annotate).
