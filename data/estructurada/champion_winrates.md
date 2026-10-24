# Win rates del roster — wr-meta (Meta Overview)

> Bucket: **Diamond +** · Datos wr-meta: **Updated 24 OCT 2026 UTC 00:00** · Refrescado por el vigía: 24/10/2026
> Fuente: `wr-meta.com/{id}-{champ}.html` (bloque Meta Overview) vía
> `model/check_patch.py` paso 4 — el MISMO proceso que busca parches nuevos (cron 2×/día
> en `patch-watch.yml`, o manual: `python3 wrlab.py winrates`).
> **Los callouts "Estado Meta Actual" de los reportes se toman de aquí** (TEMPLATE §A.1);
> alerta del vigía si un campeón se mueve ≥ 2 pts de win rate.

| Campeón | Rol | Tier | Win % | Pick % | Ban % | Tendencia | Confianza |
|---|---|---|---|---|---|---|---|
| Ahri | MID | A | 50.76 | 4.61 | 0.16 | 0 | Confidence Med |
| Caitlyn | DUO | A | 50.12 | 16.27 | 4.94 | ↑ 1 | Confidence High |
| Cho'Gath | SOLO | S | 50.32 | 9.27 | 36.17 | ↑ 3 | Confidence High |
| Cho'Gath | JUNGLE | A | 50.52 | 8.26 | 36.17 | ↓ 4 | Confidence High |
| Diana | MID | B | 47.44 | 1.03 | 0.14 | ↑ 1 | Confidence Low |
| Diana | JUNGLE | A | 50.73 | 1.34 | 0.14 | ↑ 3 | Confidence Low |
| Heimerdinger | MID | A | 49.41 | 1.73 | 1.48 | ↓ 2 | Confidence Low |
| Jinx | DUO | A | 50.53 | 13.01 | 0.53 | 0 | Confidence High |
| Kalista | DUO | A | 50.56 | 7.38 | 10.30 | 0 | Confidence Med |
| Kalista | SOLO | S+ | 53.82 | 2.78 | 10.30 | ↑ 1 | Confidence Low |
| Karma | SUPPORT | A | 49.96 | 4.74 | 0.41 | ↓ 4 | Confidence Med |
| Malphite | SUPPORT | S+ | 51.59 | 9.48 | 42.44 | ↓ 1 | Confidence High |
| Malphite | SOLO | S+ | 54.80 | 7.64 | 42.44 | 0 | Confidence Med |
| Mordekaiser | SOLO | S+ | 51.55 | 11.54 | 32.62 | ↑ 1 | Confidence High |
| Nocturne | JUNGLE | S+ | 52.63 | 6.75 | 59.22 | ↑ 1 | Confidence Med |
| Norra | MID | S | 51.03 | 1.36 | 6.89 | ↑ 6 | Confidence Low |
| Orianna | MID | S | 51.47 | 4.42 | 0.33 | ↑ 2 | Confidence Med |
| Ornn | SOLO | A | 50.62 | 1.85 | 0.18 | ↓ 3 | Confidence Low |
| Ornn | SUPPORT | B | 49.22 | 1.31 | 0.18 | 0 | Confidence Low |
| Rammus | JUNGLE | S+ | 55.64 | 4.13 | 7.07 | 0 | Confidence Med |
| Senna | SUPPORT | S | 50.13 | 6.78 | 13.39 | ↑ 4 | Confidence Med |
| Seraphine | SUPPORT | A | 49.57 | 6.33 | 1.14 | ↓ 3 | Confidence Med |
| Shyvana | JUNGLE | B | 46.46 | 3.06 | 0.95 | 0 | Confidence Med |
| Sivir | DUO | A | 49.83 | 3.89 | 0.07 | ↑ 3 | Confidence Med |
| Syndra | MID | S+ | 51.90 | 5.92 | 18.35 | 0 | Confidence Med |
| Volibear | SOLO | A | 48.64 | 8.57 | 8.13 | ↑ 1 | Confidence High |
| Volibear | JUNGLE | A | 49.10 | 4.65 | 8.13 | 0 | Confidence Med |
| Xayah | DUO | A | 50.91 | 5.01 | 0.23 | ↓ 1 | Confidence Med |
| Yunara | DUO | A | 49.23 | 6.11 | 12.33 | ↓ 3 | Confidence Med |
| Yuumi | SUPPORT | A | 48.11 | 8.38 | 33.90 | 0 | Confidence High |

Roles wr-meta: SOLO = top (Baron Lane) · JUNGLE · MID · DUO = ADC (Dragon Lane) · SUPPORT.
Máquina: `champion_winrates.csv` (mismas filas) · BD: tabla `winrates` (`build_db.py`).
Dato de CONTEXTO meta (secundario): no cambia builds por sí solo — si un movimiento
coincide con un hotfix, el flujo es el de FRAMEWORK §E (triage/annotate).
