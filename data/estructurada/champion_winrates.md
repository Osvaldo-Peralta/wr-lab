# Win rates del roster — wr-meta (Meta Overview)

> Bucket: **Diamond +** · Datos wr-meta: **Updated 11 OCT 2026 UTC 00:00** · Refrescado por el vigía: 11/10/2026
> Fuente: `wr-meta.com/{id}-{champ}.html` (bloque Meta Overview) vía
> `model/check_patch.py` paso 4 — el MISMO proceso que busca parches nuevos (cron 2×/día
> en `patch-watch.yml`, o manual: `python3 wrlab.py winrates`).
> **Los callouts "Estado Meta Actual" de los reportes se toman de aquí** (TEMPLATE §A.1);
> alerta del vigía si un campeón se mueve ≥ 2 pts de win rate.

| Campeón | Rol | Tier | Win % | Pick % | Ban % | Tendencia | Confianza |
|---|---|---|---|---|---|---|---|
| Ahri | MID | A | 50.45 | 4.16 | 0.12 | ↓ 4 | Confidence Med |
| Caitlyn | DUO | A | 49.56 | 20.13 | 9.28 | ↓ 2 | Confidence High |
| Cho'Gath | SOLO | S | 50.24 | 11.20 | 35.48 | 0 | Confidence High |
| Cho'Gath | JUNGLE | S | 50.80 | 8.57 | 35.48 | ↓ 2 | Confidence High |
| Diana | MID | B | 47.57 | 1.07 | 0.16 | ↓ 3 | Confidence Low |
| Diana | JUNGLE | A | 50.92 | 1.42 | 0.16 | ↑ 8 | Confidence Low |
| Heimerdinger | MID | A | 50.12 | 1.67 | 1.27 | ↓ 3 | Confidence Low |
| Jinx | DUO | A | 50.20 | 12.44 | 0.46 | 0 | Confidence High |
| Kalista | DUO | S | 51.34 | 5.93 | 6.70 | ↑ 1 | Confidence Med |
| Kalista | SOLO | S+ | 53.90 | 2.42 | 6.70 | 0 | Confidence Low |
| Karma | SUPPORT | A | 49.61 | 4.42 | 0.37 | ↑ 3 | Confidence Med |
| Malphite | SUPPORT | S+ | 51.76 | 7.93 | 42.29 | ↓ 1 | Confidence Med |
| Malphite | SOLO | S+ | 55.70 | 7.06 | 42.29 | 0 | Confidence Med |
| Mordekaiser | SOLO | S+ | 51.62 | 10.18 | 29.90 | ↑ 1 | Confidence High |
| Nocturne | JUNGLE | S+ | 55.34 | 10.49 | 49.29 | 0 | Confidence High |
| Norra | MID | S | 50.69 | 1.41 | 7.44 | ↑ 4 | Confidence Low |
| Orianna | MID | A | 51.22 | 4.41 | 0.29 | ↓ 6 | Confidence Med |
| Ornn | SOLO | S | 51.64 | 1.96 | 0.17 | ↑ 8 | Confidence Low |
| Ornn | SUPPORT | B | 49.26 | 1.14 | 0.17 | ↓ 8 | Confidence Low |
| Rammus | JUNGLE | S+ | 57.10 | 4.50 | 6.49 | ↓ 1 | Confidence Med |
| Senna | DUO | S+ | 55.58 | 3.34 | 34.63 | 0 | Confidence Med |
| Senna | SUPPORT | S+ | 53.63 | 12.92 | 34.63 | ↓ 1 | Confidence High |
| Seraphine | SUPPORT | A | 49.04 | 6.47 | 1.03 | 0 | Confidence Med |
| Shyvana | JUNGLE | B | 46.00 | 3.52 | 1.23 | ↓ 1 | Confidence Med |
| Sivir | DUO | A | 49.23 | 3.40 | 0.05 | 0 | Confidence Med |
| Syndra | MID | S | 51.28 | 6.37 | 20.25 | 0 | Confidence Med |
| Volibear | SOLO | B | 47.86 | 4.82 | 4.49 | ↓ 2 | Confidence Med |
| Volibear | JUNGLE | A | 48.25 | 2.38 | 4.49 | ↑ 3 | Confidence Low |
| Xayah | DUO | A | 50.10 | 4.32 | 0.18 | ↑ 3 | Confidence Med |
| Yunara | DUO | S+ | 51.44 | 15.83 | 22.94 | 0 | Confidence High |
| Yuumi | SUPPORT | S | 49.54 | 9.30 | 33.24 | ↑ 3 | Confidence High |

Roles wr-meta: SOLO = top (Baron Lane) · JUNGLE · MID · DUO = ADC (Dragon Lane) · SUPPORT.
Máquina: `champion_winrates.csv` (mismas filas) · BD: tabla `winrates` (`build_db.py`).
Dato de CONTEXTO meta (secundario): no cambia builds por sí solo — si un movimiento
coincide con un hotfix, el flujo es el de FRAMEWORK §E (triage/annotate).
