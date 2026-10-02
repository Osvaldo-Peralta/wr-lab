# MIGRACIÓN · FASE 0 — Informe de estado (entregable)

**Fecha:** 01/10/2026 · **Plan:** `deploy/PLAN_MIGRACION_VERCEL.md` v1.0 (autor) · **Riesgo de esta fase:** nulo (solo lectura)

## 1. WR-LAB (motor de análisis) — ✅ congelable, verde

| Verificación | Resultado |
|---|---|
| Suite oficial | **124/124 OK** (`python3 -m unittest discover -s tests`) |
| `wrlab.py estado` | ✅ TODO EN ORDEN (reportes sin drift + bundles al día + lint) |
| `update_reports.py check` | ✅ 16 reportes verificados contra 7.3a |
| Bundles | lite 220 KB / completo 955 KB, `--check` ✅ |
| Vigía + win rates | cron 2×/día operativo en GitHub Actions (commits del bot al 01/10) |
| Datos | parche 7.3 + hotfix 7.3a **verificado contra nota EN oficial** |

**El lab NO se toca durante la migración** (principio 2 del plan). Lo único que aporta:
este informe, el contrato de datos (Fase 1) y el backfill de frontmatter.

## 2. Inventario de contenido y matriz de divergencia (hallazgo clave de Fase 0)

Existen DOS copias de las guías: `wr-lab/reportes/` (lab) y `GuiasWildRift/content/` (vault/sitio).
Auditoría del 01/10 (repo del vault público, clonado a depth 1):

| Guía | Lab | Vault | Divergencia | Decisión propuesta |
|---|---|---|---|---|
| Jinx | v1.4 ⏩7.3a | v1.4 | **idénticos** | ninguna |
| Caitlyn | v1.2 Beta, datos 7.3 (❌ REGENERAR) | **v1.3, patch 7.3a** (421 líneas de diff) | vault adelante | **ingerir la del vault al lab** |
| Seraphine | vieja (build no extraíble) | **"Modo Agresiva" v1.2, patch 7.3a** (547 líneas) | vault adelante | **ingerir la del vault al lab** |
| Volibear Pesadilla / Volibear | "Pesadilla" v1.2 (7.3) | **Volibear.md v1.1 (7.3a)** — ¿otra guía o reemplazo? | ambiguo | **decide el autor**: ¿coexisten como variantes o la nueva reemplaza a Pesadilla? |
| Shyvana | no existe | stub "PROXIMAMENTE" | solo vault | ¿ingerir el stub (Status: Proximamente) o ignorar hasta que exista? **decide el autor** |
| Otras 12 | con bloque WRLAB-VERIF + registro/lint | sin bloque, **con `patch:` en frontmatter** | ~10-17 líneas | lab adelante en verificación; vault adelante en frontmatter → el backfill del lab + la ingesta de bloques lo convergen |

**Regla de reconciliación propuesta (contrato §7):** para cada guía gana la versión de
mayor `version`/`patch` declarado; a igual versión, gana la que tenga verificación del lab.
Tras reconciliar: **`wr-lab/reportes/` = fuente canónica** y el vault/sitio recibe copias
(lab produce → frontend consume).

## 3. Auditoría del frontmatter actual (16 reportes del lab)

| Campo | Cobertura | Origen para backfill (Fase 1) |
|---|---|---|
| `tags`, `version`, `Status` | 16/16 | ya existen (no se tocan) |
| `patch` | 1/16 (Jinx) | línea `**Parche:**` (token máximo, p.ej. "7.3+7.3a"→7.3a) |
| `champion` | 0/16 | nombre de archivo vía roster+alias (misma lógica de `update_reports`) |
| `slug` | 0/16 | kebab-case ASCII del nombre de archivo |
| `role` | 0/16 (9/16 tienen línea `**Rol principal:**`) | línea Rol → token canónico (adc/support/jungla/mid/top); fallback tags/archivo |
| `archetype` | 0/16 (10/16 tienen línea `**Arquetipo:**`) | texto de la línea (libre) |
| `engine` | 0/16 | `reportes_registry.json` (autos/onhit/rotacion/aliado/none) |
| `published_at` | 0/16 (todos tienen `**Fecha del análisis:**`) | fecha parseada (dd/mm/aaaa o dd-mmm) |

Backfill: `model/backfill_frontmatter.py` (solo añade claves ausentes, nunca modifica
existentes ni el cuerpo; idempotente; dry-run por defecto).

## 4. Auditoría del sitio actual (Quartz 5 + GitHub Pages)

- **Repo:** `Osvaldo-Peralta/GuiasWildRift` (público) — Quartz 5 completo: `quartz/components/`
  (Body, Header, PageList, ConditionalRender, Date, frames/pages/scripts), `quartz/plugins/`,
  `quartz/styles/` (base, callouts, **custom.scss** ← punto de inyección del tema, syntax, variables).
- **`quartz.config.yaml`:** `baseUrl` correcto ✓ · SPA y popovers activos · `locale: en-US`
  (cambiar a `es` cuando toque) · **`analytics: plausible` sin dominio válido** (ruido inocuo —
  poner `analytics: null` hasta la Fase 7 del plan, que trae Vercel Analytics).
- **Tema actual:** fuentes Google (Schibsted Grotesk / Source Sans Pro / IBM Plex Mono) +
  paleta light/dark completa en YAML. El tema minimalista del lab
  (`deploy/quartz-theme/wrlab-minimal.css`) es compatible: se puede aplicar como
  `custom.scss` o mapear su paleta (oro `#c8aa6e`, papel `#fdfcfa`) a las claves YAML.

### Componentes Quartz reutilizables conceptualmente en Next.js (Fase 0, tarea 4)

| De Quartz | Equivalente Next.js | Esfuerzo |
|---|---|---|
| `variables.scss` + paleta YAML | CSS vars / tailwind config (el tema minimalista ya son vars) | bajo |
| `callouts.scss` + plugin callouts | plugin remark/rehype de callouts + mismo CSS | bajo |
| Tablas/`base.scss` | CSS global (idéntico — reportes tabla-intensivos) | bajo |
| `PageList` (índice de guías) | componente de listado leyendo frontmatter | bajo |
| `contentIndex` + búsqueda Ctrl+K | índice JSON estático + Fuse (client-side) | medio |
| Explorer (árbol) | nav por rol/campeón desde frontmatter (mejor que árbol de archivos) | medio |
| Graph view / backlinks | **sin equivalente trivial** — decidir si se conserva (librería de grafos) o se sacrifica | alto |
| RSS / sitemap | route handlers de Next | bajo |
| SPA/routing | App Router nativo | nulo (mejor) |

## 5. Recomendaciones que salen de Fase 0

1. **Reconciliar contenido ANTES de definir el sync** (matriz §2): 2 decisiones del autor
   (Volibear, Shyvana) + ingesta de Caitlyn/Seraphine al lab con su ciclo completo
   (lint → triage → annotate → baseline → bundles).
2. **Backfill de frontmatter** en el lab (Fase 1) y espejo en el vault al reconciliar.
3. `analytics: null` en Quartz hasta la Fase 7 (quita el data-domain inválido de Plausible).
4. Decidir slugs canónicos: se propone kebab-case del archivo (`chogath-titan-del-baron`,
   `diana-mid`); **`Yunana.md` → renombrar a `Yunara.md`** (errata confirmada) en ambos repos.
5. El sync lab→frontend (mecanismo) queda definido en el contrato §6: GitHub Action en
   `wr-lab` que publica `reportes/` + `guias_index.json` en `wr-guides-web/content/`.
