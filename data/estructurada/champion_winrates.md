# Win rates del roster — wr-meta (Meta Overview)

> Bucket: **Diamond +** · Datos wr-meta: **Updated 04 OCT 2026 UTC 00:00** · Refrescado por el vigía: 04/10/2026
> Fuente: `wr-meta.com/{id}-{champ}.html` (bloque Meta Overview) vía
> `model/check_patch.py` paso 4 — el MISMO proceso que busca parches nuevos (cron 2×/día
> en `patch-watch.yml`, o manual: `python3 wrlab.py winrates`).
> **Los callouts "Estado Meta Actual" de los reportes se toman de aquí** (TEMPLATE §A.1);
> alerta del vigía si un campeón se mueve ≥ 2 pts de win rate.

| Campeón | Rol | Tier | Win % | Pick % | Ban % | Tendencia | Confianza |
|---|---|---|---|---|---|---|---|
| Caitlyn | DUO | S | 49.68 | 22.38 | 17.37 | ↑ 2 | Confidence High |
| Cho'Gath | SOLO | A | 50.34 | 11.63 | 34.40 | ↓ 4 | Confidence High |
| Cho'Gath | JUNGLE | A | 50.38 | 8.32 | 34.40 | ↓ 2 | Confidence High |
| Diana | MID | B | 46.57 | 1.17 | 0.19 | ↓ 3 | Confidence Low |
| Diana | JUNGLE | A | 50.58 | 1.70 | 0.19 | ↑ 2 | Confidence Low |
| Heimerdinger | MID | A | 49.62 | 1.58 | 1.11 | ↓ 5 | Confidence Low |
| Jinx | DUO | A | 50.65 | 11.84 | 0.42 | 0 | Confidence High |
| Kalista | DUO | S | 51.09 | 5.20 | 5.06 | ↑ 1 | Confidence Med |
| Kalista | SOLO | S+ | 52.95 | 2.13 | 5.06 | ↑ 1 | Confidence Low |
| Karma | SUPPORT | A | 49.20 | 5.06 | 0.37 | ↓ 1 | Confidence Med |
| Malphite | SUPPORT | S+ | 51.47 | 7.23 | 45.22 | ↓ 1 | Confidence Med |
| Malphite | SOLO | S+ | 55.30 | 7.67 | 45.22 | 0 | Confidence Med |
| Mordekaiser | SOLO | S | 51.25 | 10.43 | 27.99 | ↓ 1 | Confidence High |
| Norra | MID | A | 51.10 | 1.54 | 7.80 | 0 | Confidence Low |
| Rammus | JUNGLE | S+ | 57.33 | 4.97 | 6.65 | 0 | Confidence Med |
| Seraphine | SUPPORT | A | 49.56 | 6.45 | 0.97 | ↑ 3 | Confidence Med |
| Shyvana | JUNGLE | B | 45.86 | 3.70 | 1.40 | ↓ 1 | Confidence Med |
| Sivir | DUO | B | 48.40 | 3.46 | 0.05 | ↑ 1 | Confidence Med |
| Volibear | SOLO | A | 48.10 | 5.51 | 4.65 | ↑ 1 | Confidence Med |
| Volibear | JUNGLE | B | 48.11 | 2.54 | 4.65 | 0 | Confidence Low |
| Yunara | DUO | S+ | 51.84 | 17.19 | 23.57 | ↑ 1 | Confidence High |
| Yuumi | SUPPORT | A | 48.95 | 9.46 | 34.38 | ↑ 2 | Confidence High |

Roles wr-meta: SOLO = top (Baron Lane) · JUNGLE · MID · DUO = ADC (Dragon Lane) · SUPPORT.
Máquina: `champion_winrates.csv` (mismas filas) · BD: tabla `winrates` (`build_db.py`).
Dato de CONTEXTO meta (secundario): no cambia builds por sí solo — si un movimiento
coincide con un hotfix, el flujo es el de FRAMEWORK §E (triage/annotate).
