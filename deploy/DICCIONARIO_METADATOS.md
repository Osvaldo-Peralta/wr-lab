# DICCIONARIO DE METADATOS DE REPORTES (frontmatter) — estándar v1.15

**Propósito:** que añadir/quitar campos nunca dependa de memoria tribal. Cada campo tiene
dueño (quién lo escribe) y consumidor (para qué existe). Si agregas o eliminas un campo:
actualiza ESTE archivo + `deploy/CONTRATO_MARKDOWN_FRONTEND.md` §1 +
`model/estandarizar_metadatos.py` (CANON) + `model/backfill_frontmatter.py` (derivación)
+ tests (`tests/test_metadatos.py`).

**Orden canónico** (el que impone `estandarizar_metadatos.py`):
`tags · version · Status · champion · slug · role · variant · patch · archetype · engine ·
custom · generate · mode · published_at · updated_at · verification · verified_patch`

**Herramientas:** `python3 model/estandarizar_metadatos.py --apply` (normaliza todos los
reportes; idempotente; nunca toca el cuerpo) · `python3 model/lint_reportes.py` (audita).

| Campo | Tipo / valores | Para qué sirve |Quién lo escribe | Lo consume |
|---|---|---|---|---|
| `tags` | lista libre (`ADC`, `Soporte`, `Personalizado`…) | Filtros rápidos en sitio/Obsidian; `Personalizado`/`Custom` activa `custom` | autor | sitio (índices), backfill (deriva custom) |
| `version` | semver del reporte (`1.5`) | Historial de la guía; la reconciliación lab↔vault usa "gana mayor version/patch" | autor / generador (0.9) | reconciliación, sitio |
| `Status` | `Aprobado` · `Beta` · `Espera de verificación` · `Borrador` · `Proximamente` | **Publicabilidad**: Aprobado y Beta se publican (Beta con badge); los otros NO | autor / `aprobar` | sitio, lint, contrato §1 |
| `champion` | nombre canónico (`Yunara`, no la errata del archivo) | Agrupar guías por campeón; triage contra diffs de parche | backfill/estandarizador (del archivo+roster) | update_reports, sitio, BD |
| `slug` | kebab-case ASCII único (`chogath-titan-del-baron`) | Rutas del sitio `/guias/{slug}`; claves de likes/vistas futuras | estandarizador (del archivo) | frontend (contrato §1) |
| `role` | `adc` · `support` · `jungla` · `mid` · `top` | Curvas de oro (sim_timings), notas sistémicas del triage, navegación del sitio | estandarizador (de **Rol principal:**/tags/archivo) | update_reports, sim_timings, sitio |
| `variant` | texto (`mid`, `jungla`, `pesadilla`, `titan-del-baron`) | Distinguir guías del MISMO campeón (N guías paralelas) | estandarizador (sufijo del archivo) | sitio (agrupación campeón→variantes) |
| `patch` | token máximo (`"7.3a"`) | **Qué datos cubre la guía**: si ≥ último hotfix → ⏩ AL_DIA (no se tria ni se anota) | autor / estandarizador (de **Parche:**) | update_reports (AL_DIA), sitio (badge de vigencia) |
| `archetype` | texto libre breve | Contexto del lector y filtros ("Crítico AoE", "Enchanter-attach") | estandarizador (de **Arquetipo:** / spec) | sitio |
| `engine` | `autos` · `onhit` · `rotacion` · `aliado` · `none` | Qué motor del lab valida sus números (`none` = cualitativo/sin motor) | estandarizador (del registro) | update_reports (hooks), sitio (badge "validado por motor X") |
| `custom` | `true`/`false` | Marca guías de personalización (p.ej. "support de daño") vs estándar | estandarizador (tags Custom/Personalizado) | sitio (badge), reconciliación |
| `generate` | `manual` · `auto` | Procedencia: autoría humana/chat vs generador del lab | generador (`auto`) / default `manual` | sitio (transparencia), auditoría |
| `mode` | `sr` · `aram` (reservado) | Modo de juego — el módulo ARAM AAA usará `aram` (contrato §9) | estandarizador (default `sr`) | sitio (secciones por modo) |
| `published_at` | ISO `"2026-09-27"` | Fecha del análisis original | estandarizador (de **Fecha del análisis:**) | sitio (orden/antigüedad) |
| `updated_at` | ISO | Última vez que el lab verificó/actualizó la guía | estandarizador (del registro) | sitio ("actualizada hace…") |
| `verification` | `AL_DIA` · `ANOTAR` · `SIN_IMPACTO` · `REVISAR` · `REGENERAR` · `pending` | Veredicto del último triage contra el hotfix vigente | estandarizador (del registro) | sitio (badge ✅/⚠️/❌), decisiones editoriales |
| `verified_patch` | token (`"7.3a"`) | Contra qué parche fue esa verificación | estandarizador (del registro) | sitio (badge), auditoría |

## Campos retirados / normalizados

- `rol:` (minúscula, usado por el vault en Jinx v1.5) → **normalizado a `role:`** por el
  estandarizador. No volver a introducirlo.
- No existe `build:` en frontmatter: la build publicada vive en la Tabla A (fuente de verdad
  legible); el lab la deriva con `update_reports.extraer_build` al baselinar. Duplicarla en
  metadatos crearía dos fuentes — prohibido.

## Regla de oro del esquema

Los metadatos **organizan e identifican** (rutas, filtros, badges, vigencia) — nunca contienen
datos de análisis (builds, números, runas): eso vive en el cuerpo del reporte y en el registro
derivado del lab. Si un campo nuevo no cumple esa función, no entra.
