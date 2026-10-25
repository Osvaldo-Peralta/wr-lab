# Win rates del roster — wr-meta (Meta Overview)

> Bucket: **Diamond +** · Datos wr-meta: **Updated 25 OCT 2026 UTC 00:00** · Refrescado por el vigía: 25/10/2026
> Fuente: `wr-meta.com/{id}-{champ}.html` (bloque Meta Overview) vía
> `model/check_patch.py` paso 4 — el MISMO proceso que busca parches nuevos (cron 2×/día
> en `patch-watch.yml`, o manual: `python3 wrlab.py winrates`).
> **Los callouts "Estado Meta Actual" de los reportes se toman de aquí** (TEMPLATE §A.1);
> alerta del vigía si un campeón se mueve ≥ 2 pts de win rate.

| Campeón | Rol | Tier | Win % | Pick % | Ban % | Tendencia | Confianza |
|---|---|---|---|---|---|---|---|
| Ahri | MID | S | 51.49 | 4.62 | 0.15 | ↑ 4 | Confidence Med |
| Caitlyn | DUO | A | 49.81 | 16.13 | 4.82 | ↓ 1 | Confidence High |
| Cho'Gath | SOLO | S | 50.29 | 9.27 | 36.13 | ↓ 1 | Confidence High |
| Cho'Gath | JUNGLE | A | 50.02 | 8.28 | 36.13 | ↓ 3 | Confidence High |
| Diana | MID | B | 47.07 | 1.03 | 0.15 | 0 | Confidence Low |
| Diana | JUNGLE | A | 50.07 | 1.38 | 0.15 | ↓ 1 | Confidence Low |
| Heimerdinger | MID | A | 49.54 | 1.73 | 1.50 | ↓ 1 | Confidence Low |
| Jinx | DUO | A | 50.78 | 13.03 | 0.55 | 0 | Confidence High |
| Kalista | DUO | S | 50.80 | 7.78 | 10.64 | 0 | Confidence Med |
| Kalista | SOLO | S+ | 53.58 | 2.83 | 10.64 | 0 | Confidence Low |
| Karma | SUPPORT | A | 50.19 | 4.73 | 0.43 | ↑ 4 | Confidence Med |
| Malphite | SUPPORT | S+ | 51.59 | 9.49 | 42.60 | ↓ 1 | Confidence High |
| Malphite | SOLO | S+ | 54.77 | 7.56 | 42.60 | 0 | Confidence Med |
| Malphite | MID | S | 50.30 | 1.00 | 42.60 | 0 | Confidence Low |
| Mordekaiser | SOLO | S | 51.33 | 11.40 | 32.83 | ↓ 1 | Confidence High |
| Nocturne | JUNGLE | S+ | 52.50 | 6.67 | 59.12 | 0 | Confidence Med |
| Norra | MID | A | 50.27 | 1.32 | 6.89 | ↓ 10 | Confidence Low |
| Orianna | MID | S | 51.81 | 4.48 | 0.35 | ↑ 3 | Confidence Med |
| Ornn | SOLO | A | 51.20 | 1.82 | 0.18 | ↑ 3 | Confidence Low |
| Ornn | SUPPORT | A | 49.91 | 1.28 | 0.18 | ↑ 7 | Confidence Low |
| Rammus | JUNGLE | S+ | 55.66 | 4.03 | 6.93 | 0 | Confidence Med |
| Senna | SUPPORT | A | 49.82 | 6.71 | 12.72 | ↓ 2 | Confidence Med |
| Seraphine | SUPPORT | A | 50.03 | 6.29 | 1.11 | ↑ 5 | Confidence Med |
| Shyvana | JUNGLE | B | 46.77 | 3.05 | 0.98 | 0 | Confidence Med |
| Sivir | DUO | A | 49.42 | 4.81 | 0.07 | ↓ 3 | Confidence Med |
| Syndra | MID | S | 51.45 | 5.93 | 18.36 | ↓ 4 | Confidence Med |
| Volibear | SOLO | A | 48.65 | 8.28 | 8.16 | 0 | Confidence High |
| Volibear | JUNGLE | A | 49.15 | 4.46 | 8.16 | ↓ 1 | Confidence Med |
| Xayah | DUO | A | 50.95 | 5.05 | 0.24 | 0 | Confidence Med |
| Yunara | DUO | A | 49.50 | 5.90 | 11.63 | ↑ 2 | Confidence Med |
| Yuumi | SUPPORT | A | 47.98 | 8.37 | 33.62 | 0 | Confidence High |

Roles wr-meta: SOLO = top (Baron Lane) · JUNGLE · MID · DUO = ADC (Dragon Lane) · SUPPORT.
Máquina: `champion_winrates.csv` (mismas filas) · BD: tabla `winrates` (`build_db.py`).
Dato de CONTEXTO meta (secundario): no cambia builds por sí solo — si un movimiento
coincide con un hotfix, el flujo es el de FRAMEWORK §E (triage/annotate).
