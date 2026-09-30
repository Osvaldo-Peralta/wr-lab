# ROADMAP — WR-LAB como proyecto de software

**Estado actual (v1.10):** repo git versionado · BD SQLite derivada · 107 tests · CI (tests + BD + bundles + reportes verificados) + vigilante de parches · actualizador de reportes · optimizador de builds · bundles regenerables · datos 7.3+7.3a.

## Ya disponible

| Capacidad | Dónde | Estado |
|---|---|---|
| Control de versiones | git local (tags por versión del lab) | ✅ listo para `git remote add origin … && git push` |
| Base de datos | `data/wrlab.db` (SQLite) vía `model/build_db.py` | ✅ se reconstruye desde los .md/.csv en segundos |
| Tests de regresión | `tests/test_model.py` (unittest, sin dependencias) | ✅ golden numbers de Jinx + slots + fórmula AS + overrides 7.3a |
| **Actualizador de reportes publicados** | `model/update_reports.py` + `data/estructurada/reportes_registry.json` + `tests/test_update_reports.py` | ✅ triage/annotate/check: un hotfix **anota** los reportes con su Δ medido (umbrales 2 %/5 %) en vez de regenerarlos; bloques `WRLAB-VERIF` idempotentes; CI detecta drift y reportes sin triar. Parser v2: reportes del vault sin frontmatter champion, tablas BUILD FINAL, alias en paréntesis, veredicto ⏩ AL_DIA |
| **Optimizador de builds** | `model/optimize_build.py` + `tests/test_optimize_build.py` | ✅ búsqueda exhaustiva (DFS podado por oro/AS/crit) sobre el motor dps_model: top-N por objetivo ponderado **normalizado** por escenario; `--crit-min/--pen-min` (Leyes 1/3 duras), `--incluir/--excluir`, `--oro`, `--validar` (validación cruzada: **redescubre la build C de Jinx**). Alcance v1: arquetipo de autos; pendiente: motores batch2 (Kalista/Diana/soportes) |
| **Regenerador de bundles** | `model/build_bundles.py` | ✅ lite/completo son artefactos derivados de las fuentes; `--check` en CI evita desfases; validación de integridad embebida (motor íntegro, 140 AS, 186 ítems, 16 reportes con WRLAB-VERIF, 11 fichas) |
| Vigía de parches | `model/check_patch.py` + `.github/workflows/patch-watch.yml` (cron 2×/día) | ✅ detecta: cambios en la página 7.3, aparición de 7.3a/7.4, nuevas entradas de changelog en wr-meta |
| CI | `.github/workflows/ci.yml` (tests + rebuild BD en cada push) | ✅ |
| Motor de DPS + validador | `model/dps_model.py` (`validate_slots`, `eval_build`, `compare`) | ✅ |

## Hallazgos del optimizador (registro vivo)

- **29/09 · Protocolo de validación (2 niveles):** NIVEL 1 — dentro de las candidatas del propio
  reporte (§8), la publicada debe ganar: ✅ Jinx C (búsqueda exhaustiva), ✅ Diana D2-LT, ✅ Yuumi Y1
  (puntuación normalizada). NIVEL 2 — exploración completa: puede superar al reporte; los modelos
  NO puntúan defensa ni pasivas no modeladas (Zhonyas stasis, Echoes siphon, Redemption activo,
  tenacidad de Wit's End) → los hallazgos se documentan aquí, NO se auto-aplican.
- **29/09 · Kalista (motor onhit):** el híbrido `Gunmetal+Runaan+Statikk+Guinsoo+Terminus+BotRK`
  supera a K2 por **0.3 %** (ruido del modelo; K2 conserva valor defensivo no modelado de Wit's End).
  IE excluido del pool on-hit a propósito: kalista() no modela críticos (sub/valora ambos lados).
- **29/09 · Diana/Yuumi (pool completo):** el objetivo puramente ofensivo prefiere glass-cannon
  (Diana: Stormsurge+VoidStaff+Orb +31 % dps vs D2; Yuumi: Censer+Staff+HorizonFocus+Stormsurge
  sobre Y1) — limitación conocida: sin valor defensivo/utilidad activa en el score.
- **29/09 · Jinx post-7.3a:** con el pool completo y Leyes 1+3 duras (18 000 g, nivel 15), la
  frontera óptima se movió tras el buff de Yun Tal (AS 25→35): `Gunmetal+C44+Terminus+YunTal+LDR+IE`
  (pen 65) alcanza ~90 % de eficiencia normalizada vs ~83 % de la build C publicada (que sigue
  siendo la mejor en AoE 3v3 puro). Supuestos a declarar antes de cualquier re-derivación:
  Yun Tal al **máximo de rampa** (125 ataques) y Terminus a stacks completos. **Decisión pendiente
  del autor** (la Regla de Oro v1.6 aplica: el reporte publicado no se toca sin decisión explícita).

## Módulos propuestos (prioridad × esfuerzo)

1. ~~**`wrlab` CLI unificado**~~ ✅ **hecho en v1.9** — CLI + menú interactivo escalable (`wrlab.py`).

2. ~~**Optimizador v2 para motores batch2**~~ ✅ **hecho en v1.8** — 4 motores (autos/onhit/
   rotacion/aliado) con protocolo de validación en 2 niveles (ver §Hallazgos).

3. ~~**Buscador de runas**~~ ✅ **hecho en v1.9** — `optimize_runes.py` (autos + rotación).
   Pendiente v2: motores onhit/aliado (parametrizar LT/Alacrity en kalista()/yuumi()) y
   verificar en juego los supuestos declarados (CD de Electrocute, valores de Brutal).

4. **Sincronizador con el sitio Quartz** (bajo-medio)
   `wrlab sync-vault <ruta-del-vault>`: copia reportes + fichas con frontmatter, genera
   índice `Guias.md`, respeta la nomenclatura del vault y hace commit en ese repo.
   Publicar = `git push` del vault (su workflow de Pages ya funciona).

5. ~~**Simulador de timings de oro**~~ ✅ **hecho en v1.10** — `sim_timings.py` (curvas del
   vault). Mejora futura: calibrar con minion gold / passive income verificados en juego
   (hoy las anclas son las estimaciones de los autores — fuente secundaria declarada).

6. **Matriz de matchups** (alto) — EHP/DPS efectivo cruzado entre builds (p.ej. "¿mi Jinx
   full contra un Chainlaced+Randuin?"), usando las tablas de mitigación ya existentes.

7. **Backup externo de la BD** (bajo) — el repo en GitHub YA es el backup (texto + db commiteada);
   opcional: export nocturno de `wrlab.db` a release assets vía Actions.

## Decisiones de arquitectura (por qué así)

- **Texto plano como fuente de verdad, SQLite como índice:** los .md/.csv viajan en los bundles
  portables (cualquier chat/IA los consume sin tooling); la BD da consultas rápidas y es reconstruible.
  Nunca al revés (una BD opaca rompería la portabilidad que ya resolvimos).
- **Sin dependencias de terceros:** todo stdlib (urllib, sqlite3, unittest, csv). Cero `pip install`,
  cero superficie de rotura. `requirements.txt` existe pero está vacío a propósito.
- **Golden tests:** los números canónicos de los reportes están fijados en tests; cualquier cambio de
  datos que los mueva falla en CI y obliga a documentar el porqué (como el override 7.3a de Caitlyn).
- **El vigía no actualiza solo:** detecta y avisa (exit 1 + step summary). La actualización real sigue
  el protocolo FRAMEWORK §E porque requiere criterio (discrepancias, overrides, re-validación).

## Para ponerlo en GitHub (una vez, ~3 minutos)

```bash
# en tu máquina, dentro de la carpeta wr-lab descargada/copiada:
git remote add origin https://github.com/Osvaldo-Peralta/wr-lab.git   # repo nuevo, privado o público
git push -u origin main --tags
# GitHub Actions corre ci.yml en el push y patch-watch.yml 2×/día.
```
