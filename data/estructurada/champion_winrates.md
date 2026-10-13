# Win rates del roster — wr-meta (Meta Overview)

> Bucket: **Diamond +** · Datos wr-meta: **Updated 13 OCT 2026 UTC 00:00** · Refrescado por el vigía: 13/10/2026
> Fuente: `wr-meta.com/{id}-{champ}.html` (bloque Meta Overview) vía
> `model/check_patch.py` paso 4 — el MISMO proceso que busca parches nuevos (cron 2×/día
> en `patch-watch.yml`, o manual: `python3 wrlab.py winrates`).
> **Los callouts "Estado Meta Actual" de los reportes se toman de aquí** (TEMPLATE §A.1);
> alerta del vigía si un campeón se mueve ≥ 2 pts de win rate.

| Campeón | Rol | Tier | Win % | Pick % | Ban % | Tendencia | Confianza |
|---|---|---|---|---|---|---|---|
| Ahri | MID | A | 50.75 | 4.34 | 0.13 | ↓ 2 | Confidence Med |
| Caitlyn | DUO | A | 49.79 | 19.03 | 8.48 | ↑ 1 | Confidence High |
| Cho'Gath | SOLO | A | 50.05 | 10.84 | 35.00 | ↓ 4 | Confidence High |
| Cho'Gath | JUNGLE | S | 50.71 | 8.61 | 35.00 | ↓ 1 | Confidence High |
| Diana | MID | B | 47.43 | 1.10 | 0.15 | 0 | Confidence Low |
| Diana | JUNGLE | A | 50.86 | 1.48 | 0.15 | ↑ 6 | Confidence Low |
| Heimerdinger | MID | B | 48.80 | 1.63 | 1.31 | ↓ 11 | Confidence Low |
| Jinx | DUO | A | 50.53 | 12.32 | 0.45 | 0 | Confidence High |
| Kalista | DUO | A | 50.39 | 6.01 | 7.22 | ↓ 3 | Confidence Med |
| Kalista | SOLO | S+ | 53.41 | 2.40 | 7.22 | 0 | Confidence Low |
| Karma | SUPPORT | A | 49.63 | 4.45 | 0.35 | ↓ 3 | Confidence Med |
| Malphite | SUPPORT | S+ | 51.47 | 7.92 | 41.21 | 0 | Confidence Med |
| Malphite | SOLO | S+ | 55.32 | 6.98 | 41.21 | 0 | Confidence Med |
| Mordekaiser | SOLO | S | 51.12 | 10.96 | 29.22 | ↓ 5 | Confidence High |
| Nocturne | JUNGLE | S+ | 55.68 | 10.64 | 53.12 | 0 | Confidence High |
| Norra | MID | A | 50.98 | 1.43 | 7.25 | ↓ 2 | Confidence Low |
| Orianna | MID | A | 51.09 | 4.51 | 0.30 | ↓ 6 | Confidence Med |
| Ornn | SOLO | A | 51.75 | 1.99 | 0.17 | ↓ 3 | Confidence Low |
| Ornn | SUPPORT | B | 49.38 | 1.16 | 0.17 | ↓ 1 | Confidence Low |
| Rammus | JUNGLE | S+ | 57.46 | 4.35 | 6.56 | 0 | Confidence Med |
| Senna | DUO | S+ | 55.70 | 3.25 | 33.31 | 0 | Confidence Med |
| Senna | SUPPORT | S+ | 54.04 | 12.87 | 33.31 | 0 | Confidence High |
| Seraphine | SUPPORT | A | 49.27 | 6.61 | 1.05 | 0 | Confidence Med |
| Shyvana | JUNGLE | B | 45.15 | 3.41 | 1.20 | ↓ 1 | Confidence Med |
| Sivir | DUO | B | 48.28 | 3.45 | 0.05 | ↓ 3 | Confidence Med |
| Syndra | MID | S+ | 51.45 | 6.23 | 19.43 | ↑ 1 | Confidence Med |
| Volibear | SOLO | A | 47.93 | 4.92 | 4.47 | ↑ 1 | Confidence Med |
| Volibear | JUNGLE | A | 48.06 | 2.47 | 4.47 | ↑ 3 | Confidence Low |
| Xayah | DUO | A | 49.66 | 4.50 | 0.18 | ↓ 2 | Confidence Med |
| Yunara | DUO | S+ | 51.48 | 15.77 | 23.78 | 0 | Confidence High |
| Yuumi | SUPPORT | A | 48.64 | 8.97 | 33.55 | ↓ 3 | Confidence High |

Roles wr-meta: SOLO = top (Baron Lane) · JUNGLE · MID · DUO = ADC (Dragon Lane) · SUPPORT.
Máquina: `champion_winrates.csv` (mismas filas) · BD: tabla `winrates` (`build_db.py`).
Dato de CONTEXTO meta (secundario): no cambia builds por sí solo — si un movimiento
coincide con un hotfix, el flujo es el de FRAMEWORK §E (triage/annotate).
