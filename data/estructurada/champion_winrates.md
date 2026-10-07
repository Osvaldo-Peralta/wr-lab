# Win rates del roster — wr-meta (Meta Overview)

> Bucket: **Diamond +** · Datos wr-meta: **Updated 07 OCT 2026 UTC 00:00** · Refrescado por el vigía: 07/10/2026
> Fuente: `wr-meta.com/{id}-{champ}.html` (bloque Meta Overview) vía
> `model/check_patch.py` paso 4 — el MISMO proceso que busca parches nuevos (cron 2×/día
> en `patch-watch.yml`, o manual: `python3 wrlab.py winrates`).
> **Los callouts "Estado Meta Actual" de los reportes se toman de aquí** (TEMPLATE §A.1);
> alerta del vigía si un campeón se mueve ≥ 2 pts de win rate.

| Campeón | Rol | Tier | Win % | Pick % | Ban % | Tendencia | Confianza |
|---|---|---|---|---|---|---|---|
| Ahri | MID | A | 50.66 | 4.27 | 0.13 | 0 | Confidence Med |
| Caitlyn | DUO | A | 49.41 | 20.88 | 12.67 | ↓ 2 | Confidence High |
| Cho'Gath | SOLO | S | 50.75 | 11.31 | 35.12 | 0 | Confidence High |
| Cho'Gath | JUNGLE | S | 50.68 | 8.31 | 35.12 | ↑ 2 | Confidence High |
| Diana | MID | B | 47.49 | 1.16 | 0.16 | ↓ 1 | Confidence Low |
| Diana | JUNGLE | A | 50.54 | 1.58 | 0.16 | ↑ 2 | Confidence Low |
| Heimerdinger | MID | A | 49.78 | 1.61 | 1.15 | ↓ 1 | Confidence Low |
| Jinx | DUO | A | 50.54 | 12.09 | 0.44 | 0 | Confidence High |
| Kalista | DUO | A | 51.22 | 5.58 | 5.68 | ↓ 1 | Confidence Med |
| Kalista | SOLO | S+ | 53.37 | 2.16 | 5.68 | 0 | Confidence Low |
| Karma | SUPPORT | A | 49.99 | 4.88 | 0.36 | ↑ 5 | Confidence Med |
| Malphite | SUPPORT | S+ | 51.51 | 7.36 | 44.26 | ↑ 1 | Confidence Med |
| Malphite | SOLO | S+ | 55.33 | 7.38 | 44.26 | 0 | Confidence Med |
| Mordekaiser | SOLO | S | 51.07 | 10.54 | 28.52 | ↓ 1 | Confidence High |
| Nocturne | JUNGLE | S+ | 55.13 | 9.47 | 43.77 | 0 | Confidence High |
| Norra | MID | S | 51.07 | 1.52 | 7.54 | ↑ 3 | Confidence Low |
| Orianna | MID | A | 51.46 | 4.50 | 0.27 | ↑ 1 | Confidence Med |
| Rammus | JUNGLE | S+ | 56.49 | 4.81 | 7.08 | ↓ 1 | Confidence Med |
| Seraphine | SUPPORT | A | 49.60 | 6.54 | 0.96 | ↑ 1 | Confidence Med |
| Shyvana | JUNGLE | B | 46.12 | 3.43 | 1.25 | ↑ 2 | Confidence Med |
| Sivir | DUO | A | 48.69 | 3.53 | 0.05 | ↑ 3 | Confidence Med |
| Syndra | MID | S+ | 51.33 | 6.70 | 23.82 | ↑ 1 | Confidence Med |
| Volibear | SOLO | B | 47.85 | 5.22 | 4.55 | ↓ 2 | Confidence Med |
| Volibear | JUNGLE | A | 48.18 | 2.39 | 4.55 | ↑ 1 | Confidence Low |
| Yunara | DUO | S+ | 51.49 | 16.53 | 24.10 | 0 | Confidence High |
| Yuumi | SUPPORT | A | 48.90 | 9.67 | 34.38 | ↑ 2 | Confidence High |

Roles wr-meta: SOLO = top (Baron Lane) · JUNGLE · MID · DUO = ADC (Dragon Lane) · SUPPORT.
Máquina: `champion_winrates.csv` (mismas filas) · BD: tabla `winrates` (`build_db.py`).
Dato de CONTEXTO meta (secundario): no cambia builds por sí solo — si un movimiento
coincide con un hotfix, el flujo es el de FRAMEWORK §E (triage/annotate).
