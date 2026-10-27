# Win rates del roster — wr-meta (Meta Overview)

> Bucket: **Diamond +** · Datos wr-meta: **Updated 27 OCT 2026 UTC 00:00** · Refrescado por el vigía: 27/10/2026
> Fuente: `wr-meta.com/{id}-{champ}.html` (bloque Meta Overview) vía
> `model/check_patch.py` paso 4 — el MISMO proceso que busca parches nuevos (cron 2×/día
> en `patch-watch.yml`, o manual: `python3 wrlab.py winrates`).
> **Los callouts "Estado Meta Actual" de los reportes se toman de aquí** (TEMPLATE §A.1);
> alerta del vigía si un campeón se mueve ≥ 2 pts de win rate.

| Campeón | Rol | Tier | Win % | Pick % | Ban % | Tendencia | Confianza |
|---|---|---|---|---|---|---|---|
| Ahri | MID | A | 50.84 | 4.74 | 0.15 | ↓ 1 | Confidence Med |
| Caitlyn | DUO | A | 49.68 | 15.95 | 4.70 | ↓ 2 | Confidence High |
| Cho'Gath | SOLO | S | 50.44 | 9.24 | 35.79 | ↑ 7 | Confidence High |
| Cho'Gath | JUNGLE | S | 50.04 | 8.30 | 35.79 | ↑ 2 | Confidence High |
| Diana | MID | B | 46.82 | 1.07 | 0.15 | ↓ 2 | Confidence Low |
| Diana | JUNGLE | A | 49.97 | 1.34 | 0.15 | ↓ 4 | Confidence Low |
| Heimerdinger | MID | A | 49.83 | 1.78 | 1.53 | ↓ 3 | Confidence Low |
| Jinx | DUO | A | 50.25 | 12.71 | 0.56 | ↓ 3 | Confidence High |
| Kalista | DUO | A | 50.76 | 8.01 | 11.17 | ↓ 1 | Confidence High |
| Kalista | SOLO | S+ | 53.18 | 2.81 | 11.17 | ↓ 1 | Confidence Low |
| Karma | SUPPORT | A | 50.06 | 4.82 | 0.45 | ↑ 2 | Confidence Med |
| Malphite | SUPPORT | S+ | 51.62 | 9.45 | 42.44 | ↑ 1 | Confidence High |
| Malphite | SOLO | S+ | 54.73 | 7.49 | 42.44 | 0 | Confidence Med |
| Mordekaiser | SOLO | S+ | 51.29 | 11.21 | 32.97 | ↑ 3 | Confidence High |
| Nocturne | JUNGLE | S+ | 52.26 | 6.89 | 58.55 | ↑ 3 | Confidence Med |
| Norra | MID | A | 51.02 | 1.32 | 6.89 | ↑ 1 | Confidence Low |
| Orianna | MID | S | 51.93 | 4.88 | 0.35 | ↓ 1 | Confidence Med |
| Ornn | SOLO | A | 50.73 | 2.09 | 0.21 | ↓ 4 | Confidence Low |
| Ornn | SUPPORT | B | 48.94 | 1.37 | 0.21 | ↓ 9 | Confidence Low |
| Rammus | JUNGLE | S+ | 56.23 | 3.81 | 6.93 | ↓ 1 | Confidence Med |
| Senna | SUPPORT | A | 49.81 | 6.58 | 11.30 | ↑ 1 | Confidence Med |
| Seraphine | SUPPORT | A | 49.88 | 6.70 | 1.15 | ↑ 2 | Confidence Med |
| Shyvana | JUNGLE | B | 45.87 | 2.99 | 0.98 | ↓ 1 | Confidence Low |
| Sivir | DUO | A | 49.63 | 5.04 | 0.08 | ↓ 1 | Confidence Med |
| Syndra | MID | S+ | 52.07 | 5.89 | 17.83 | ↑ 1 | Confidence Med |
| Volibear | SOLO | A | 49.08 | 7.60 | 7.99 | ↓ 1 | Confidence Med |
| Volibear | JUNGLE | A | 48.94 | 3.94 | 7.99 | ↑ 2 | Confidence Med |
| Xayah | DUO | A | 51.14 | 4.95 | 0.23 | ↑ 2 | Confidence Med |
| Yunara | DUO | S | 50.28 | 5.51 | 10.59 | ↑ 7 | Confidence Med |
| Yuumi | SUPPORT | A | 47.47 | 8.01 | 33.95 | 0 | Confidence High |

Roles wr-meta: SOLO = top (Baron Lane) · JUNGLE · MID · DUO = ADC (Dragon Lane) · SUPPORT.
Máquina: `champion_winrates.csv` (mismas filas) · BD: tabla `winrates` (`build_db.py`).
Dato de CONTEXTO meta (secundario): no cambia builds por sí solo — si un movimiento
coincide con un hotfix, el flujo es el de FRAMEWORK §E (triage/annotate).
