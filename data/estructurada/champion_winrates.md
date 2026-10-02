# Win rates del roster — wr-meta (Meta Overview)

> Bucket: **Diamond +** · Datos wr-meta: **Updated 02 OCT 2026 UTC 00:00** · Refrescado por el vigía: 02/10/2026
> Fuente: `wr-meta.com/{id}-{champ}.html` (bloque Meta Overview) vía
> `model/check_patch.py` paso 4 — el MISMO proceso que busca parches nuevos (cron 2×/día
> en `patch-watch.yml`, o manual: `python3 wrlab.py winrates`).
> **Los callouts "Estado Meta Actual" de los reportes se toman de aquí** (TEMPLATE §A.1);
> alerta del vigía si un campeón se mueve ≥ 2 pts de win rate.

| Campeón | Rol | Tier | Win % | Pick % | Ban % | Tendencia | Confianza |
|---|---|---|---|---|---|---|---|
| Caitlyn | DUO | A | 49.48 | 23.40 | 22.15 | ↓ 2 | Confidence High |
| Cho'Gath | SOLO | A | 50.15 | 12.19 | 33.81 | ↓ 3 | Confidence High |
| Cho'Gath | JUNGLE | S | 50.67 | 8.53 | 33.81 | ↑ 2 | Confidence High |
| Diana | MID | B | 47.40 | 1.16 | 0.17 | ↓ 4 | Confidence Low |
| Diana | JUNGLE | A | 50.91 | 1.72 | 0.17 | ↑ 7 | Confidence Low |
| Heimerdinger | MID | A | 50.40 | 1.59 | 1.06 | ↓ 3 | Confidence Low |
| Jinx | DUO | S | 51.10 | 11.58 | 0.43 | ↑ 2 | Confidence High |
| Kalista | DUO | A | 51.18 | 4.86 | 4.58 | ↓ 1 | Confidence Med |
| Kalista | SOLO | S+ | 53.82 | 2.16 | 4.58 | 0 | Confidence Low |
| Karma | SUPPORT | A | 49.32 | 5.08 | 0.40 | ↑ 4 | Confidence Med |
| Malphite | SUPPORT | S+ | 51.78 | 7.14 | 46.21 | ↑ 2 | Confidence Med |
| Malphite | SOLO | S+ | 55.69 | 8.12 | 46.21 | ↓ 1 | Confidence High |
| Mordekaiser | SOLO | S+ | 51.35 | 10.54 | 27.95 | ↑ 3 | Confidence High |
| Norra | MID | A | 50.42 | 1.57 | 7.94 | ↑ 1 | Confidence Low |
| Rammus | JUNGLE | S+ | 56.74 | 4.79 | 6.15 | 0 | Confidence Med |
| Seraphine | SUPPORT | A | 49.21 | 6.74 | 0.97 | ↓ 4 | Confidence Med |
| Shyvana | JUNGLE | B | 46.43 | 3.70 | 1.39 | ↑ 2 | Confidence Med |
| Sivir | DUO | A | 48.57 | 3.53 | 0.05 | ↑ 1 | Confidence Med |
| Volibear | SOLO | A | 47.79 | 5.68 | 4.61 | ↑ 1 | Confidence Med |
| Volibear | JUNGLE | B | 46.87 | 2.48 | 4.61 | ↓ 4 | Confidence Low |
| Yunara | DUO | S+ | 51.22 | 17.62 | 22.51 | ↑ 1 | Confidence High |
| Yuumi | SUPPORT | A | 49.23 | 9.82 | 34.21 | ↑ 6 | Confidence High |

Roles wr-meta: SOLO = top (Baron Lane) · JUNGLE · MID · DUO = ADC (Dragon Lane) · SUPPORT.
Máquina: `champion_winrates.csv` (mismas filas) · BD: tabla `winrates` (`build_db.py`).
Dato de CONTEXTO meta (secundario): no cambia builds por sí solo — si un movimiento
coincide con un hotfix, el flujo es el de FRAMEWORK §E (triage/annotate).
