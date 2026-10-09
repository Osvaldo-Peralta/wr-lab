# Win rates del roster — wr-meta (Meta Overview)

> Bucket: **Diamond +** · Datos wr-meta: **Updated 09 OCT 2026 UTC 00:00** · Refrescado por el vigía: 09/10/2026
> Fuente: `wr-meta.com/{id}-{champ}.html` (bloque Meta Overview) vía
> `model/check_patch.py` paso 4 — el MISMO proceso que busca parches nuevos (cron 2×/día
> en `patch-watch.yml`, o manual: `python3 wrlab.py winrates`).
> **Los callouts "Estado Meta Actual" de los reportes se toman de aquí** (TEMPLATE §A.1);
> alerta del vigía si un campeón se mueve ≥ 2 pts de win rate.

| Campeón | Rol | Tier | Win % | Pick % | Ban % | Tendencia | Confianza |
|---|---|---|---|---|---|---|---|
| Ahri | MID | A | 50.52 | 4.26 | 0.12 | ↑ 3 | Confidence Med |
| Caitlyn | DUO | A | 49.70 | 20.58 | 10.79 | ↑ 1 | Confidence High |
| Cho'Gath | SOLO | S | 50.46 | 11.10 | 35.10 | ↑ 3 | Confidence High |
| Cho'Gath | JUNGLE | S | 50.85 | 8.52 | 35.10 | ↑ 1 | Confidence High |
| Diana | MID | B | 47.14 | 1.10 | 0.16 | ↑ 1 | Confidence Low |
| Diana | JUNGLE | A | 49.67 | 1.45 | 0.16 | ↑ 1 | Confidence Low |
| Heimerdinger | MID | A | 50.16 | 1.70 | 1.23 | ↓ 1 | Confidence Low |
| Jinx | DUO | A | 50.69 | 12.16 | 0.46 | ↓ 2 | Confidence High |
| Kalista | DUO | A | 50.70 | 5.70 | 6.30 | ↑ 1 | Confidence Med |
| Kalista | SOLO | S+ | 53.35 | 2.38 | 6.30 | 0 | Confidence Low |
| Karma | SUPPORT | A | 49.77 | 4.76 | 0.37 | ↑ 7 | Confidence Med |
| Malphite | SUPPORT | S | 51.07 | 7.53 | 42.85 | ↓ 1 | Confidence Med |
| Malphite | SOLO | S+ | 55.55 | 7.24 | 42.85 | 0 | Confidence Med |
| Mordekaiser | SOLO | S+ | 51.73 | 10.59 | 29.24 | ↑ 3 | Confidence High |
| Nocturne | JUNGLE | S+ | 55.46 | 10.42 | 46.04 | 0 | Confidence High |
| Norra | MID | S | 51.21 | 1.50 | 7.62 | ↑ 5 | Confidence Low |
| Orianna | MID | A | 51.67 | 4.50 | 0.27 | 0 | Confidence Med |
| Ornn | SOLO | A | 51.76 | 2.08 | 0.17 | ↑ 1 | Confidence Low |
| Ornn | SUPPORT | A | 48.90 | 1.14 | 0.17 | ↑ 4 | Confidence Low |
| Rammus | JUNGLE | S+ | 57.13 | 4.80 | 6.60 | 0 | Confidence Med |
| Seraphine | SUPPORT | A | 49.59 | 6.59 | 1.03 | ↑ 1 | Confidence Med |
| Shyvana | JUNGLE | B | 46.13 | 3.41 | 1.25 | 0 | Confidence Med |
| Sivir | DUO | A | 48.78 | 3.54 | 0.06 | ↑ 1 | Confidence Med |
| Syndra | MID | S | 50.86 | 6.51 | 21.08 | ↓ 1 | Confidence Med |
| Volibear | SOLO | A | 48.25 | 5.03 | 4.51 | 0 | Confidence Med |
| Volibear | JUNGLE | B | 48.31 | 2.34 | 4.51 | ↓ 2 | Confidence Low |
| Xayah | DUO | A | 50.44 | 4.49 | 0.18 | 0 | Confidence Med |
| Yunara | DUO | S+ | 51.67 | 15.97 | 23.02 | ↑ 1 | Confidence High |
| Yuumi | SUPPORT | A | 48.70 | 9.25 | 33.79 | ↓ 3 | Confidence High |

Roles wr-meta: SOLO = top (Baron Lane) · JUNGLE · MID · DUO = ADC (Dragon Lane) · SUPPORT.
Máquina: `champion_winrates.csv` (mismas filas) · BD: tabla `winrates` (`build_db.py`).
Dato de CONTEXTO meta (secundario): no cambia builds por sí solo — si un movimiento
coincide con un hotfix, el flujo es el de FRAMEWORK §E (triage/annotate).
