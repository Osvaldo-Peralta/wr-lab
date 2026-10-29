# Win rates del roster — wr-meta (Meta Overview)

> Bucket: **Diamond +** · Datos wr-meta: **Updated 29 OCT 2026 UTC 00:00** · Refrescado por el vigía: 29/10/2026
> Fuente: `wr-meta.com/{id}-{champ}.html` (bloque Meta Overview) vía
> `model/check_patch.py` paso 4 — el MISMO proceso que busca parches nuevos (cron 2×/día
> en `patch-watch.yml`, o manual: `python3 wrlab.py winrates`).
> **Los callouts "Estado Meta Actual" de los reportes se toman de aquí** (TEMPLATE §A.1);
> alerta del vigía si un campeón se mueve ≥ 2 pts de win rate.

| Campeón | Rol | Tier | Win % | Pick % | Ban % | Tendencia | Confianza |
|---|---|---|---|---|---|---|---|
| Ahri | MID | A | 50.66 | 4.71 | 0.17 | ↑ 1 | Confidence Med |
| Caitlyn | DUO | A | 49.81 | 15.47 | 4.31 | ↑ 1 | Confidence High |
| Cho'Gath | SOLO | A | 50.33 | 9.15 | 35.67 | ↓ 4 | Confidence High |
| Cho'Gath | JUNGLE | S | 50.56 | 8.18 | 35.67 | ↑ 2 | Confidence High |
| Diana | MID | B | 48.25 | 1.01 | 0.13 | ↑ 5 | Confidence Low |
| Diana | JUNGLE | B | 49.21 | 1.29 | 0.13 | ↓ 12 | Confidence Low |
| Heimerdinger | MID | A | 50.37 | 1.70 | 1.57 | ↑ 4 | Confidence Low |
| Jinx | DUO | A | 50.53 | 12.68 | 0.53 | 0 | Confidence High |
| Kalista | DUO | A | 50.56 | 7.84 | 11.77 | 0 | Confidence Med |
| Kalista | SOLO | S+ | 53.27 | 2.95 | 11.77 | 0 | Confidence Low |
| Karma | SUPPORT | A | 49.93 | 4.55 | 0.46 | ↓ 2 | Confidence Med |
| Malphite | SUPPORT | S+ | 51.67 | 9.54 | 43.15 | ↓ 1 | Confidence High |
| Malphite | SOLO | S+ | 54.20 | 7.45 | 43.15 | ↓ 1 | Confidence Med |
| Malphite | MID | S+ | 50.86 | 1.02 | 43.15 | ↑ 4 | Confidence Low |
| Mordekaiser | SOLO | S+ | 51.51 | 10.84 | 33.78 | ↑ 5 | Confidence High |
| Nocturne | JUNGLE | S+ | 52.81 | 7.05 | 59.60 | ↑ 2 | Confidence Med |
| Norra | MID | S | 51.04 | 1.30 | 6.77 | ↑ 12 | Confidence Low |
| Orianna | MID | S | 52.24 | 4.86 | 0.36 | ↑ 3 | Confidence Med |
| Ornn | SOLO | A | 50.90 | 1.93 | 0.22 | ↓ 2 | Confidence Low |
| Ornn | SUPPORT | B | 49.28 | 1.29 | 0.22 | ↓ 8 | Confidence Low |
| Rammus | JUNGLE | S+ | 56.41 | 3.86 | 6.79 | 0 | Confidence Med |
| Senna | SUPPORT | A | 50.05 | 6.05 | 9.82 | ↑ 2 | Confidence Med |
| Seraphine | SUPPORT | A | 49.77 | 6.61 | 1.16 | ↓ 5 | Confidence Med |
| Shyvana | JUNGLE | B | 46.36 | 3.14 | 0.97 | 0 | Confidence Med |
| Sivir | DUO | A | 49.72 | 4.70 | 0.10 | ↑ 1 | Confidence Med |
| Syndra | MID | S+ | 51.72 | 5.87 | 17.82 | 0 | Confidence Med |
| Volibear | SOLO | A | 49.00 | 7.15 | 7.54 | ↓ 1 | Confidence Med |
| Volibear | JUNGLE | A | 48.93 | 3.93 | 7.54 | ↓ 4 | Confidence Med |
| Xayah | DUO | A | 50.86 | 4.82 | 0.25 | ↓ 2 | Confidence Med |
| Yunara | DUO | A | 49.48 | 7.68 | 10.09 | ↑ 1 | Confidence Med |
| Yuumi | SUPPORT | A | 48.12 | 8.09 | 33.87 | ↑ 1 | Confidence High |

Roles wr-meta: SOLO = top (Baron Lane) · JUNGLE · MID · DUO = ADC (Dragon Lane) · SUPPORT.
Máquina: `champion_winrates.csv` (mismas filas) · BD: tabla `winrates` (`build_db.py`).
Dato de CONTEXTO meta (secundario): no cambia builds por sí solo — si un movimiento
coincide con un hotfix, el flujo es el de FRAMEWORK §E (triage/annotate).
