# Win rates del roster — wr-meta (Meta Overview)

> Bucket: **Diamond +** · Datos wr-meta: **Updated 19 OCT 2026 UTC 00:00** · Refrescado por el vigía: 19/10/2026
> Fuente: `wr-meta.com/{id}-{champ}.html` (bloque Meta Overview) vía
> `model/check_patch.py` paso 4 — el MISMO proceso que busca parches nuevos (cron 2×/día
> en `patch-watch.yml`, o manual: `python3 wrlab.py winrates`).
> **Los callouts "Estado Meta Actual" de los reportes se toman de aquí** (TEMPLATE §A.1);
> alerta del vigía si un campeón se mueve ≥ 2 pts de win rate.

| Campeón | Rol | Tier | Win % | Pick % | Ban % | Tendencia | Confianza |
|---|---|---|---|---|---|---|---|
| Ahri | MID | A | 50.52 | 4.58 | 0.14 | ↓ 6 | Confidence Med |
| Caitlyn | DUO | A | 49.67 | 15.83 | 6.19 | ↓ 1 | Confidence High |
| Cho'Gath | SOLO | A | 50.46 | 9.70 | 35.87 | ↓ 4 | Confidence High |
| Cho'Gath | JUNGLE | A | 49.80 | 8.60 | 35.87 | ↓ 2 | Confidence High |
| Diana | MID | B | 48.20 | 1.09 | 0.16 | ↑ 3 | Confidence Low |
| Diana | JUNGLE | A | 50.97 | 1.44 | 0.16 | ↑ 8 | Confidence Low |
| Heimerdinger | MID | A | 50.08 | 1.62 | 1.36 | ↓ 1 | Confidence Low |
| Jinx | DUO | A | 50.80 | 12.46 | 0.51 | ↓ 1 | Confidence High |
| Kalista | DUO | A | 50.75 | 6.74 | 8.59 | ↓ 1 | Confidence Med |
| Kalista | SOLO | S+ | 54.05 | 2.52 | 8.59 | 0 | Confidence Low |
| Karma | SUPPORT | A | 50.37 | 4.64 | 0.39 | ↑ 1 | Confidence Med |
| Malphite | SUPPORT | S+ | 51.65 | 9.26 | 41.50 | ↑ 1 | Confidence High |
| Malphite | SOLO | S+ | 55.12 | 7.28 | 41.50 | ↑ 1 | Confidence Med |
| Mordekaiser | SOLO | S+ | 51.38 | 11.08 | 30.47 | ↑ 4 | Confidence High |
| Nocturne | JUNGLE | S+ | 52.24 | 7.17 | 57.44 | ↓ 2 | Confidence Med |
| Norra | MID | A | 49.79 | 1.49 | 7.00 | ↓ 6 | Confidence Low |
| Orianna | MID | S | 52.09 | 4.52 | 0.32 | 0 | Confidence Med |
| Ornn | SOLO | A | 50.35 | 1.83 | 0.18 | ↓ 9 | Confidence Low |
| Ornn | SUPPORT | A | 50.01 | 1.34 | 0.18 | ↓ 1 | Confidence Low |
| Rammus | JUNGLE | S+ | 55.91 | 3.79 | 6.89 | 0 | Confidence Med |
| Senna | SUPPORT | A | 49.62 | 7.70 | 20.44 | ↑ 3 | Confidence Med |
| Seraphine | SUPPORT | A | 49.52 | 6.53 | 1.08 | ↓ 8 | Confidence Med |
| Shyvana | JUNGLE | B | 46.42 | 3.39 | 1.07 | ↓ 1 | Confidence Med |
| Sivir | DUO | A | 50.14 | 3.86 | 0.07 | ↑ 9 | Confidence Med |
| Syndra | MID | S+ | 51.95 | 5.89 | 18.75 | ↑ 1 | Confidence Med |
| Volibear | SOLO | A | 48.48 | 9.17 | 8.42 | ↓ 2 | Confidence High |
| Volibear | JUNGLE | A | 49.13 | 4.75 | 8.42 | ↑ 4 | Confidence Med |
| Xayah | DUO | A | 50.98 | 4.97 | 0.19 | ↑ 2 | Confidence Med |
| Yunara | DUO | A | 48.85 | 7.11 | 17.34 | ↑ 1 | Confidence Med |
| Yuumi | SUPPORT | A | 47.72 | 8.41 | 34.07 | 0 | Confidence High |

Roles wr-meta: SOLO = top (Baron Lane) · JUNGLE · MID · DUO = ADC (Dragon Lane) · SUPPORT.
Máquina: `champion_winrates.csv` (mismas filas) · BD: tabla `winrates` (`build_db.py`).
Dato de CONTEXTO meta (secundario): no cambia builds por sí solo — si un movimiento
coincide con un hotfix, el flujo es el de FRAMEWORK §E (triage/annotate).
