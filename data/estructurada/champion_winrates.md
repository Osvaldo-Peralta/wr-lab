# Win rates del roster — wr-meta (Meta Overview)

> Bucket: **Diamond +** · Datos wr-meta: **Updated 03 OCT 2026 UTC 00:00** · Refrescado por el vigía: 03/10/2026
> Fuente: `wr-meta.com/{id}-{champ}.html` (bloque Meta Overview) vía
> `model/check_patch.py` paso 4 — el MISMO proceso que busca parches nuevos (cron 2×/día
> en `patch-watch.yml`, o manual: `python3 wrlab.py winrates`).
> **Los callouts "Estado Meta Actual" de los reportes se toman de aquí** (TEMPLATE §A.1);
> alerta del vigía si un campeón se mueve ≥ 2 pts de win rate.

| Campeón | Rol | Tier | Win % | Pick % | Ban % | Tendencia | Confianza |
|---|---|---|---|---|---|---|---|
| Caitlyn | DUO | A | 49.35 | 22.99 | 19.79 | 0 | Confidence High |
| Cho'Gath | SOLO | S+ | 50.63 | 11.89 | 34.01 | ↑ 8 | Confidence High |
| Cho'Gath | JUNGLE | S | 50.50 | 8.34 | 34.01 | 0 | Confidence High |
| Diana | MID | B | 47.78 | 1.15 | 0.19 | ↑ 3 | Confidence Low |
| Diana | JUNGLE | A | 50.14 | 1.76 | 0.19 | ↓ 7 | Confidence Low |
| Heimerdinger | MID | A | 50.15 | 1.59 | 1.08 | 0 | Confidence Low |
| Jinx | DUO | A | 50.91 | 11.61 | 0.43 | 0 | Confidence High |
| Kalista | DUO | A | 51.08 | 5.10 | 4.85 | 0 | Confidence Med |
| Kalista | SOLO | S | 52.58 | 2.10 | 4.85 | ↓ 1 | Confidence Low |
| Karma | SUPPORT | A | 49.15 | 4.96 | 0.38 | ↓ 4 | Confidence Med |
| Malphite | SUPPORT | S+ | 51.64 | 7.10 | 45.43 | ↓ 1 | Confidence Med |
| Malphite | SOLO | S+ | 55.58 | 7.81 | 45.43 | 0 | Confidence Med |
| Mordekaiser | SOLO | S+ | 51.43 | 10.46 | 27.73 | ↑ 1 | Confidence High |
| Norra | MID | S | 51.01 | 1.52 | 8.00 | ↑ 5 | Confidence Low |
| Rammus | JUNGLE | S+ | 56.81 | 4.78 | 6.43 | 0 | Confidence Med |
| Seraphine | SUPPORT | A | 49.75 | 6.63 | 0.96 | ↑ 4 | Confidence Med |
| Shyvana | JUNGLE | B | 46.18 | 3.69 | 1.46 | ↓ 1 | Confidence Med |
| Sivir | DUO | B | 48.07 | 3.48 | 0.06 | ↓ 1 | Confidence Med |
| Volibear | SOLO | A | 47.88 | 5.64 | 4.77 | ↑ 2 | Confidence Med |
| Volibear | JUNGLE | A | 48.43 | 2.49 | 4.77 | ↑ 5 | Confidence Low |
| Yunara | DUO | S+ | 51.84 | 17.44 | 23.16 | ↑ 1 | Confidence High |
| Yuumi | SUPPORT | A | 48.56 | 9.52 | 34.34 | ↓ 7 | Confidence High |

Roles wr-meta: SOLO = top (Baron Lane) · JUNGLE · MID · DUO = ADC (Dragon Lane) · SUPPORT.
Máquina: `champion_winrates.csv` (mismas filas) · BD: tabla `winrates` (`build_db.py`).
Dato de CONTEXTO meta (secundario): no cambia builds por sí solo — si un movimiento
coincide con un hotfix, el flujo es el de FRAMEWORK §E (triage/annotate).
