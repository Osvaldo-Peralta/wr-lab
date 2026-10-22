# Win rates del roster — wr-meta (Meta Overview)

> Bucket: **Diamond +** · Datos wr-meta: **Updated 22 OCT 2026 UTC 00:00** · Refrescado por el vigía: 22/10/2026
> Fuente: `wr-meta.com/{id}-{champ}.html` (bloque Meta Overview) vía
> `model/check_patch.py` paso 4 — el MISMO proceso que busca parches nuevos (cron 2×/día
> en `patch-watch.yml`, o manual: `python3 wrlab.py winrates`).
> **Los callouts "Estado Meta Actual" de los reportes se toman de aquí** (TEMPLATE §A.1);
> alerta del vigía si un campeón se mueve ≥ 2 pts de win rate.

| Campeón | Rol | Tier | Win % | Pick % | Ban % | Tendencia | Confianza |
|---|---|---|---|---|---|---|---|
| Ahri | MID | A | 51.25 | 4.44 | 0.16 | ↑ 1 | Confidence Med |
| Caitlyn | DUO | A | 49.85 | 15.98 | 5.16 | 0 | Confidence High |
| Cho'Gath | SOLO | S | 50.68 | 9.41 | 36.37 | ↓ 1 | Confidence High |
| Cho'Gath | JUNGLE | S | 50.36 | 8.45 | 36.37 | ↓ 1 | Confidence High |
| Diana | MID | B | 47.47 | 1.07 | 0.15 | ↑ 1 | Confidence Low |
| Diana | JUNGLE | A | 51.11 | 1.35 | 0.15 | ↑ 6 | Confidence Low |
| Heimerdinger | MID | A | 49.85 | 1.72 | 1.43 | ↓ 1 | Confidence Low |
| Jinx | DUO | A | 50.65 | 12.73 | 0.53 | 0 | Confidence High |
| Kalista | DUO | S | 50.57 | 7.79 | 9.76 | ↑ 1 | Confidence Med |
| Kalista | SOLO | S+ | 54.20 | 2.68 | 9.76 | 0 | Confidence Low |
| Karma | SUPPORT | A | 50.18 | 4.83 | 0.41 | ↑ 5 | Confidence Med |
| Malphite | SUPPORT | S+ | 51.81 | 9.38 | 42.07 | 0 | Confidence High |
| Malphite | SOLO | S+ | 54.84 | 7.46 | 42.07 | 0 | Confidence Med |
| Mordekaiser | SOLO | S | 51.21 | 11.28 | 32.12 | ↓ 4 | Confidence High |
| Nocturne | JUNGLE | S+ | 52.47 | 6.99 | 58.94 | ↑ 1 | Confidence Med |
| Norra | MID | A | 49.72 | 1.39 | 6.84 | ↓ 10 | Confidence Low |
| Orianna | MID | S | 52.04 | 4.46 | 0.32 | ↑ 3 | Confidence Med |
| Ornn | SOLO | B | 49.57 | 1.82 | 0.19 | ↓ 7 | Confidence Low |
| Ornn | SUPPORT | A | 50.07 | 1.32 | 0.19 | 0 | Confidence Low |
| Rammus | JUNGLE | S+ | 56.10 | 4.20 | 7.03 | ↑ 1 | Confidence Med |
| Senna | SUPPORT | A | 49.78 | 7.22 | 15.47 | ↓ 4 | Confidence Med |
| Seraphine | SUPPORT | A | 49.93 | 6.26 | 1.11 | ↑ 1 | Confidence Med |
| Shyvana | JUNGLE | B | 46.64 | 3.08 | 1.02 | ↑ 2 | Confidence Med |
| Sivir | DUO | A | 50.04 | 3.88 | 0.06 | ↑ 5 | Confidence Med |
| Syndra | MID | S | 51.36 | 5.94 | 18.45 | ↓ 2 | Confidence Med |
| Volibear | SOLO | A | 47.83 | 9.25 | 8.17 | ↓ 1 | Confidence High |
| Volibear | JUNGLE | A | 48.68 | 4.92 | 8.17 | ↓ 3 | Confidence Med |
| Xayah | DUO | A | 51.12 | 4.92 | 0.22 | ↓ 1 | Confidence Med |
| Yunara | DUO | A | 49.51 | 6.42 | 13.92 | ↓ 1 | Confidence Med |
| Yuumi | SUPPORT | A | 47.60 | 8.44 | 33.76 | 0 | Confidence High |

Roles wr-meta: SOLO = top (Baron Lane) · JUNGLE · MID · DUO = ADC (Dragon Lane) · SUPPORT.
Máquina: `champion_winrates.csv` (mismas filas) · BD: tabla `winrates` (`build_db.py`).
Dato de CONTEXTO meta (secundario): no cambia builds por sí solo — si un movimiento
coincide con un hotfix, el flujo es el de FRAMEWORK §E (triage/annotate).
