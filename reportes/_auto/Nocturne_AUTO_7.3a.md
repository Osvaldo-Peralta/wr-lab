---
tags:
  - Jungla
  - Auto
version: 0.9
Status: Espera de verificación
champion: Nocturne
slug: nocturne-auto-73a
role: jungla
variant: auto-7-3a
patch: "7.3a"
archetype: "sin motor cuantitativo — generación cualitativa (tanque/mago/asesino)"
engine: none
custom: false
generate: auto
mode: sr
published_at: "2026-10-04"
updated_at: "2026-10-04"
verification: pending
---
**Fecha del análisis:** 04/10/2026 (auto-generado, modo cualitativo)
**Parche:** 7.3 (21-sep-2026) + hotfix 7.3a
**Rol principal:** jungla (hint del lab — revisar)
**Arquetipo:** sin motor cuantitativo (motores de tanques/magos/asesinos: ROADMAP). Método:
datos reales (ficha wr-meta, diffs oficiales, win rates, BD de ítems) + cálculos parciales
con supuestos declarados + TODOs explícitos.
**Enfoque:** semilla comunitaria filtrada contra la BD 7.3 — TODO validar en juego.

> [!WARNING] REPORTE AUTO-GENERADO (MODO CUALITATIVO) — ESPERA DE VERIFICACIÓN
> Generado por `model/generate_report.py` el 04/10/2026. Este campeón no tiene
> motor cuantitativo en el lab: las secciones de daño por build llevan **TODO**; los cálculos
> incluidos (EHP) usan supuestos DECLARADOS en §10.
> La build es la popular de wr-meta filtrada (la página mezcla contenido de varias fechas — descartados los ítems fuera de la BD 7.3): VALIDAR EN JUEGO. El autor debe completar TODOs, verificar en juego y `aprobar` (o regenerar a mano).

> [!NOTE]
> **Estado Meta Actual (2026-10-04):**
> Win Rate 55.46 % | Pick 9.57 % | Ban 37.99 % | Tendencia ↓ 1 | **Tier S+** | Rol JUNGLE · Diamond + · actualizado 2026-10-04 (champion_winrates.csv)

---

## 0. RESUMEN EJECUTIVO

### Tabla A — BUILD SEMILLA (comunidad, por validar)

| Slot | Ítem | Oro | Rol en la build |
|------|------|-----|-----------------|
| 1 (botas) | **Boots of Dynamism → ⬆️ Armorcrusher Boots** (min 10:00, MISMO slot) | 1 200 | 🌐 comunidad (wr-meta) — TODO validar |
| 2 | **Duskblade of Draktharr** | 3 000 | 🌐 comunidad (wr-meta) — TODO validar |
| 3 | **Trinity Force** | 3 333 | 🌐 comunidad (wr-meta) — TODO validar |
| 4 | **Serylda's Grudge** | 3 100 | 🌐 comunidad (wr-meta) — TODO validar |
| 5 | **Serpent's Fang** | 2 800 | 🌐 comunidad (wr-meta) — TODO validar |
| 6 | **Guardian Angel** | 3 200 | 🌐 comunidad (wr-meta) — TODO validar |

> **Oro total: 17 633 g** (incluye +1 000 del upgrade T2→T3, Ley 0)
> Stats agregados (BD oficial): HP +333 · Armadura +50 · MR +0

### Tabla B — Ruta de compra cronológica (sintetizada con curvas de oro del vault)

| # | Compra | Oro acum. | Minuto típico |
|---|--------|-----------|---------------|
| 1 | Ítem inicial + poción (start) | 500 | ~0:00 |
| 2 | Boots of Dynamism | 1 700 | ~4:30 |
| 3 | Duskblade of Draktharr | 4 700 | ~8:21 |
| 4 | Trinity Force | 8 033 | ~9:56 |
| 5 | Serylda's Grudge | 11 133 | ~13:41 |
| 6 | Serpent's Fang | 13 933 | ~16:02 |
| 7 | Guardian Angel | 17 133 | ~18:42 |
| 8 | ⬆️ Armorcrusher Boots (mismo slot) | 18 133 | ~10:00 |

### Runas · Hechizos · Habilidades

| Categoría | Elección |
|-----------|----------|
| Keystone | **TODO** (verificar meta en juego/wr-meta — la ficha cruda tiene la sugerencia comunitaria) |
| Hechizos | Smite + Flash (jungla) |
| Habilidades | ver §2 (ficha) — **TODO: orden de subida** |

### Resultado del modelo — CÁLCULOS PARCIALES (supuestos en §10)

| Métrica | Pre-7.3a | Post-7.3a | Δ |
|---|---|---|---|
| Armadura total aprox. (nivel 15) | 156 | 156 | +0 |
| EHP físico aprox. | 7 345 | 7 345 | +0.0 % |

---

## 1. CONTEXTO DEL CAMPEÓN EN ESTE PARCHE

### 1.1 Cambios directos (Nocturne)

| Cambio |
|--------|
| Sin cambios directos encontrados en los diffs del lab. |

### 1.2 Cambios sistémicos relevantes (jungla)

| Sistema |
|---------|
| Smite burn vs monstruos: 30–198/s → **22–162/s** → Jungla early más lenta → Diana jungla: Nashor's 1.º aún más correcto; Shyvana/Volibear/Cho'Gath jungla: clear early −15-20 % |

### 1.3 ¿Escala con crítico/otro stat? — **TODO humano** (leer kit en §2)

## 2. FICHA MATEMÁTICA (datos del lab)

| Parámetro | Valor | Fuente |
|---|---|---|
| AS ratio / base / bonus / por nivel | 0.721,0.721,0.11,0.024 | champion_attack_speed_7.3.csv |
| Bases nivel 15 | HP 2536 · Armadura 106 · MR 68 (nivel 15, ficha wr-meta) |
| Kit (habilidades con valores) | ver ficha `data/estructurada/campeones/nocturne.md` | wr-meta (crudo en data/raw/campeones/) |
| Cambios 7.3/7.3a | ver §1.1 | diffs oficiales verificados contra nota EN |

## 3. MODELO Y FÓRMULAS

**Sin motor cuantitativo** (ROADMAP: motor de tanques/magos). Cálculos parciales de §0/§8:
EHP = (HP base ficha + HP ítems) × (1 + armadura/100). Supuestos en §10.

## 4. LEYES APLICADAS A NOCTURNE (formato compacto — estándar v1.13.1)

- **Ley 0 — Slots:** semilla de 6 slots; validada (1 botas + 5 ítems) con upgrade T2→T3 añadido (+1 000 g, mismo slot).
- **Ley 3b — Exclusividades:** sin conflictos (items_exclusivos.csv) ✅.
- **Ley 1/2 — Crítico/AS:** TODO (el arquetipo no prioriza crítico; verificar AS útil del kit).
- **Ley 4 — Stats muertos:** TODO humano con el kit en §2.
- **Ley 5/6 — Eficiencia/timing:** ruta de §0 (curvas del vault); TODO validar recalls.
- **Ley 7 — Sistemas:** ver §1.2.

## 5. ANÁLISIS DEL PRIMER ÍTEM

Semilla wr-meta: Boots of Dynamism — **TODO humano:** validar
contra el meta 7.3a y el clear de jungla (smite nerf) si aplica.

## 6. BUILD FINAL RANURA POR RANURA

**TODO humano:** justificación por slot. Alternativas de la BD oficial para la matriz situacional:

| Ítem alternativo | Motivo |
|---|---|
| Titanic Hydra | **TODO numérico** (sin motor para el arquetipo — ROADMAP) |
| Overlord's Bloodmail | **TODO numérico** (sin motor para el arquetipo — ROADMAP) |
| Sterak's Gage | **TODO numérico** (sin motor para el arquetipo — ROADMAP) |
| Death's Dance | **TODO numérico** (sin motor para el arquetipo — ROADMAP) |
| Banshee's Veil | **TODO numérico** (sin motor para el arquetipo — ROADMAP) |
| Zhonya's Hourglass | **TODO numérico** (sin motor para el arquetipo — ROADMAP) |

## 7. RUNAS · HECHIZOS · HABILIDADES

**TODO humano.** La ficha cruda (`data/estructurada/campeones/nocturne.md`, sección
"Build/runas populares") trae la sugerencia comunitaria de runas como insumo.

## 8. COMPARACIÓN CONTRA LAS ALTERNATIVAS

Comparación cuantitativa de builds: **PENDIENTE del motor del arquetipo** (ROADMAP).
Con datos de 7.3a (supuestos §10):

| Métrica | 📌 Pre-7.3a | 🔬 LAB post-7.3a | Δ |
|---|---|---|---|
| Armadura total aprox. (nivel 15) | 156 | 156 | +0 |
| EHP físico aprox. | 7 345 | 7 345 | +0.0 % |

> **TODO:** al existir el motor, re-optimizar y marcar fuentes (⭐ LAB / 📌 publicada / 🌐 comunidad).

## 9. PLAN DE JUEGO

**TODO humano.** Picos de §0 Tabla B. Ajustar por smite nerf (jungla).

## 10. VERIFICACIONES, DISCREPANCIAS Y SUPUESTOS

- **Fuentes:** ficha wr-meta (nocturne) + apéndice AS oficial 7.3 · diffs cambios_*.md
  (verificados contra nota EN oficial) · items_7.3.csv · champion_winrates.csv
  (2026-10-04) · build semilla: popular wr-meta (página con contenido mixto 2025-07/2026-07 — filtrada contra BD 7.3).
- **Supuestos DECLARADOS:** bases nivel 15 de la ficha wr-meta;
  EHP sin escudos/activas.
  **Verificar en juego antes de publicar.**
- **Validación:** Ley 0 y 3b chequeadas · win rates del pipeline oficial.

## APÉNDICE A — POOL DEL ROL: veredicto automático

Alternativas del §6 (BD oficial) — veredictos numéricos pendientes del motor.

## APÉNDICE B — RUTAS DE COMPRA

Tabla B de §0 (sintetizada con curvas del vault, rol jungla).

---

## Pie de página

*Reporte AUTO-GENERADO (modo cualitativo) el 04/10/2026 con datos del parche 7.3 +
7.3a (verificados contra nota EN oficial el 29/09/2026). WR-LAB v1.15. Estado: **Espera de
verificación** — no publicar hasta aprobación del autor. Cálculos parciales con supuestos
declarados en §10.*

**Referencias y créditos**

- Notas oficiales del parche 7.3 y hotfix 7.3a — © Riot Games, Inc. (wildrift.leagueoflegends.com).
- Ficha, build popular y win rates — wr-meta.com (proyecto comunitario), Diamond+ del 2026-10-04.
- Modelo, Leyes 0-7 y validaciones — WR-LAB (`model/generate_report.py`, modo cualitativo).

**Aviso legal:** Wild Rift y League of Legends son marcas registradas de Riot Games, Inc.
Este documento es una guía de comunidad con fines educativos, **no está afiliada, patrocinada
ni respaldada por Riot Games**.
