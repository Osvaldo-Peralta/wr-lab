# Win rates del roster — wr-meta (Meta Overview)

> Bucket: **Diamond +** · Datos wr-meta: **Updated 28 OCT 2026 UTC 00:00** · Refrescado por el vigía: 28/10/2026
> Fuente: `wr-meta.com/{id}-{champ}.html` (bloque Meta Overview) vía
> `model/check_patch.py` paso 4 — el MISMO proceso que busca parches nuevos (cron 2×/día
> en `patch-watch.yml`, o manual: `python3 wrlab.py winrates`).
> **Los callouts "Estado Meta Actual" de los reportes se toman de aquí** (TEMPLATE §A.1);
> alerta del vigía si un campeón se mueve ≥ 2 pts de win rate.

| Campeón | Rol | Tier | Win % | Pick % | Ban % | Tendencia | Confianza |
|---|---|---|---|---|---|---|---|
| Ahri | MID | A | 50.36 | 4.78 | 0.16 | ↓ 5 | Confidence Med |
| Caitlyn | DUO | A | 49.90 | 15.84 | 4.39 | ↑ 2 | Confidence High |
| Cho'Gath | SOLO | S | 50.50 | 9.16 | 36.12 | ↓ 1 | Confidence High |
| Cho'Gath | JUNGLE | S | 50.18 | 8.27 | 36.12 | ↑ 1 | Confidence High |
| Diana | MID | B | 46.63 | 1.04 | 0.14 | ↓ 1 | Confidence Low |
| Diana | JUNGLE | A | 50.89 | 1.28 | 0.14 | ↑ 7 | Confidence Low |
| Heimerdinger | MID | A | 50.12 | 1.70 | 1.55 | ↓ 2 | Confidence Low |
| Jinx | DUO | S | 50.49 | 12.82 | 0.54 | ↑ 3 | Confidence High |
| Kalista | DUO | S | 50.88 | 7.87 | 11.40 | 0 | Confidence Med |
| Kalista | SOLO | S+ | 53.40 | 2.90 | 11.40 | ↑ 1 | Confidence Low |
| Karma | SUPPORT | A | 50.04 | 4.56 | 0.44 | ↓ 2 | Confidence Med |
| Malphite | SUPPORT | S+ | 51.60 | 9.59 | 43.02 | ↑ 2 | Confidence High |
| Malphite | SOLO | S+ | 54.80 | 7.47 | 43.02 | ↑ 1 | Confidence Med |
| Malphite | MID | S | 50.29 | 1.01 | 43.02 | 0 | Confidence Low |
| Mordekaiser | SOLO | S | 51.25 | 10.99 | 33.60 | ↓ 3 | Confidence High |
| Nocturne | JUNGLE | S+ | 52.85 | 6.90 | 59.52 | 0 | Confidence Med |
| Norra | MID | A | 50.14 | 1.31 | 6.79 | ↓ 12 | Confidence Low |
| Orianna | MID | S | 51.86 | 4.76 | 0.35 | ↑ 1 | Confidence Med |
| Ornn | SOLO | A | 51.39 | 1.95 | 0.20 | ↑ 3 | Confidence Low |
| Ornn | SUPPORT | A | 50.06 | 1.31 | 0.20 | ↑ 9 | Confidence Low |
| Rammus | JUNGLE | S+ | 56.35 | 3.80 | 6.78 | ↑ 1 | Confidence Med |
| Senna | SUPPORT | A | 49.94 | 6.17 | 10.50 | ↓ 1 | Confidence Med |
| Seraphine | SUPPORT | A | 50.13 | 6.67 | 1.17 | ↑ 2 | Confidence Med |
| Shyvana | JUNGLE | B | 46.28 | 3.15 | 0.94 | ↑ 1 | Confidence Med |
| Sivir | DUO | A | 49.72 | 4.73 | 0.09 | ↑ 2 | Confidence Med |
| Syndra | MID | S | 51.46 | 5.77 | 17.77 | ↓ 4 | Confidence Med |
| Volibear | SOLO | A | 49.17 | 7.19 | 7.69 | 0 | Confidence Med |
| Volibear | JUNGLE | A | 49.52 | 4.01 | 7.69 | ↑ 4 | Confidence Med |
| Xayah | DUO | A | 51.27 | 4.66 | 0.25 | ↑ 1 | Confidence Med |
| Yunara | DUO | A | 49.45 | 7.44 | 10.34 | ↓ 7 | Confidence Med |
| Yuumi | SUPPORT | A | 47.81 | 8.13 | 33.67 | 0 | Confidence High |

Roles wr-meta: SOLO = top (Baron Lane) · JUNGLE · MID · DUO = ADC (Dragon Lane) · SUPPORT.
Máquina: `champion_winrates.csv` (mismas filas) · BD: tabla `winrates` (`build_db.py`).
Dato de CONTEXTO meta (secundario): no cambia builds por sí solo — si un movimiento
coincide con un hotfix, el flujo es el de FRAMEWORK §E (triage/annotate).
