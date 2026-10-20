# Win rates del roster — wr-meta (Meta Overview)

> Bucket: **Diamond +** · Datos wr-meta: **Updated 20 OCT 2026 UTC 00:00** · Refrescado por el vigía: 20/10/2026
> Fuente: `wr-meta.com/{id}-{champ}.html` (bloque Meta Overview) vía
> `model/check_patch.py` paso 4 — el MISMO proceso que busca parches nuevos (cron 2×/día
> en `patch-watch.yml`, o manual: `python3 wrlab.py winrates`).
> **Los callouts "Estado Meta Actual" de los reportes se toman de aquí** (TEMPLATE §A.1);
> alerta del vigía si un campeón se mueve ≥ 2 pts de win rate.

| Campeón | Rol | Tier | Win % | Pick % | Ban % | Tendencia | Confianza |
|---|---|---|---|---|---|---|---|
| Ahri | MID | S | 51.24 | 4.57 | 0.14 | ↑ 6 | Confidence Med |
| Caitlyn | DUO | A | 49.86 | 15.75 | 5.73 | ↑ 2 | Confidence High |
| Cho'Gath | SOLO | S+ | 50.68 | 9.68 | 36.10 | ↑ 5 | Confidence High |
| Cho'Gath | JUNGLE | S | 50.51 | 8.52 | 36.10 | ↑ 4 | Confidence High |
| Diana | MID | B | 47.53 | 1.08 | 0.15 | ↓ 1 | Confidence Low |
| Diana | JUNGLE | A | 50.88 | 1.40 | 0.15 | ↓ 1 | Confidence Low |
| Heimerdinger | MID | A | 49.43 | 1.65 | 1.41 | ↓ 1 | Confidence Low |
| Jinx | DUO | A | 50.73 | 12.71 | 0.51 | ↑ 1 | Confidence High |
| Kalista | DUO | S | 50.61 | 7.41 | 8.98 | ↑ 1 | Confidence Med |
| Kalista | SOLO | S+ | 53.37 | 2.51 | 8.98 | ↓ 1 | Confidence Low |
| Karma | SUPPORT | A | 49.73 | 4.63 | 0.39 | ↓ 5 | Confidence Med |
| Malphite | SUPPORT | S+ | 51.78 | 9.31 | 41.61 | ↑ 1 | Confidence High |
| Malphite | SOLO | S+ | 55.00 | 7.32 | 41.61 | ↓ 1 | Confidence Med |
| Mordekaiser | SOLO | S | 51.11 | 10.89 | 30.91 | ↓ 2 | Confidence High |
| Nocturne | JUNGLE | S+ | 52.51 | 6.98 | 58.16 | ↑ 2 | Confidence Med |
| Norra | MID | A | 49.90 | 1.53 | 6.98 | ↑ 3 | Confidence Low |
| Orianna | MID | S | 52.22 | 4.56 | 0.31 | ↑ 1 | Confidence Med |
| Ornn | SOLO | A | 51.28 | 1.83 | 0.19 | ↑ 11 | Confidence Low |
| Ornn | SUPPORT | B | 49.14 | 1.28 | 0.19 | ↓ 6 | Confidence Low |
| Rammus | JUNGLE | S+ | 56.17 | 3.84 | 6.98 | 0 | Confidence Med |
| Senna | SUPPORT | S | 49.92 | 7.39 | 18.51 | ↑ 6 | Confidence Med |
| Seraphine | SUPPORT | A | 49.83 | 6.54 | 1.10 | ↑ 7 | Confidence Med |
| Shyvana | JUNGLE | B | 46.60 | 3.31 | 1.09 | 0 | Confidence Med |
| Sivir | DUO | A | 49.57 | 3.99 | 0.07 | ↓ 4 | Confidence Med |
| Syndra | MID | S+ | 51.85 | 5.88 | 18.77 | ↓ 1 | Confidence Med |
| Volibear | SOLO | A | 48.49 | 9.41 | 8.29 | ↑ 2 | Confidence High |
| Volibear | JUNGLE | A | 49.49 | 4.97 | 8.29 | ↑ 3 | Confidence Med |
| Xayah | DUO | A | 50.41 | 4.96 | 0.20 | ↓ 3 | Confidence Med |
| Yunara | DUO | A | 49.50 | 6.90 | 15.90 | 0 | Confidence Med |
| Yuumi | SUPPORT | A | 48.26 | 8.40 | 34.22 | ↑ 1 | Confidence High |

Roles wr-meta: SOLO = top (Baron Lane) · JUNGLE · MID · DUO = ADC (Dragon Lane) · SUPPORT.
Máquina: `champion_winrates.csv` (mismas filas) · BD: tabla `winrates` (`build_db.py`).
Dato de CONTEXTO meta (secundario): no cambia builds por sí solo — si un movimiento
coincide con un hotfix, el flujo es el de FRAMEWORK §E (triage/annotate).
