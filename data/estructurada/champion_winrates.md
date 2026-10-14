# Win rates del roster — wr-meta (Meta Overview)

> Bucket: **Diamond +** · Datos wr-meta: **Updated 14 OCT 2026 UTC 00:00** · Refrescado por el vigía: 14/10/2026
> Fuente: `wr-meta.com/{id}-{champ}.html` (bloque Meta Overview) vía
> `model/check_patch.py` paso 4 — el MISMO proceso que busca parches nuevos (cron 2×/día
> en `patch-watch.yml`, o manual: `python3 wrlab.py winrates`).
> **Los callouts "Estado Meta Actual" de los reportes se toman de aquí** (TEMPLATE §A.1);
> alerta del vigía si un campeón se mueve ≥ 2 pts de win rate.

| Campeón | Rol | Tier | Win % | Pick % | Ban % | Tendencia | Confianza |
|---|---|---|---|---|---|---|---|
| Ahri | MID | A | 51.11 | 4.21 | 0.13 | ↑ 5 | Confidence Med |
| Caitlyn | DUO | A | 49.68 | 19.08 | 7.65 | ↓ 1 | Confidence High |
| Cho'Gath | SOLO | S+ | 50.67 | 10.74 | 35.42 | ↑ 3 | Confidence High |
| Cho'Gath | JUNGLE | S+ | 50.91 | 8.67 | 35.42 | ↑ 3 | Confidence High |
| Diana | MID | B | 47.10 | 1.07 | 0.15 | ↓ 1 | Confidence Low |
| Diana | JUNGLE | A | 50.24 | 1.46 | 0.15 | ↓ 4 | Confidence Low |
| Heimerdinger | MID | A | 49.82 | 1.68 | 1.30 | ↑ 7 | Confidence Low |
| Jinx | DUO | A | 50.62 | 12.50 | 0.44 | 0 | Confidence High |
| Kalista | DUO | S | 50.93 | 6.19 | 7.30 | ↑ 2 | Confidence Med |
| Kalista | SOLO | S+ | 53.31 | 2.48 | 7.30 | 0 | Confidence Low |
| Karma | SUPPORT | A | 49.85 | 4.39 | 0.34 | ↑ 3 | Confidence Med |
| Malphite | SUPPORT | S+ | 51.61 | 8.10 | 41.49 | ↑ 1 | Confidence High |
| Malphite | SOLO | S+ | 55.10 | 7.04 | 41.49 | 0 | Confidence Med |
| Mordekaiser | SOLO | A | 50.46 | 11.73 | 29.90 | ↓ 7 | Confidence High |
| Nocturne | JUNGLE | S+ | 55.78 | 10.23 | 55.41 | ↓ 1 | Confidence High |
| Norra | MID | A | 50.50 | 1.43 | 7.25 | 0 | Confidence Low |
| Orianna | MID | S | 51.64 | 4.45 | 0.30 | ↑ 7 | Confidence Med |
| Ornn | SOLO | A | 51.48 | 1.91 | 0.16 | 0 | Confidence Low |
| Ornn | SUPPORT | A | 49.84 | 1.16 | 0.16 | ↑ 4 | Confidence Low |
| Rammus | JUNGLE | S+ | 56.97 | 4.46 | 6.44 | 0 | Confidence Med |
| Senna | DUO | S+ | 55.51 | 3.20 | 32.49 | 0 | Confidence Med |
| Senna | SUPPORT | S+ | 54.11 | 12.82 | 32.49 | 0 | Confidence High |
| Seraphine | SUPPORT | B | 48.73 | 6.27 | 1.05 | ↓ 4 | Confidence Med |
| Shyvana | JUNGLE | B | 45.68 | 3.45 | 1.16 | 0 | Confidence Med |
| Sivir | DUO | A | 48.77 | 3.34 | 0.06 | ↑ 2 | Confidence Med |
| Syndra | MID | S | 51.38 | 6.08 | 19.13 | 0 | Confidence Med |
| Volibear | SOLO | A | 47.98 | 4.76 | 4.34 | ↑ 1 | Confidence Med |
| Volibear | JUNGLE | B | 48.02 | 2.44 | 4.34 | ↓ 1 | Confidence Low |
| Xayah | DUO | A | 50.24 | 4.37 | 0.17 | ↑ 3 | Confidence Med |
| Yunara | DUO | S+ | 51.56 | 15.54 | 23.50 | 0 | Confidence High |
| Yuumi | SUPPORT | A | 49.02 | 9.24 | 33.06 | ↑ 3 | Confidence High |

Roles wr-meta: SOLO = top (Baron Lane) · JUNGLE · MID · DUO = ADC (Dragon Lane) · SUPPORT.
Máquina: `champion_winrates.csv` (mismas filas) · BD: tabla `winrates` (`build_db.py`).
Dato de CONTEXTO meta (secundario): no cambia builds por sí solo — si un movimiento
coincide con un hotfix, el flujo es el de FRAMEWORK §E (triage/annotate).
