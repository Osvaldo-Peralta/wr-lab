# Win rates del roster — wr-meta (Meta Overview)

> Bucket: **Diamond +** · Datos wr-meta: **Updated 05 OCT 2026 UTC 00:00** · Refrescado por el vigía: 05/10/2026
> Fuente: `wr-meta.com/{id}-{champ}.html` (bloque Meta Overview) vía
> `model/check_patch.py` paso 4 — el MISMO proceso que busca parches nuevos (cron 2×/día
> en `patch-watch.yml`, o manual: `python3 wrlab.py winrates`).
> **Los callouts "Estado Meta Actual" de los reportes se toman de aquí** (TEMPLATE §A.1);
> alerta del vigía si un campeón se mueve ≥ 2 pts de win rate.

| Campeón | Rol | Tier | Win % | Pick % | Ban % | Tendencia | Confianza |
|---|---|---|---|---|---|---|---|
| Ahri | MID | A | 50.77 | 4.28 | 0.13 | ↓ 2 | Confidence Med |
| Caitlyn | DUO | A | 49.69 | 21.72 | 15.43 | ↓ 1 | Confidence High |
| Cho'Gath | SOLO | S+ | 50.77 | 11.40 | 34.76 | ↑ 5 | Confidence High |
| Cho'Gath | JUNGLE | S | 50.35 | 8.33 | 34.76 | ↑ 1 | Confidence High |
| Diana | MID | B | 46.88 | 1.17 | 0.17 | 0 | Confidence Low |
| Diana | JUNGLE | A | 50.23 | 1.62 | 0.17 | ↓ 1 | Confidence Low |
| Heimerdinger | MID | A | 49.60 | 1.58 | 1.11 | 0 | Confidence Low |
| Jinx | DUO | A | 50.55 | 11.99 | 0.44 | 0 | Confidence High |
| Kalista | DUO | A | 50.88 | 5.35 | 5.31 | ↓ 1 | Confidence Med |
| Kalista | SOLO | S | 52.58 | 2.10 | 5.31 | ↓ 2 | Confidence Low |
| Karma | SUPPORT | A | 49.52 | 4.96 | 0.37 | ↑ 8 | Confidence Med |
| Malphite | SUPPORT | S+ | 51.92 | 7.23 | 44.98 | ↑ 2 | Confidence Med |
| Malphite | SOLO | S+ | 55.53 | 7.56 | 44.98 | 0 | Confidence Med |
| Mordekaiser | SOLO | S+ | 51.35 | 10.51 | 28.12 | ↑ 2 | Confidence High |
| Nocturne | JUNGLE | S+ | 55.13 | 9.42 | 39.95 | 0 | Confidence High |
| Norra | MID | A | 50.78 | 1.52 | 7.62 | ↓ 1 | Confidence Low |
| Orianna | MID | A | 51.55 | 4.63 | 0.26 | ↓ 1 | Confidence Med |
| Rammus | JUNGLE | S+ | 57.42 | 5.00 | 7.02 | 0 | Confidence Med |
| Seraphine | SUPPORT | A | 49.30 | 6.41 | 0.97 | ↓ 6 | Confidence Med |
| Shyvana | JUNGLE | B | 46.71 | 3.58 | 1.36 | ↑ 2 | Confidence Med |
| Sivir | DUO | B | 48.65 | 3.49 | 0.05 | 0 | Confidence Med |
| Syndra | MID | A | 50.76 | 6.77 | 25.33 | ↓ 6 | Confidence Med |
| Volibear | SOLO | B | 47.74 | 5.41 | 4.65 | ↓ 1 | Confidence Med |
| Volibear | JUNGLE | B | 47.40 | 2.47 | 4.65 | ↓ 5 | Confidence Low |
| Yunara | DUO | S+ | 51.64 | 16.83 | 23.80 | ↓ 1 | Confidence High |
| Yuumi | SUPPORT | A | 48.95 | 9.51 | 34.28 | ↓ 1 | Confidence High |

Roles wr-meta: SOLO = top (Baron Lane) · JUNGLE · MID · DUO = ADC (Dragon Lane) · SUPPORT.
Máquina: `champion_winrates.csv` (mismas filas) · BD: tabla `winrates` (`build_db.py`).
Dato de CONTEXTO meta (secundario): no cambia builds por sí solo — si un movimiento
coincide con un hotfix, el flujo es el de FRAMEWORK §E (triage/annotate).
