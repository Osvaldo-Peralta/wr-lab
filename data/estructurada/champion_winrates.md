# Win rates del roster — wr-meta (Meta Overview)

> Bucket: **Diamond +** · Datos wr-meta: **Updated 01 OCT 2026 UTC 00:00** · Refrescado por el vigía: 01/10/2026
> Fuente: `wr-meta.com/{id}-{champ}.html` (bloque Meta Overview) vía
> `model/check_patch.py` paso 4 — el MISMO proceso que busca parches nuevos (cron 2×/día
> en `patch-watch.yml`, o manual: `python3 wrlab.py winrates`).
> **Los callouts "Estado Meta Actual" de los reportes se toman de aquí** (TEMPLATE §A.1);
> alerta del vigía si un campeón se mueve ≥ 2 pts de win rate.

| Campeón | Rol | Tier | Win % | Pick % | Ban % | Tendencia | Confianza |
|---|---|---|---|---|---|---|---|
| Caitlyn | DUO | A | 50.44 | 25.95 | 27.38 | ↓ 10 | Confidence High |
| Cho'Gath | SOLO | A | 50.17 | 12.72 | 33.10 | ↓ 2 | Confidence High |
| Cho'Gath | JUNGLE | A | 50.41 | 8.64 | 33.10 | ↓ 3 | Confidence High |
| Diana | MID | B | 47.95 | 1.16 | 0.18 | ↓ 2 | Confidence Low |
| Diana | JUNGLE | A | 50.35 | 1.74 | 0.18 | ↑ 5 | Confidence Low |
| Heimerdinger | MID | A | 50.49 | 1.52 | 1.01 | ↓ 3 | Confidence Low |
| Jinx | DUO | A | 50.55 | 11.30 | 0.41 | 0 | Confidence High |
| Kalista | DUO | S | 51.12 | 4.65 | 4.19 | ↑ 1 | Confidence Med |
| Kalista | SOLO | S+ | 53.01 | 2.05 | 4.19 | ↑ 4 | Confidence Low |
| Karma | SUPPORT | A | 49.19 | 5.13 | 0.38 | ↓ 5 | Confidence Med |
| Malphite | SUPPORT | S+ | 51.51 | 7.30 | 46.65 | ↓ 2 | Confidence Med |
| Malphite | SOLO | S+ | 56.44 | 9.32 | 46.65 | 0 | Confidence High |
| Mordekaiser | SOLO | S | 50.87 | 10.83 | 27.69 | 0 | Confidence High |
| Norra | MID | A | 50.06 | 1.57 | 7.98 | ↑ 1 | Confidence Low |
| Rammus | JUNGLE | S+ | 56.81 | 5.42 | 5.84 | 0 | Confidence Med |
| Seraphine | SUPPORT | A | 49.30 | 6.88 | 0.96 | ↓ 1 | Confidence Med |
| Shyvana | JUNGLE | B | 46.14 | 3.76 | 1.45 | 0 | Confidence Med |
| Sivir | DUO | B | 48.08 | 3.45 | 0.05 | ↓ 1 | Confidence Med |
| Volibear | SOLO | B | 47.53 | 5.87 | 4.65 | ↓ 3 | Confidence Med |
| Volibear | JUNGLE | B | 47.97 | 2.51 | 4.65 | 0 | Confidence Low |
| Yunara | DUO | S | 50.91 | 18.06 | 22.13 | ↑ 1 | Confidence High |
| Yuumi | SUPPORT | A | 48.90 | 10.43 | 34.20 | ↓ 5 | Confidence High |

Roles wr-meta: SOLO = top (Baron Lane) · JUNGLE · MID · DUO = ADC (Dragon Lane) · SUPPORT.
Máquina: `champion_winrates.csv` (mismas filas) · BD: tabla `winrates` (`build_db.py`).
Dato de CONTEXTO meta (secundario): no cambia builds por sí solo — si un movimiento
coincide con un hotfix, el flujo es el de FRAMEWORK §E (triage/annotate).
