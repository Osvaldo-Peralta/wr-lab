# Win rates del roster — wr-meta (Meta Overview)

> Bucket: **Diamond +** · Datos wr-meta: **Updated 26 OCT 2026 UTC 00:00** · Refrescado por el vigía: 26/10/2026
> Fuente: `wr-meta.com/{id}-{champ}.html` (bloque Meta Overview) vía
> `model/check_patch.py` paso 4 — el MISMO proceso que busca parches nuevos (cron 2×/día
> en `patch-watch.yml`, o manual: `python3 wrlab.py winrates`).
> **Los callouts "Estado Meta Actual" de los reportes se toman de aquí** (TEMPLATE §A.1);
> alerta del vigía si un campeón se mueve ≥ 2 pts de win rate.

| Campeón | Rol | Tier | Win % | Pick % | Ban % | Tendencia | Confianza |
|---|---|---|---|---|---|---|---|
| Ahri | MID | A | 50.99 | 4.81 | 0.15 | ↓ 2 | Confidence Med |
| Caitlyn | DUO | A | 49.84 | 15.73 | 4.86 | ↓ 1 | Confidence High |
| Cho'Gath | SOLO | A | 49.80 | 9.40 | 35.84 | ↓ 3 | Confidence High |
| Cho'Gath | JUNGLE | S | 50.21 | 8.24 | 35.84 | ↓ 1 | Confidence High |
| Diana | MID | B | 47.15 | 1.07 | 0.16 | ↑ 1 | Confidence Low |
| Diana | JUNGLE | A | 50.44 | 1.36 | 0.16 | 0 | Confidence Low |
| Heimerdinger | MID | A | 50.22 | 1.72 | 1.57 | ↑ 8 | Confidence Low |
| Jinx | DUO | A | 50.38 | 12.67 | 0.56 | 0 | Confidence High |
| Kalista | DUO | S | 50.64 | 7.84 | 10.98 | ↑ 1 | Confidence Med |
| Kalista | SOLO | S+ | 53.49 | 2.78 | 10.98 | 0 | Confidence Low |
| Karma | SUPPORT | A | 49.98 | 4.73 | 0.44 | ↓ 2 | Confidence Med |
| Malphite | SUPPORT | S+ | 51.55 | 9.47 | 42.31 | ↓ 2 | Confidence High |
| Malphite | SOLO | S+ | 54.62 | 7.41 | 42.31 | 0 | Confidence Med |
| Mordekaiser | SOLO | S | 51.15 | 11.32 | 32.47 | ↓ 1 | Confidence High |
| Nocturne | JUNGLE | S+ | 52.05 | 6.83 | 58.07 | ↓ 4 | Confidence Med |
| Norra | MID | S | 50.89 | 1.31 | 6.86 | ↑ 8 | Confidence Low |
| Orianna | MID | S | 51.89 | 4.54 | 0.35 | ↑ 1 | Confidence Med |
| Ornn | SOLO | A | 51.31 | 1.98 | 0.21 | ↑ 2 | Confidence Low |
| Ornn | SUPPORT | A | 50.09 | 1.37 | 0.21 | ↑ 2 | Confidence Low |
| Rammus | JUNGLE | S+ | 56.52 | 3.88 | 6.82 | ↑ 1 | Confidence Med |
| Senna | SUPPORT | A | 49.74 | 6.68 | 12.07 | ↓ 1 | Confidence Med |
| Seraphine | SUPPORT | A | 49.79 | 6.52 | 1.13 | ↓ 3 | Confidence Med |
| Shyvana | JUNGLE | B | 46.46 | 3.02 | 0.98 | 0 | Confidence Med |
| Sivir | DUO | A | 49.38 | 4.90 | 0.08 | 0 | Confidence Med |
| Syndra | MID | S+ | 51.88 | 5.89 | 17.73 | ↑ 5 | Confidence Med |
| Volibear | SOLO | A | 49.26 | 8.24 | 8.28 | ↑ 5 | Confidence High |
| Volibear | JUNGLE | A | 48.82 | 4.30 | 8.28 | ↓ 1 | Confidence Med |
| Xayah | DUO | A | 50.57 | 4.96 | 0.21 | ↓ 1 | Confidence Med |
| Yunara | DUO | A | 49.30 | 5.63 | 11.40 | ↓ 2 | Confidence Med |
| Yuumi | SUPPORT | A | 48.05 | 8.05 | 33.73 | 0 | Confidence High |

Roles wr-meta: SOLO = top (Baron Lane) · JUNGLE · MID · DUO = ADC (Dragon Lane) · SUPPORT.
Máquina: `champion_winrates.csv` (mismas filas) · BD: tabla `winrates` (`build_db.py`).
Dato de CONTEXTO meta (secundario): no cambia builds por sí solo — si un movimiento
coincide con un hotfix, el flujo es el de FRAMEWORK §E (triage/annotate).
