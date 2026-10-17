# Win rates del roster — wr-meta (Meta Overview)

> Bucket: **Diamond +** · Datos wr-meta: **Updated 17 OCT 2026 UTC 00:00** · Refrescado por el vigía: 17/10/2026
> Fuente: `wr-meta.com/{id}-{champ}.html` (bloque Meta Overview) vía
> `model/check_patch.py` paso 4 — el MISMO proceso que busca parches nuevos (cron 2×/día
> en `patch-watch.yml`, o manual: `python3 wrlab.py winrates`).
> **Los callouts "Estado Meta Actual" de los reportes se toman de aquí** (TEMPLATE §A.1);
> alerta del vigía si un campeón se mueve ≥ 2 pts de win rate.

| Campeón | Rol | Tier | Win % | Pick % | Ban % | Tendencia | Confianza |
|---|---|---|---|---|---|---|---|
| Ahri | MID | A | 50.95 | 4.37 | 0.13 | 0 | Confidence Med |
| Caitlyn | DUO | A | 49.74 | 16.80 | 6.55 | ↓ 1 | Confidence High |
| Cho'Gath | SOLO | S | 50.39 | 10.22 | 36.00 | 0 | Confidence High |
| Cho'Gath | JUNGLE | A | 50.35 | 8.63 | 36.00 | ↓ 5 | Confidence High |
| Diana | MID | B | 47.83 | 1.05 | 0.15 | ↑ 1 | Confidence Low |
| Diana | JUNGLE | A | 50.46 | 1.42 | 0.15 | ↑ 2 | Confidence Low |
| Heimerdinger | MID | A | 50.10 | 1.63 | 1.35 | ↓ 6 | Confidence Low |
| Jinx | DUO | S | 50.82 | 12.63 | 0.46 | ↑ 1 | Confidence High |
| Kalista | DUO | S | 51.08 | 6.13 | 7.81 | ↑ 2 | Confidence Med |
| Kalista | SOLO | S+ | 53.77 | 2.50 | 7.81 | 0 | Confidence Low |
| Karma | SUPPORT | A | 50.74 | 4.39 | 0.34 | ↑ 7 | Confidence Med |
| Malphite | SUPPORT | S+ | 51.58 | 8.89 | 41.47 | 0 | Confidence High |
| Malphite | SOLO | S+ | 54.94 | 7.12 | 41.47 | 0 | Confidence Med |
| Malphite | MID | A | 50.04 | 1.01 | 41.47 | ↓ 2 | Confidence Low |
| Mordekaiser | SOLO | S+ | 51.02 | 11.00 | 30.52 | ↑ 2 | Confidence High |
| Nocturne | JUNGLE | S+ | 52.81 | 8.15 | 58.59 | ↓ 5 | Confidence High |
| Norra | MID | A | 50.10 | 1.37 | 6.79 | ↓ 7 | Confidence Low |
| Orianna | MID | S | 51.32 | 4.48 | 0.30 | ↑ 3 | Confidence Med |
| Ornn | SOLO | A | 51.48 | 1.85 | 0.18 | ↑ 9 | Confidence Low |
| Ornn | SUPPORT | B | 49.47 | 1.24 | 0.18 | ↓ 10 | Confidence Low |
| Rammus | JUNGLE | S+ | 56.80 | 4.10 | 6.81 | 0 | Confidence Med |
| Senna | DUO | S | 50.98 | 1.54 | 26.20 | ↓ 6 | Confidence Low |
| Senna | SUPPORT | A | 50.25 | 9.33 | 26.20 | ↓ 17 | Confidence High |
| Seraphine | SUPPORT | A | 49.99 | 6.31 | 1.02 | ↑ 9 | Confidence Med |
| Shyvana | JUNGLE | B | 46.27 | 3.42 | 1.07 | 0 | Confidence Med |
| Sivir | DUO | A | 48.89 | 3.27 | 0.05 | ↑ 1 | Confidence Med |
| Syndra | MID | S+ | 51.77 | 5.95 | 19.32 | ↑ 4 | Confidence Med |
| Volibear | SOLO | A | 48.82 | 8.56 | 7.67 | ↑ 5 | Confidence High |
| Volibear | JUNGLE | A | 49.06 | 4.26 | 7.67 | ↑ 4 | Confidence Med |
| Xayah | DUO | A | 50.42 | 4.70 | 0.17 | ↑ 1 | Confidence Med |
| Yunara | DUO | A | 50.13 | 8.92 | 20.77 | ↓ 6 | Confidence High |
| Yuumi | SUPPORT | A | 48.23 | 8.92 | 33.84 | ↓ 3 | Confidence High |

Roles wr-meta: SOLO = top (Baron Lane) · JUNGLE · MID · DUO = ADC (Dragon Lane) · SUPPORT.
Máquina: `champion_winrates.csv` (mismas filas) · BD: tabla `winrates` (`build_db.py`).
Dato de CONTEXTO meta (secundario): no cambia builds por sí solo — si un movimiento
coincide con un hotfix, el flujo es el de FRAMEWORK §E (triage/annotate).
