# Win rates del roster — wr-meta (Meta Overview)

> Bucket: **Diamond +** · Datos wr-meta: **Updated 10 OCT 2026 UTC 00:00** · Refrescado por el vigía: 10/10/2026
> Fuente: `wr-meta.com/{id}-{champ}.html` (bloque Meta Overview) vía
> `model/check_patch.py` paso 4 — el MISMO proceso que busca parches nuevos (cron 2×/día
> en `patch-watch.yml`, o manual: `python3 wrlab.py winrates`).
> **Los callouts "Estado Meta Actual" de los reportes se toman de aquí** (TEMPLATE §A.1);
> alerta del vigía si un campeón se mueve ≥ 2 pts de win rate.

| Campeón | Rol | Tier | Win % | Pick % | Ban % | Tendencia | Confianza |
|---|---|---|---|---|---|---|---|
| Ahri | MID | A | 50.76 | 4.17 | 0.12 | 0 | Confidence Med |
| Caitlyn | DUO | A | 49.79 | 20.30 | 10.11 | ↑ 1 | Confidence High |
| Cho'Gath | SOLO | S | 50.44 | 11.21 | 35.58 | ↓ 2 | Confidence High |
| Cho'Gath | JUNGLE | S | 51.12 | 8.56 | 35.58 | ↓ 1 | Confidence High |
| Diana | MID | B | 48.38 | 1.05 | 0.16 | ↑ 4 | Confidence Low |
| Diana | JUNGLE | A | 49.87 | 1.46 | 0.16 | 0 | Confidence Low |
| Heimerdinger | MID | A | 50.25 | 1.87 | 1.27 | ↑ 2 | Confidence Low |
| Jinx | DUO | A | 50.30 | 12.49 | 0.44 | ↓ 1 | Confidence High |
| Kalista | DUO | S | 51.29 | 5.85 | 6.57 | 0 | Confidence Med |
| Kalista | SOLO | S+ | 52.98 | 2.43 | 6.57 | 0 | Confidence Low |
| Karma | SUPPORT | A | 49.75 | 4.46 | 0.36 | ↓ 2 | Confidence Med |
| Malphite | SUPPORT | S+ | 51.68 | 7.91 | 43.00 | ↑ 5 | Confidence Med |
| Malphite | SOLO | S+ | 55.88 | 7.13 | 43.00 | 0 | Confidence Med |
| Mordekaiser | SOLO | S+ | 51.64 | 10.64 | 29.87 | ↓ 1 | Confidence High |
| Nocturne | JUNGLE | S+ | 55.33 | 9.83 | 47.61 | 0 | Confidence High |
| Norra | MID | A | 50.20 | 1.43 | 7.57 | ↓ 8 | Confidence Low |
| Orianna | MID | S | 51.90 | 4.36 | 0.27 | ↑ 1 | Confidence Med |
| Ornn | SOLO | A | 51.04 | 1.96 | 0.18 | ↓ 8 | Confidence Low |
| Ornn | SUPPORT | A | 50.40 | 1.13 | 0.18 | ↑ 12 | Confidence Low |
| Rammus | JUNGLE | S+ | 57.34 | 4.55 | 6.42 | 0 | Confidence Med |
| Seraphine | SUPPORT | A | 48.89 | 6.52 | 1.03 | ↓ 6 | Confidence Med |
| Shyvana | JUNGLE | B | 46.14 | 3.60 | 1.25 | 0 | Confidence Med |
| Sivir | DUO | A | 48.96 | 3.41 | 0.05 | 0 | Confidence Med |
| Syndra | MID | S+ | 51.56 | 6.32 | 20.80 | ↑ 4 | Confidence Med |
| Volibear | SOLO | B | 47.97 | 4.87 | 4.52 | 0 | Confidence Med |
| Volibear | JUNGLE | B | 47.70 | 2.35 | 4.52 | ↓ 3 | Confidence Low |
| Xayah | DUO | A | 49.38 | 4.32 | 0.18 | ↓ 4 | Confidence Med |
| Yunara | DUO | S+ | 51.61 | 15.71 | 22.71 | 0 | Confidence High |
| Yuumi | SUPPORT | S | 49.43 | 9.30 | 33.35 | ↑ 7 | Confidence High |

Roles wr-meta: SOLO = top (Baron Lane) · JUNGLE · MID · DUO = ADC (Dragon Lane) · SUPPORT.
Máquina: `champion_winrates.csv` (mismas filas) · BD: tabla `winrates` (`build_db.py`).
Dato de CONTEXTO meta (secundario): no cambia builds por sí solo — si un movimiento
coincide con un hotfix, el flujo es el de FRAMEWORK §E (triage/annotate).
