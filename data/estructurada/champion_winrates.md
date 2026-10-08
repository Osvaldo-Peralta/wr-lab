# Win rates del roster — wr-meta (Meta Overview)

> Bucket: **Diamond +** · Datos wr-meta: **Updated 08 OCT 2026 UTC 00:00** · Refrescado por el vigía: 08/10/2026
> Fuente: `wr-meta.com/{id}-{champ}.html` (bloque Meta Overview) vía
> `model/check_patch.py` paso 4 — el MISMO proceso que busca parches nuevos (cron 2×/día
> en `patch-watch.yml`, o manual: `python3 wrlab.py winrates`).
> **Los callouts "Estado Meta Actual" de los reportes se toman de aquí** (TEMPLATE §A.1);
> alerta del vigía si un campeón se mueve ≥ 2 pts de win rate.

| Campeón | Rol | Tier | Win % | Pick % | Ban % | Tendencia | Confianza |
|---|---|---|---|---|---|---|---|
| Ahri | MID | A | 50.62 | 4.33 | 0.13 | ↓ 3 | Confidence Med |
| Caitlyn | DUO | A | 49.64 | 20.51 | 11.62 | ↑ 1 | Confidence High |
| Cho'Gath | SOLO | A | 50.12 | 11.17 | 35.16 | ↓ 5 | Confidence High |
| Cho'Gath | JUNGLE | S | 50.90 | 8.35 | 35.16 | ↑ 1 | Confidence High |
| Diana | MID | B | 46.81 | 1.11 | 0.18 | ↓ 1 | Confidence Low |
| Diana | JUNGLE | B | 49.49 | 1.59 | 0.18 | ↓ 6 | Confidence Low |
| Heimerdinger | MID | A | 50.45 | 1.66 | 1.17 | ↑ 3 | Confidence Low |
| Jinx | DUO | S | 50.83 | 12.17 | 0.43 | ↑ 2 | Confidence High |
| Kalista | DUO | A | 50.49 | 5.69 | 5.90 | ↓ 1 | Confidence Med |
| Kalista | SOLO | S+ | 53.07 | 2.27 | 5.90 | 0 | Confidence Low |
| Karma | SUPPORT | A | 49.10 | 4.91 | 0.36 | ↓ 9 | Confidence Med |
| Malphite | SUPPORT | S | 51.12 | 7.34 | 43.97 | ↓ 3 | Confidence Med |
| Malphite | SOLO | S+ | 55.42 | 7.40 | 43.97 | 0 | Confidence Med |
| Mordekaiser | SOLO | S+ | 51.44 | 10.65 | 28.60 | ↑ 1 | Confidence High |
| Nocturne | JUNGLE | S+ | 55.09 | 9.62 | 45.92 | 0 | Confidence High |
| Norra | MID | A | 50.75 | 1.53 | 7.46 | ↓ 4 | Confidence Low |
| Orianna | MID | S | 51.65 | 4.54 | 0.28 | ↑ 1 | Confidence Med |
| Ornn | SOLO | A | 51.68 | 2.11 | 0.17 | ↓ 2 | Confidence Low |
| Ornn | SUPPORT | B | 48.33 | 1.15 | 0.17 | ↓ 6 | Confidence Low |
| Rammus | JUNGLE | S+ | 56.80 | 4.86 | 7.10 | ↑ 1 | Confidence Med |
| Seraphine | SUPPORT | A | 49.26 | 6.60 | 0.97 | 0 | Confidence Med |
| Shyvana | JUNGLE | B | 46.26 | 3.36 | 1.20 | 0 | Confidence Med |
| Sivir | DUO | A | 48.85 | 3.50 | 0.05 | 0 | Confidence Med |
| Syndra | MID | S | 51.14 | 6.64 | 23.19 | ↓ 2 | Confidence Med |
| Volibear | SOLO | A | 48.30 | 5.13 | 4.54 | ↑ 1 | Confidence Med |
| Volibear | JUNGLE | A | 48.65 | 2.32 | 4.54 | ↑ 3 | Confidence Low |
| Xayah | DUO | A | 50.17 | 4.74 | 0.17 | ↑ 2 | Confidence Med |
| Yunara | DUO | S+ | 51.62 | 16.28 | 23.95 | 0 | Confidence High |
| Yuumi | SUPPORT | A | 49.09 | 9.54 | 34.58 | ↑ 2 | Confidence High |

Roles wr-meta: SOLO = top (Baron Lane) · JUNGLE · MID · DUO = ADC (Dragon Lane) · SUPPORT.
Máquina: `champion_winrates.csv` (mismas filas) · BD: tabla `winrates` (`build_db.py`).
Dato de CONTEXTO meta (secundario): no cambia builds por sí solo — si un movimiento
coincide con un hotfix, el flujo es el de FRAMEWORK §E (triage/annotate).
