# CONTRATO MARKDOWN ↔ FRONTEND (Fase 1 de la migración)

**Versión:** 1.2 · **Fecha:** 04/10/2026 · **Partes:** `wr-lab` (productor) ↔ `wr-guides-web` (consumidor)
**Principio hexagonal:** el frontend consume ESTE contrato (puerto); nunca conoce el interior del
lab. El lab produce Markdown + un índice JSON; nunca conoce al frontend.

---

> **v1.2:** el esquema completo, con el propósito de cada campo y sus dueños/consumidores,
> vive en `deploy/DICCIONARIO_METADATOS.md` (fuente de verdad del esquema). Aquí queda el
> resumen operativo. Nuevos campos canónicos: `updated_at`, `verification`, `verified_patch`
> (badges de vigencia del sitio) y orden canónico impuesto por `model/estandarizar_metadatos.py`.

## 1. Frontmatter canónico de cada guía (resumen — ver DICCIONARIO_METADATOS.md)

```yaml
---
tags: [ADC]                  # existente — libre, para filtros rápidos
version: "1.4"               # existente — semver del reporte
Status: Aprobado             # existente — Aprobado | Beta | Borrador | Proximamente
champion: Jinx               # BACKFILL — canónico del roster (no del archivo: Yunana.md → Yunara)
slug: jinx                   # BACKFILL — kebab-case ASCII, único; ruta /guias/{slug}
role: adc                    # BACKFILL — adc | support | jungla | mid | top (canónico)
patch: "7.3a"                # BACKFILL — parche máximo que el reporte declara cubrir
archetype: Crítico AoE       # BACKFILL (si el reporte tiene línea **Arquetipo:**) — texto libre
engine: autos                # BACKFILL — autos | onhit | rotacion | aliado | none (validación del lab)
published_at: 2026-09-27     # BACKFILL — de **Fecha del análisis:** (ISO 8601)
custom: false                # BACKFILL (v1.1) — true si tags incluye Custom/Personalizado
updated_at: "2026-10-04"     # v1.2 — última verificación/actualización del lab (ISO)
verification: AL_DIA         # v1.2 — AL_DIA|ANOTAR|SIN_IMPACTO|REVISAR|REGENERAR|pending
verified_patch: "7.3a"       # v1.2 — contra qué parche fue la verificación
variant: pesadilla           # BACKFILL (v1.1) — sufijo del archivo; ausente = guía estándar del campeón
generate: manual             # v1.1 — manual | auto (ausente = manual)
mode: sr                     # v1.1 reservado — sr | aram (módulo ARAM AAA futuro)
---
```

**Vocabulario de `Status` (v1.1):** `Aprobado` (publicable) · `Beta` (publicable con badge) ·
`Espera de verificación` (generado automáticamente — **NO publicable** hasta aprobación del
autor) · `Borrador` (no publicable) · `Proximamente` (anuncio, publicable como placeholder).

**Guías custom (v1.1):** un campeón puede tener N guías paralelas (estándar + personalizadas:
"Volibear Pesadilla", "Seraphine Modo Agresivo", "Yuumi poke-híbrida"…). Identidad = `slug`;
agrupación = `champion`; la naturaleza custom se declara con `custom: true` (tag
Custom/Personalizado) y `variant`. El frontend muestra las custom bajo el campeón con su
badge — la flexibilidad que motivó la migración.

Reglas:
- **Claves nuevas en minúscula; las existentes (`tags/version/Status`) no se renombran** —
  el frontend mapea `Status`→`status`. (Renombrar todo a minúsculas sería breaking para el
  lab: build_db/lint/update_reports leen `Status`.)
- `slug` se deriva del nombre de archivo: minúsculas, sin acentos, `'`→ vacío,
  espacios/`-`→`-`, colapso de guiones. Ejemplos: `Cho'Gath - Titán del Barón.md` →
  `chogath-titan-del-baron`; `Diana - Mid.md` → `diana-mid`; `Volibear Pesadilla.md` →
  `volibear-pesadilla`.
- **Un campeón puede tener varias guías** (Diana jungla/mid; Cho'Gath jungla/barón) —
  la identidad es el `slug`, no el `champion`. El frontend agrupa por `champion`.
- `patch: "7.3a"` ⇒ la guía declara cubrir ese hotfix ⇒ el frontend puede mostrar el badge
  "verificada 7.3a" aunque no exista bloque WRLAB-VERIF (semántica ⏩ AL_DIA del lab).

## 2. Índice derivado: `guias_index.json`

El lab publica (junto a los .md) un índice para listados/rutas sin parsear 18 archivos:

```json
{
  "generado": "2026-10-01",
  "patch_vigente": "7.3a",
  "guias": [
    {"slug": "jinx", "champion": "Jinx", "role": "adc", "patch": "7.3a", "version": "1.4",
     "status": "Aprobado", "engine": "autos", "published_at": "2026-09-27",
     "verificada": "AL_DIA", "win": {"win_pct": 49.47, "pick_pct": 11.61, "ban_pct": 0.41,
     "tier": "A", "actualizado": "2026-10-01", "role_fuente": "DUO"}}
  ]
}
```

- `verificada`: `AL_DIA` | `ANOTAR` | `SIN_IMPACTO` | `REVISAR` | `REGENERAR` | `null`
  (de `reportes_registry.json` → `ultima_verificacion`). El frontend la usa para el badge
  de estado de la guía (✅ verificada / ⚠️ en revisión / ❌ obsoleta).
- `win`: última fila de `champion_winrates.csv` para el campeón+rol (fuente del badge meta).

## 3. Reglas de renderizado del cuerpo (obligatorias para el frontend)

1. **Bloques `<!-- WRLAB-VERIF:{patch}:START … END -->`**: NO son comentarios mudos —
   renderizar como *badge/ficha de verificación* plegable (el contenido entre marcas es un
   blockquote `> [!NOTE]`). Nunca mostrar el HTML crudo ni strippearlo en silencio.
2. **Callouts `> [!NOTE|TIP|WARNING|DANGER]`**: plugin remark/rehype (Quartz ya los usa —
   portar `callouts.scss`).
3. **Tablas**: son la estructura dominante (Tabla A/B, matrices). Respetar alineaciones y
   el estándar de números: espacio de miles (`17 350 g`) y `%` con espacio (`25 %`) —
   no re-formatear números al renderizar.
4. **Secciones**: los reportes siguen TEMPLATE_REPORTE v1.4 (§0-§10 + apéndices + pie).
   El frontend puede generar TOC desde los `##`/`###`; el pie de página (créditos Riot/
   wr-meta/WR-LAB + aviso legal) debe conservarse visible SIEMPRE (requisito legal).
5. **Imágenes**: hoy no hay; si se añaden, rutas relativas a `content/assets/`.

## 4. Win rates en callouts (regla editorial, ya vigente en el lab)

El callout "Estado Meta Actual" cita la última fila de `data/estructurada/champion_winrates.csv`
(champion+rol, con fecha). El frontend puede **sustituir ese callout por datos vivos** de
`guias_index.json.win` (más frescos que el texto). Si lo hace, debe mostrar la fecha
`actualizado` y mantener el aspecto del callout.

## 5. Validación (gate de calidad del productor)

- `python3 model/lint_reportes.py --strict` debe pasar para que una guía se publique
  (frontmatter completo, build extraíble, Ley 0, ítems existentes en la BD oficial).
- Campos del contrato ausentes ⇒ el lab los repone con `model/backfill_frontmatter.py`
  (derivación documentada en Fase 0 §3); si no son derivables ⇒ lint ERROR.

## 6. Mecanismo de sync lab → frontend (propuesta de Fase 0 §5, refrendada aquí)

- **Unidireccional:** GitHub Action en `wr-lab` (trigger: push a main que toque `reportes/`
  o `champion_winrates.csv`) → copia `reportes/*.md` + genera `guias_index.json` →
  commit en `wr-guides-web/content/` (bot con repo-scoped token).
- El frontend NUNCA edita los .md; si hay corrección editorial, se hace en el lab
  (o en un chat externo que entrega el .md al lab — flujo Jinx v1.4).
- Alternativa descartada: submódulo (acopla builds y complica el preview de Vercel).

## 7. Reconciliación previa (una vez, antes de activar el sync)

Estado a 01/10: el vault (`GuiasWildRift/content/`) está ADELANTE en Caitlyn (v1.3/7.3a),
Seraphine ("Modo Agresiva" v1.2/7.3a), Volibear.md (v1.1/7.3a, ¿reemplaza a "Volibear
Pesadilla"?) y Shyvana.md (stub "PROXIMAMENTE"); el lab está adelante en verificación
(WRLAB-VERIF + registro). Regla: **gana mayor version/patch; a igualdad, la verificada**.
Procedimiento: ingerir las ganadoras al lab (ciclo lint→triage→annotate→baseline→bundles),
decidir los 2 casos ambigüos (autor), y entonces `wr-lab/reportes/` pasa a ser canónica.

## 8. Auto-regeneración y aprobación (v1.1)

Flujo para reportes con veredicto ❌ REGENERAR (o campeones sin guía — escalabilidad a
100+ campeones):

1. `python3 model/generate_report.py generar --champion <c> [--rol <r>]` → escribe
   `reportes/_auto/{Champion}_AUTO_{patch}.md` completo (motor + optimizador + runas +
   timings + win rates + TEMPLATE v1.4), con `Status: Espera de verificación`,
   `generate: auto` y TODOs explícitos donde hace falta criterio humano (orden de
   habilidades, plan de juego). El original publicado **no se toca**.
2. El autor compara ambas versiones (diff/lector) y decide:
   · **Aprueba** → `python3 model/generate_report.py aprobar --archivo <_auto/…> [--destino reportes/<Nombre>.md]`
     (mueve, pone `Status: Aprobado`, corre baseline+annotate+lint+check).
   · **No aprueba** → regeneración manual (chat externo con bundle) o correcciones directas;
     el archivo _auto se descarta o se conserva como referencia.
3. Los reportes `_auto/` y `_borradores/` están FUERA del registro, bundles, BD y sitio
   (solo `reportes/*.md` raíz se publica). `borrador` (esqueleto) sigue existiendo como
   fallback para campeones sin motor (tanques/rotaciones no cubiertas — p.ej. Rammus).

Cobertura v1 del generador: campeones con ChampSpec Y motor (autos/onhit/rotacion/aliado).
Fuera de cobertura → mensaje honesto + borrador. Los avisos de aproximación del motor
(p.ej. Shyvana sin Q doble-golpe) se imprimen como `> [!WARNING]` en el propio reporte.

## 9. Fuera del contrato (explícitamente)

- Likes/vistas/usuarios: NO viven en el Markdown (principio 6 del plan — estado en Supabase).
  El frontend asocia métricas por `slug`.
- Build/optimización/validación: responsabilidad exclusiva del lab; el frontend solo muestra.
- ARAM AAA (futuro módulo): cuando exista, sus guías llevarán `mode: aram` en frontmatter
  (extensión reservada desde ya) y slugs `aram/{champion}` — el núcleo SR no se mezcla.
