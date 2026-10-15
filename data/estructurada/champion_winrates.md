# Win rates del roster — wr-meta (Meta Overview)

> Bucket: **Diamond +** · Datos wr-meta: **Updated 15 OCT 2026 UTC 00:00** · Refrescado por el vigía: 15/10/2026
> Fuente: `wr-meta.com/{id}-{champ}.html` (bloque Meta Overview) vía
> `model/check_patch.py` paso 4 — el MISMO proceso que busca parches nuevos (cron 2×/día
> en `patch-watch.yml`, o manual: `python3 wrlab.py winrates`).
> **Los callouts "Estado Meta Actual" de los reportes se toman de aquí** (TEMPLATE §A.1);
> alerta del vigía si un campeón se mueve ≥ 2 pts de win rate.

| Campeón | Rol | Tier | Win % | Pick % | Ban % | Tendencia | Confianza |
|---|---|---|---|---|---|---|---|
| Ahri | MID | A | 50.24 | 4.23 | 0.13 | ↓ 8 | Confidence Med |
| Caitlyn | DUO | A | 49.63 | 18.90 | 7.31 | 0 | Confidence High |
| Cho'Gath | SOLO | S | 50.64 | 10.68 | 35.44 | ↑ 2 | Confidence High |
| Cho'Gath | JUNGLE | S | 50.71 | 8.78 | 35.44 | 0 | Confidence High |
| Diana | MID | B | 47.89 | 1.05 | 0.15 | ↑ 3 | Confidence Low |
| Diana | JUNGLE | A | 50.22 | 1.45 | 0.15 | 0 | Confidence Low |
| Heimerdinger | MID | A | 49.88 | 1.69 | 1.32 | ↓ 1 | Confidence Low |
| Jinx | DUO | A | 50.55 | 12.51 | 0.44 | 0 | Confidence High |
| Kalista | DUO | A | 50.68 | 6.15 | 7.48 | 0 | Confidence Med |
| Kalista | SOLO | S+ | 53.63 | 2.51 | 7.48 | 0 | Confidence Low |
| Karma | SUPPORT | A | 49.73 | 4.27 | 0.35 | ↓ 1 | Confidence Med |
| Malphite | SUPPORT | S | 51.26 | 8.12 | 41.03 | ↓ 2 | Confidence High |
| Malphite | SOLO | S+ | 55.35 | 6.97 | 41.03 | 0 | Confidence Med |
| Malphite | MID | S+ | 52.04 | 1.00 | 41.03 | 0 | Confidence Low |
| Mordekaiser | SOLO | S+ | 50.64 | 11.54 | 30.14 | ↑ 4 | Confidence High |
| Nocturne | JUNGLE | S+ | 55.51 | 10.04 | 56.95 | ↑ 1 | Confidence High |
| Norra | MID | A | 50.70 | 1.38 | 7.09 | ↓ 1 | Confidence Low |
| Orianna | MID | A | 51.48 | 4.41 | 0.28 | ↓ 3 | Confidence Med |
| Ornn | SOLO | A | 51.26 | 1.95 | 0.18 | ↓ 3 | Confidence Low |
| Ornn | SUPPORT | B | 48.80 | 1.18 | 0.18 | ↓ 11 | Confidence Low |
| Rammus | JUNGLE | S+ | 57.38 | 4.44 | 6.49 | 0 | Confidence Med |
| Senna | DUO | S+ | 55.82 | 3.09 | 31.97 | 0 | Confidence Med |
| Senna | SUPPORT | S+ | 54.34 | 12.83 | 31.97 | 0 | Confidence High |
| Seraphine | SUPPORT | A | 49.22 | 6.26 | 1.04 | ↑ 7 | Confidence Med |
| Shyvana | JUNGLE | B | 46.10 | 3.43 | 1.11 | ↑ 1 | Confidence Med |
| Sivir | DUO | A | 48.81 | 3.34 | 0.05 | 0 | Confidence Med |
| Syndra | MID | S | 51.18 | 6.12 | 18.61 | ↓ 5 | Confidence Med |
| Volibear | SOLO | B | 48.22 | 4.73 | 4.30 | ↓ 1 | Confidence Med |
| Volibear | JUNGLE | B | 48.06 | 2.41 | 4.30 | 0 | Confidence Low |
| Xayah | DUO | A | 50.18 | 4.37 | 0.18 | 0 | Confidence Med |
| Yunara | DUO | S+ | 51.31 | 15.42 | 23.32 | 0 | Confidence High |
| Yuumi | SUPPORT | A | 49.14 | 9.13 | 33.03 | ↑ 2 | Confidence High |

Roles wr-meta: SOLO = top (Baron Lane) · JUNGLE · MID · DUO = ADC (Dragon Lane) · SUPPORT.
Máquina: `champion_winrates.csv` (mismas filas) · BD: tabla `winrates` (`build_db.py`).
Dato de CONTEXTO meta (secundario): no cambia builds por sí solo — si un movimiento
coincide con un hotfix, el flujo es el de FRAMEWORK §E (triage/annotate).
