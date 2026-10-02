# 🎨 SITIO DE GUÍAS — personalización y estado (v1.12.1 · 01-oct-2026)

| Pieza | Archivo | Estado |
|---|---|---|
| Tema minimalista (Quartz) | `quartz-theme/wrlab-minimal.css` | ✅ listo para copiar al vault |
| Plan de migración del sitio (autor) | `PLAN_MIGRACION_VERCEL.md` | 📋 v1.0 del autor — fases 0-1 son del lado del lab |
| Despliegue actual (GitHub Pages) | `GITHUB_PAGES_QUARTZ.md` | ✅ referencia del sitio en producción |

## 1. Tema minimalista — `quartz-theme/wrlab-minimal.css`

Papel limpio, un acento (oro Wild Rift `#c8aa6e`), tipografía del sistema (cero peticiones
externas), tablas densas legibles (los reportes son tabla-intensivos), callouts
`[!NOTE]/[!TIP]/[!WARNING]/[!DANGER]` con colores semánticos suaves, dark mode automático
y estilos de impresión. Zonas comentadas (1 variables · 2 base · 3 tipografía · 4 tablas ·
5 callouts · 6 código · 7 navegación · 8 dark · 9 utilidades).

**Instalación:** copiar al vault (p. ej. `quartz/styles/wrlab-minimal.css`) e importar según
el esquema de tu Quartz (v4: `@import` en `quartz/styles/custom.scss`; v5: clave de estilos
personalizados del YAML). Selectores sobre las clases estables de Quartz (`.callout`,
`article`, `table`, `#explorer-content`…); si tu build renombró alguna, ajusta el selector.
El CSS es portable: si el sitio migra a Next.js (ver plan), las variables y reglas se
re-mapean componente a componente sin rediseñar.

## 2. Win rates en los callouts (core del lab desde v1.11 oficial)

La fuente de verdad es `data/estructurada/champion_winrates.csv/.md` (por rol, Diamond+,
con confianza y fecha), refrescada por el vigía 2×/día y manual con `wrlab.py winrates`.
Reglas para reportes (TEMPLATE §A.1): el callout **"Estado Meta Actual"** cita la última
fila del campeón (con su fecha); el lint avisa si un callout publicado diverge >3 pts del
dato actual. Tras cada parche/hotfix el refresco es automático (FRAMEWORK §E).

## 3. Migración del sitio

Seguir `PLAN_MIGRACION_VERCEL.md` (del autor). Del lado del lab, las fases 0-1 piden:
informe de estado (suite verde, artefactos al día) y **backfill de frontmatter** de los
reportes al esquema del contrato (`champion/slug/role/patch/version/status/archetype/
published_at`) — hoy el lab deriva champion/rol del nombre de archivo y los metadatos,
así que el backfill es automatizable desde `reportes_registry.json` cuando se apruebe.
