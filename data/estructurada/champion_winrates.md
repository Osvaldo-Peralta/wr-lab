# Win rates del roster — wr-meta (Meta Overview)

> Bucket: **Diamond +** · Datos wr-meta: **Updated 16 OCT 2026 UTC 00:00** · Refrescado por el vigía: 16/10/2026
> Fuente: `wr-meta.com/{id}-{champ}.html` (bloque Meta Overview) vía
> `model/check_patch.py` paso 4 — el MISMO proceso que busca parches nuevos (cron 2×/día
> en `patch-watch.yml`, o manual: `python3 wrlab.py winrates`).
> **Los callouts "Estado Meta Actual" de los reportes se toman de aquí** (TEMPLATE §A.1);
> alerta del vigía si un campeón se mueve ≥ 2 pts de win rate.

| Campeón | Rol | Tier | Win % | Pick % | Ban % | Tendencia | Confianza |
|---|---|---|---|---|---|---|---|
| Ahri | MID | A | 50.95 | 4.28 | 0.12 | ↑ 5 | Confidence Med |
| Caitlyn | DUO | A | 49.71 | 18.50 | 6.96 | ↑ 1 | Confidence High |
| Cho'Gath | SOLO | S | 50.58 | 10.64 | 35.48 | ↓ 4 | Confidence High |
| Cho'Gath | JUNGLE | A | 50.34 | 8.91 | 35.48 | ↓ 2 | Confidence High |
| Diana | MID | B | 47.48 | 1.05 | 0.16 | ↓ 4 | Confidence Low |
| Diana | JUNGLE | B | 49.66 | 1.42 | 0.16 | ↓ 4 | Confidence Low |
| Heimerdinger | MID | A | 50.89 | 1.66 | 1.33 | ↑ 9 | Confidence Low |
| Jinx | DUO | A | 50.63 | 12.52 | 0.45 | 0 | Confidence High |
| Kalista | DUO | A | 50.86 | 6.21 | 7.60 | 0 | Confidence Med |
| Kalista | SOLO | S+ | 53.91 | 2.51 | 7.60 | 0 | Confidence Low |
| Karma | SUPPORT | A | 49.84 | 4.20 | 0.34 | ↓ 1 | Confidence Med |
| Malphite | SUPPORT | S+ | 51.37 | 8.14 | 40.82 | ↑ 1 | Confidence High |
| Malphite | SOLO | S+ | 55.12 | 6.88 | 40.82 | 0 | Confidence Med |
| Malphite | MID | A | 50.27 | 1.01 | 40.82 | ↓ 16 | Confidence Low |
| Mordekaiser | SOLO | S+ | 50.82 | 11.33 | 30.24 | ↑ 2 | Confidence High |
| Nocturne | JUNGLE | S+ | 55.79 | 9.92 | 58.62 | ↓ 1 | Confidence High |
| Norra | MID | S | 50.95 | 1.43 | 6.91 | ↑ 2 | Confidence Low |
| Orianna | MID | A | 50.88 | 4.46 | 0.27 | ↓ 8 | Confidence Med |
| Ornn | SOLO | A | 50.78 | 1.94 | 0.17 | ↓ 7 | Confidence Low |
| Ornn | SUPPORT | A | 50.17 | 1.19 | 0.17 | ↑ 13 | Confidence Low |
| Rammus | JUNGLE | S+ | 57.11 | 4.43 | 6.47 | 0 | Confidence Med |
| Senna | DUO | S+ | 56.46 | 2.99 | 31.68 | 0 | Confidence Low |
| Senna | SUPPORT | S+ | 53.95 | 12.75 | 31.68 | 0 | Confidence High |
| Seraphine | SUPPORT | A | 48.90 | 6.19 | 1.03 | ↓ 7 | Confidence Med |
| Shyvana | JUNGLE | B | 46.13 | 3.56 | 1.09 | ↓ 1 | Confidence Med |
| Sivir | DUO | B | 48.45 | 3.31 | 0.05 | ↓ 2 | Confidence Med |
| Syndra | MID | S+ | 51.26 | 6.07 | 18.35 | ↑ 3 | Confidence Med |
| Volibear | SOLO | B | 47.92 | 4.76 | 4.20 | 0 | Confidence Med |
| Volibear | JUNGLE | B | 47.90 | 2.41 | 4.20 | ↓ 1 | Confidence Low |
| Xayah | DUO | A | 50.43 | 4.44 | 0.17 | ↑ 1 | Confidence Med |
| Yunara | DUO | S+ | 51.79 | 15.26 | 23.37 | 0 | Confidence High |
| Yuumi | SUPPORT | A | 49.00 | 9.06 | 32.98 | ↓ 4 | Confidence High |

Roles wr-meta: SOLO = top (Baron Lane) · JUNGLE · MID · DUO = ADC (Dragon Lane) · SUPPORT.
Máquina: `champion_winrates.csv` (mismas filas) · BD: tabla `winrates` (`build_db.py`).
Dato de CONTEXTO meta (secundario): no cambia builds por sí solo — si un movimiento
coincide con un hotfix, el flujo es el de FRAMEWORK §E (triage/annotate).
