# Win rates del roster — wr-meta (Meta Overview)

> Bucket: **Diamond +** · Datos wr-meta: **Updated 06 OCT 2026 UTC 00:00** · Refrescado por el vigía: 06/10/2026
> Fuente: `wr-meta.com/{id}-{champ}.html` (bloque Meta Overview) vía
> `model/check_patch.py` paso 4 — el MISMO proceso que busca parches nuevos (cron 2×/día
> en `patch-watch.yml`, o manual: `python3 wrlab.py winrates`).
> **Los callouts "Estado Meta Actual" de los reportes se toman de aquí** (TEMPLATE §A.1);
> alerta del vigía si un campeón se mueve ≥ 2 pts de win rate.

| Campeón | Rol | Tier | Win % | Pick % | Ban % | Tendencia | Confianza |
|---|---|---|---|---|---|---|---|
| Ahri | MID | A | 50.97 | 4.27 | 0.14 | ↑ 2 | Confidence Med |
| Caitlyn | DUO | A | 49.79 | 21.36 | 13.93 | 0 | Confidence High |
| Cho'Gath | SOLO | S | 50.67 | 11.38 | 35.00 | ↓ 1 | Confidence High |
| Cho'Gath | JUNGLE | S | 50.44 | 8.19 | 35.00 | ↑ 1 | Confidence High |
| Diana | MID | B | 47.44 | 1.15 | 0.17 | ↑ 2 | Confidence Low |
| Diana | JUNGLE | A | 50.36 | 1.67 | 0.17 | ↓ 1 | Confidence Low |
| Heimerdinger | MID | A | 50.24 | 1.62 | 1.12 | ↑ 4 | Confidence Low |
| Jinx | DUO | A | 50.68 | 12.07 | 0.44 | 0 | Confidence High |
| Kalista | DUO | S | 51.19 | 5.43 | 5.48 | ↑ 1 | Confidence Med |
| Kalista | SOLO | S+ | 52.67 | 2.10 | 5.48 | ↑ 2 | Confidence Low |
| Karma | SUPPORT | A | 49.57 | 4.94 | 0.37 | ↓ 2 | Confidence Med |
| Malphite | SUPPORT | S | 51.30 | 7.31 | 44.69 | ↓ 2 | Confidence Med |
| Malphite | SOLO | S+ | 55.09 | 7.47 | 44.69 | 0 | Confidence Med |
| Mordekaiser | SOLO | S | 51.23 | 10.50 | 28.28 | ↓ 2 | Confidence High |
| Nocturne | JUNGLE | S+ | 55.32 | 9.47 | 42.12 | 0 | Confidence High |
| Norra | MID | A | 50.81 | 1.50 | 7.53 | ↓ 1 | Confidence Low |
| Orianna | MID | A | 51.39 | 4.51 | 0.27 | ↓ 2 | Confidence Med |
| Rammus | JUNGLE | S+ | 56.84 | 4.88 | 7.21 | 0 | Confidence Med |
| Seraphine | SUPPORT | A | 49.55 | 6.47 | 0.97 | ↑ 2 | Confidence Med |
| Shyvana | JUNGLE | B | 46.14 | 3.64 | 1.32 | ↓ 3 | Confidence Med |
| Sivir | DUO | B | 48.16 | 3.52 | 0.05 | ↓ 1 | Confidence Med |
| Syndra | MID | S+ | 51.08 | 6.63 | 24.64 | ↑ 7 | Confidence Med |
| Volibear | SOLO | A | 48.19 | 5.30 | 4.58 | ↑ 2 | Confidence Med |
| Volibear | JUNGLE | A | 47.85 | 2.41 | 4.58 | ↑ 3 | Confidence Low |
| Yunara | DUO | S+ | 51.54 | 16.71 | 23.93 | 0 | Confidence High |
| Yuumi | SUPPORT | A | 48.89 | 9.59 | 34.46 | ↓ 1 | Confidence High |

Roles wr-meta: SOLO = top (Baron Lane) · JUNGLE · MID · DUO = ADC (Dragon Lane) · SUPPORT.
Máquina: `champion_winrates.csv` (mismas filas) · BD: tabla `winrates` (`build_db.py`).
Dato de CONTEXTO meta (secundario): no cambia builds por sí solo — si un movimiento
coincide con un hotfix, el flujo es el de FRAMEWORK §E (triage/annotate).
