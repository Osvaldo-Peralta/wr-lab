# RECONSTRUCCIÓN · VERIFICACIÓN · v1.11 — WR-LAB

**Actualizado:** 01/10/2026 · **Repo oficial:** https://github.com/Osvaldo-Peralta/wr-lab
**Base:** bundle estable `WR-LAB_completo.md` v1.10 (30/09/2026, sha256(cuerpo)=957395e591f84ab9)

## Fase 1 — Reconstrucción desde el bundle (01/10)

Se extrajeron las 63 fuentes embebidas en las §§1–18 del bundle y se regeneraron los
artefactos derivados. Prueba de fidelidad: un `build_bundles.py` reescrito reprodujo el
bundle **byte a byte**; `update_reports.py annotate --fecha 29/09/2026` resultó
**idempotente** (15 bloques `WRLAB-VERIF` regenerados idénticos; Jinx ⏩ AL_DIA).

## Fase 2 — Verificación contra el repositorio

| Verificación | Resultado |
|---|---|
| Bundle adjunto vs `WR-LAB_completo.md` del repo en `46f9c4d` (v1.10) | ✅ idénticos (sha256 `e8be158a…6342b`) |
| Árbol reconstruido vs exportación prístina de `46f9c4d` | ✅ idéntico byte a byte (tras adoptar nombres/generador/README/deploy/raw oficiales) |
| Suite del repo | ✅ 107/107 OK (el "107" del ROADMAP incluía `test_sim_timings.py`, que el bundle §17 no embebe) |

## Fase 3 — Emparejamiento con `origin/main` (01/10)

Tras el fix del autor `71e1ef4` ("Corrección a commit erróneo… Seraphine"): el lab local
quedó **idéntico a `origin/main`** (Seraphine revertida a v1.10, 15 bloques WRLAB-VERIF
re-sellados al 30/09, bundle/registro/BD regenerados). Verificado: 107/107 tests,
`build_bundles --check` ✅, `update_reports check` ✅, `wrlab.py estado` ✅.
Tag local `v1.10` reapuntado al commit oficial `46f9c4d`.

## v1.11 — Win rates en el mismo proceso del vigía (petición del autor)

**Requisito:** "es indispensable que el laboratorio pueda actualizar la win rate de los
campeones en el mismo proceso en el que busca cambios de la versión/parche, para tener
este dato vital siempre actualizado (fundamental para los reportes)".

**Implementación (todo en el ciclo existente del vigía):**

- `model/check_patch.py` **paso 4** (junto a los pasos 1-3 de parches): descarga el bloque
  *Meta Overview* (`wrCnFsSnapWrap`, bucket **Diamond+**) de wr-meta para el **roster**
  (17 campeones = 16 reportes + 13 specs, ampliado automáticamente por
  `reportes_registry.json`), por rol (SOLO/JUNGLE/MID/DUO/SUPPORT).
- Salidas (fuente de verdad en texto plano, como todo el lab):
  `data/estructurada/champion_winrates.csv` (CRLF, como los demás CSV) +
  `champion_winrates.md` (legible, viaja en los bundles como **§7b**, en LITE y COMPLETO).
  Escritura **idempotente**: solo se reescriben si cambian los VALORES (sin commits parásitos).
- **Alerta:** \|Δ win rate\| ≥ **2 pts** vs el estado previo → finding del vigía (exit 1 +
  step summary en `patch-watch.yml`, que ahora commitea CSV/MD/estado).
- **Descubrimiento de ids:** `WRMETA_IDS` sembrado (FUENTES + verificación en vivo) y
  completado vía `sitemap.xml`; lo descubierto se persiste en `.watch_state.json`.
- **Consumo en reportes:** TEMPLATE §A.1 — el callout "Estado Meta Actual" se cita desde el
  CSV, no de memoria; `lint_reportes.py` añade AVISO (no error) si lo publicado diverge
  **>3 pts** del dato actual. `build_db.py` carga la tabla `winrates` (22 filas hoy).
- **Acceso:** automático (cron 2×/día en `patch-watch.yml`) · `python3 wrlab.py winrates`
  (manual, solo paso 4) · `python3 wrlab.py watch` (ciclo completo) · menú 📊 ESTADO.
- **Tests:** `tests/test_winrates.py` (17, offline: fixture sintético + snapshot commiteado
  de Cho'Gath, red simulada con monkeypatch, drift, idempotencia, lint, §7b, CLI).
  Suite total: **124 OK**.
- **Siembra en vivo (01/10/2026):** 17 campeones · 22 filas · "Updated: 01 OCT 2026 UTC
  00:00" — coherente con los callouts publicados (Δ < 1 pt en los 9 reportes con "Win Rate").
- Docs: FRAMEWORK §E (nota v1.11 + paso 2b), FUENTES (registro, fuente secundaria,
  diagrama de derivación), ROADMAP (v1.11 + fila "Win rates del roster" + matiz al vigía),
  README (mapa, tabla, changelog v1.11).

**Filosofía respetada:** el vigía NO actualiza solo datos de *balance* (eso sigue el
protocolo FRAMEWORK §E con criterio humano); las win rates son dato de *contexto* de
fuente única y formato estable → sí se escriben en el ciclo, y un movimiento ≥ 2 pts
avisa para re-verificar callouts (no re-deriva builds: Regla de Oro v1.6 intacta).

## Estado del lab

```bash
python3 -m unittest discover -s tests   # 124 tests OK (offline)
python3 model/build_bundles.py --check  # ✅ LITE 217 763 B · COMPLETO 950 475 B (01/10/2026)
python3 model/update_reports.py check   # ✅ 16 reportes sin drift, verificados vs 7.3a
python3 wrlab.py estado                 # ✅ TODO EN ORDEN
python3 wrlab.py winrates               # refresco manual de win rates (red)
```

**Parche vigente:** 7.3 + hotfix 7.3a (29-sep-2026). Sin páginas 7.3b/7.4 al 29-sep-2026.
Pendiente para el autor: `git push` (el sandbox no tiene credenciales) — el commit local
`v1.11` queda listo sobre `origin/main`.
