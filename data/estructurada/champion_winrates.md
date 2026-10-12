# Win rates del roster — wr-meta (Meta Overview)

> Bucket: **Diamond +** · Datos wr-meta: **Updated 12 OCT 2026 UTC 00:00** · Refrescado por el vigía: 12/10/2026
> Fuente: `wr-meta.com/{id}-{champ}.html` (bloque Meta Overview) vía
> `model/check_patch.py` paso 4 — el MISMO proceso que busca parches nuevos (cron 2×/día
> en `patch-watch.yml`, o manual: `python3 wrlab.py winrates`).
> **Los callouts "Estado Meta Actual" de los reportes se toman de aquí** (TEMPLATE §A.1);
> alerta del vigía si un campeón se mueve ≥ 2 pts de win rate.

| Campeón | Rol | Tier | Win % | Pick % | Ban % | Tendencia | Confianza |
|---|---|---|---|---|---|---|---|
| Ahri | MID | A | 50.61 | 4.23 | 0.12 | ↑ 4 | Confidence Med |
| Caitlyn | DUO | A | 49.69 | 19.58 | 8.84 | 0 | Confidence High |
| Cho'Gath | SOLO | S | 50.45 | 11.05 | 35.24 | ↑ 4 | Confidence High |
| Cho'Gath | JUNGLE | S | 50.54 | 8.51 | 35.24 | 0 | Confidence High |
| Diana | MID | B | 48.13 | 1.08 | 0.17 | 0 | Confidence Low |
| Diana | JUNGLE | A | 49.99 | 1.44 | 0.17 | ↓ 5 | Confidence Low |
| Heimerdinger | MID | A | 49.97 | 1.67 | 1.32 | ↑ 1 | Confidence Low |
| Jinx | DUO | A | 50.44 | 12.44 | 0.45 | ↑ 1 | Confidence High |
| Kalista | DUO | A | 50.86 | 6.10 | 7.03 | 0 | Confidence Med |
| Kalista | SOLO | S+ | 53.72 | 2.47 | 7.03 | 0 | Confidence Low |
| Karma | SUPPORT | A | 50.12 | 4.36 | 0.35 | 0 | Confidence Med |
| Malphite | SUPPORT | S+ | 51.57 | 7.98 | 41.74 | ↓ 1 | Confidence Med |
| Malphite | SOLO | S+ | 55.60 | 7.09 | 41.74 | 0 | Confidence Med |
| Mordekaiser | SOLO | S+ | 51.55 | 10.37 | 29.84 | ↓ 1 | Confidence High |
| Nocturne | JUNGLE | S+ | 55.53 | 10.78 | 51.05 | ↑ 1 | Confidence High |
| Norra | MID | S | 50.66 | 1.38 | 7.43 | ↑ 3 | Confidence Low |
| Orianna | MID | S | 51.63 | 4.41 | 0.29 | ↑ 5 | Confidence Med |
| Ornn | SOLO | S | 52.72 | 2.02 | 0.16 | ↑ 2 | Confidence Low |
| Ornn | SUPPORT | A | 49.29 | 1.16 | 0.16 | ↑ 1 | Confidence Low |
| Rammus | JUNGLE | S+ | 57.32 | 4.39 | 6.53 | ↑ 1 | Confidence Med |
| Senna | DUO | S+ | 55.69 | 3.24 | 33.74 | 0 | Confidence Med |
| Senna | SUPPORT | S+ | 53.97 | 12.80 | 33.74 | ↑ 1 | Confidence High |
| Seraphine | SUPPORT | A | 49.12 | 6.44 | 1.04 | ↑ 1 | Confidence Med |
| Shyvana | JUNGLE | B | 45.91 | 3.45 | 1.25 | ↑ 1 | Confidence Med |
| Sivir | DUO | B | 48.79 | 3.42 | 0.06 | ↓ 1 | Confidence Med |
| Syndra | MID | S | 51.28 | 6.18 | 19.67 | 0 | Confidence Med |
| Volibear | SOLO | B | 48.13 | 4.83 | 4.45 | ↓ 1 | Confidence Med |
| Volibear | JUNGLE | B | 47.73 | 2.39 | 4.45 | ↓ 5 | Confidence Low |
| Xayah | DUO | A | 50.11 | 4.45 | 0.17 | ↓ 1 | Confidence Med |
| Yunara | DUO | S+ | 51.41 | 15.88 | 23.14 | 0 | Confidence High |
| Yuumi | SUPPORT | A | 48.89 | 9.15 | 33.08 | ↓ 7 | Confidence High |

Roles wr-meta: SOLO = top (Baron Lane) · JUNGLE · MID · DUO = ADC (Dragon Lane) · SUPPORT.
Máquina: `champion_winrates.csv` (mismas filas) · BD: tabla `winrates` (`build_db.py`).
Dato de CONTEXTO meta (secundario): no cambia builds por sí solo — si un movimiento
coincide con un hotfix, el flujo es el de FRAMEWORK §E (triage/annotate).
