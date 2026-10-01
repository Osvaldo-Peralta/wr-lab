# RECONSTRUCCIÓN + VERIFICACIÓN DE COMPATIBILIDAD — WR-LAB v1.10

**Fecha:** 01/10/2026 · **Entrada:** `WR-LAB_completo.md` (bundle estable v1.10, generado 30/09/2026,
sha256(cuerpo)=957395e591f84ab9) · **Repo oficial:** https://github.com/Osvaldo-Peralta/wr-lab

## Fase 1 — Reconstrucción desde el bundle

Se extrajeron las 63 fuentes embebidas en las §§1–18 del bundle y se regeneraron los
artefactos derivados. Prueba de fidelidad: un `build_bundles.py` reescrito reprodujo el
bundle **byte a byte** (932 571 B, salvo fecha/sha del pie, que el propio tooling normaliza);
`update_reports.py annotate --fecha 29/09/2026` resultó **idempotente** (los 15 bloques
`WRLAB-VERIF` se regeneraron idénticos; Jinx ⏩ AL_DIA).

## Fase 2 — Verificación contra el repositorio (este es el veredicto)

| Verificación | Resultado |
|---|---|
| `WR-LAB_completo.md` del repo (commit `46f9c4d`, "Feat: Laboratorio en su versión 1.10") vs bundle adjunto | ✅ **idénticos byte a byte** (sha256 `e8be158a…6342b` en ambos) |
| Árbol local vs exportación prístina de `46f9c4d` | ✅ **idéntico byte a byte** en los 100+ archivos (única adición: este documento) |
| Suite de regresión del repo | ✅ **107/107 tests OK** (coincide con el "107 tests" del ROADMAP; el bundle §17 solo embebe 7 de los 8 archivos de tests — falta `test_sim_timings.py`, ver "hallazgos") |
| `python3 model/build_bundles.py --check` | ✅ LITE al día (215 170 B) · COMPLETO al día (932 571 B) |
| `python3 model/update_reports.py check` | ✅ 16 reportes sin drift, verificados contra 7.3a |
| `python3 wrlab.py estado` | ✅ TODO EN ORDEN |

**Veredicto: la reconstrucción es 100 % compatible con la versión v1.10 del repositorio**
(commit `46f9c4d`, 30/09/2026). Nota: el repo no tiene tag `v1.10` en GitHub (solo `v1.5`);
la referencia de versión es el commit.

## Diferencias que la Fase 2 corrigió sobre la Fase 1 (documento de transparencia)

La reconstrucción inicial desde el bundle era fiel en contenido pero difería del repo en
detalles que solo el repo podía resolver; se adoptaron las versiones oficiales:

1. **Nombres reales vs inferidos:** `reportes/Cho'Gath - Titán de la Jungla.md` (no
   "Cho'Gath - Jungla.md"), `tests/test_lint_refresh.py` (no test_calidad_reportes.py),
   `tests/test_wrlab.py` (no test_wrlab_cli.py). Los contenidos de mis tests inferidos
   eran idénticos a los reales (verificado con `cmp`); la asignación semántica de
   "Titán del Barón" al reporte Top/Baron Lane fue correcta.
2. **`model/build_bundles.py`:** el generador real reemplazó a mi reescritura. Diferencias
   de fondo: LITE = §§1–10e **sin** ROADMAP ni §15; §8 se **deriva del CSV** en tiempo de
   ensamblado (`csv_a_md`), no del .md; reportes/fichas se unen con `---` en el ensamblado
   (los archivos en disco NO llevan el separador pegado); §3b/3c/… son dinámicos por cada
   `cambios_<patch>.md`.
3. **Archivos que el bundle no transporta y el repo sí tiene:** `README.md`,
   `deploy/GITHUB_PAGES_QUARTZ.md`, `data/raw/` completo (26 archivos: notas oficiales
   7.2/7.3/7.3a en HTML/TXT, wr-meta, `.watch_state.json`, `referencia_estilo_jinx.md`,
   12 fichas HTML incluido malphite), `tests/test_sim_timings.py` (10 tests),
   `requirements.txt` real (comentarios, no vacío), `.gitignore` real (incluye `*.zip`),
   workflows reales de CI y patch-watch.
4. **Finos de bytes:** CSV oficiales con CRLF (el generador los normaliza a LF al embeber
   por universal-newlines), trailing-newline en 7 .md, `reportes_registry.json` y
   `wrlab.db` sellados el 30/09, `_borradores` con fecha 30/09/2026.
5. **`champion_base_stats.json`:** mi regeneración desde las fichas + CSV resultó
   **idéntica byte a byte** a la del repo (no requirió corrección).

## Hallazgos sobre el estado actual del repo (main = `e8d8410`, posterior a v1.10)

- HEAD añadió "Feat: Se actualizo la guia de Seraphine: Modo Agresiva" (01/10/2026):
  reescribe `reportes/Seraphine.md` (555 líneas) **sin regenerar los bundles** →
  el CI de main está en **rojo**: `build_bundles.py --check` reporta
  `❌ COMPLETO: WR-LAB_completo.md DESFASADO` (LITE sí al día, no incluye reportes).
  `update_reports.py check` sigue en ✅ (Seraphine no tiene hook cuantitativo).
  Arreglo: `python3 model/build_bundles.py && python3 -m unittest discover -s tests` y commit
  (o `python3 wrlab.py hotfix`/menú 📦). **Este lab local está alineado a v1.10, no a HEAD.**
- El bundle §17 se anuncia como "suite completa" pero la lista TESTS del generador omite
  `test_sim_timings.py` (10 tests): un bundle externo no transporta esa suite.
- Los commits `chore: patch-watch state` (4c630a2, b839269) posteriores a v1.10 solo tocan
  `data/raw/.watch_state.json`.

## Cómo usar este lab

```bash
python3 wrlab.py                     # menú interactivo
python3 wrlab.py estado              # salud: check reportes + bundles + lint
python3 -m unittest discover -s tests    # 107 tests
git remote -v                        # origin → github.com/Osvaldo-Peralta/wr-lab
```

**Parche vigente:** 7.3 + hotfix 7.3a (29-sep-2026). Sin páginas 7.3b/7.4 al 29-sep-2026.
