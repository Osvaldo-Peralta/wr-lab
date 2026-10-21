# Win rates del roster — wr-meta (Meta Overview)

> Bucket: **Diamond +** · Datos wr-meta: **Updated 21 OCT 2026 UTC 00:00** · Refrescado por el vigía: 21/10/2026
> Fuente: `wr-meta.com/{id}-{champ}.html` (bloque Meta Overview) vía
> `model/check_patch.py` paso 4 — el MISMO proceso que busca parches nuevos (cron 2×/día
> en `patch-watch.yml`, o manual: `python3 wrlab.py winrates`).
> **Los callouts "Estado Meta Actual" de los reportes se toman de aquí** (TEMPLATE §A.1);
> alerta del vigía si un campeón se mueve ≥ 2 pts de win rate.

| Campeón | Rol | Tier | Win % | Pick % | Ban % | Tendencia | Confianza |
|---|---|---|---|---|---|---|---|
| Ahri | MID | A | 50.88 | 4.39 | 0.15 | 0 | Confidence Med |
| Caitlyn | DUO | A | 49.66 | 16.04 | 5.31 | ↓ 2 | Confidence High |
| Cho'Gath | SOLO | S | 50.71 | 9.48 | 36.48 | ↓ 1 | Confidence High |
| Cho'Gath | JUNGLE | A | 50.11 | 8.50 | 36.48 | ↓ 2 | Confidence High |
| Diana | MID | B | 47.13 | 1.08 | 0.15 | ↓ 2 | Confidence Low |
| Diana | JUNGLE | A | 50.21 | 1.35 | 0.15 | ↓ 3 | Confidence Low |
| Heimerdinger | MID | A | 49.98 | 1.78 | 1.46 | ↑ 2 | Confidence Low |
| Jinx | DUO | A | 50.75 | 12.75 | 0.52 | ↓ 1 | Confidence High |
| Kalista | DUO | A | 50.40 | 7.74 | 9.39 | ↓ 2 | Confidence Med |
| Kalista | SOLO | S+ | 53.43 | 2.64 | 9.39 | ↑ 1 | Confidence Low |
| Karma | SUPPORT | A | 49.72 | 4.84 | 0.39 | ↑ 1 | Confidence Med |
| Malphite | SUPPORT | S+ | 51.88 | 9.26 | 42.11 | 0 | Confidence High |
| Malphite | SOLO | S+ | 54.36 | 7.44 | 42.11 | 0 | Confidence Med |
| Mordekaiser | SOLO | S+ | 51.84 | 11.18 | 31.80 | ↑ 4 | Confidence High |
| Nocturne | JUNGLE | S+ | 52.41 | 6.99 | 59.17 | ↓ 1 | Confidence Med |
| Norra | MID | A | 50.63 | 1.43 | 6.92 | ↑ 7 | Confidence Low |
| Orianna | MID | A | 51.66 | 4.46 | 0.31 | ↓ 4 | Confidence Med |
| Ornn | SOLO | A | 50.11 | 1.88 | 0.19 | ↓ 12 | Confidence Low |
| Ornn | SUPPORT | A | 50.01 | 1.31 | 0.19 | ↑ 9 | Confidence Low |
| Rammus | JUNGLE | S+ | 55.85 | 4.23 | 6.96 | ↓ 1 | Confidence Med |
| Senna | SUPPORT | A | 49.89 | 7.25 | 16.96 | ↓ 1 | Confidence Med |
| Seraphine | SUPPORT | A | 49.63 | 6.28 | 1.13 | ↓ 3 | Confidence Med |
| Shyvana | JUNGLE | B | 46.31 | 3.10 | 1.03 | 0 | Confidence Med |
| Sivir | DUO | A | 49.38 | 3.85 | 0.06 | 0 | Confidence Med |
| Syndra | MID | S+ | 51.93 | 5.88 | 18.58 | ↑ 1 | Confidence Med |
| Volibear | SOLO | A | 48.29 | 9.43 | 8.19 | ↓ 4 | Confidence High |
| Volibear | JUNGLE | A | 48.80 | 4.93 | 8.19 | ↓ 3 | Confidence Med |
| Xayah | DUO | S | 51.30 | 4.90 | 0.20 | ↑ 4 | Confidence Med |
| Yunara | DUO | A | 49.40 | 6.60 | 14.70 | ↑ 2 | Confidence Med |
| Yuumi | SUPPORT | A | 47.91 | 8.70 | 33.86 | ↓ 1 | Confidence High |

Roles wr-meta: SOLO = top (Baron Lane) · JUNGLE · MID · DUO = ADC (Dragon Lane) · SUPPORT.
Máquina: `champion_winrates.csv` (mismas filas) · BD: tabla `winrates` (`build_db.py`).
Dato de CONTEXTO meta (secundario): no cambia builds por sí solo — si un movimiento
coincide con un hotfix, el flujo es el de FRAMEWORK §E (triage/annotate).
