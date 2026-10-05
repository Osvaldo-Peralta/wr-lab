---
tags:
  - Mid
  - Auto
version: 0.9
Status: Espera de verificación
champion: Syndra
slug: syndra-auto-73a
role: mid
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
**Rol principal:** mid (hint del lab — revisar)
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
> Win Rate 51.21 % | Pick 6.84 % | Ban 26.19 % | Tendencia ↑ 2 | **Tier S+** | Rol MID · Diamond + · actualizado 2026-10-04 (champion_winrates.csv)

---

## 0. RESUMEN EJECUTIVO

### Tabla A — BUILD SEMILLA (comunidad, por validar)

| Slot | Ítem | Oro | Rol en la build |
|------|------|-----|-----------------|
| 1 (botas) | **Boots of Mana → ⬆️ Spellslinger's Shoes** (min 10:00, MISMO slot) | 1 200 | 🌐 comunidad (wr-meta) — TODO validar |
| 2 | **Blackfire Torch** | 2 800 | 🌐 comunidad (wr-meta) — TODO validar |
| 3 | **Infinity Orb** | 3 100 | 🌐 comunidad (wr-meta) — TODO validar |
| 4 | **Rabadon's Deathcap** | 3 400 | 🌐 comunidad (wr-meta) — TODO validar |
| 5 | **Morellonomicon** | 2 650 | 🌐 comunidad (wr-meta) — TODO validar |
| 6 | **Oceanid's Trident** | 2 600 | 🌐 comunidad (wr-meta) — TODO validar |

> **Oro total: 16 750 g** (incluye +1 000 del upgrade T2→T3, Ley 0)
> Stats agregados (BD oficial): HP +500 · Armadura +0 · MR +0

### Tabla B — Ruta de compra cronológica (sintetizada con curvas de oro del vault)

| # | Compra | Oro acum. | Minuto típico |
|---|--------|-----------|---------------|
| 1 | Ítem inicial + poción (start) | 500 | ~0:00 |
| 2 | Boots of Mana | 1 700 | ~7:12 |
| 3 | Blackfire Torch | 4 500 | ~9:00 |
| 4 | Infinity Orb | 7 600 | ~11:29 |
| 5 | Rabadon's Deathcap | 11 000 | ~14:25 |
| 6 | Morellonomicon | 13 650 | ~16:55 |
| 7 | Oceanid's Trident | 16 250 | ~19:40 |
| 8 | ⬆️ Spellslinger's Shoes (mismo slot) | 17 250 | ~19:51 |

### Runas · Hechizos · Habilidades

| Categoría | Elección |
|-----------|----------|
| Keystone | **TODO** (verificar meta en juego/wr-meta — la ficha cruda tiene la sugerencia comunitaria) |
| Hechizos | TODO por rol |
| Habilidades | ver §2 (ficha) — **TODO: orden de subida** |

### Resultado del modelo — CÁLCULOS PARCIALES (supuestos en §10)

| Métrica | Pre-7.3a | Post-7.3a | Δ |
|---|---|---|---|
| Armadura total aprox. (nivel 15) | 97 | 97 | +0 |
| EHP físico aprox. | 5 536 | 5 536 | +0.0 % |

---

## 1. CONTEXTO DEL CAMPEÓN EN ESTE PARCHE

### 1.1 Cambios directos (Syndra)

| Cambio |
|--------|
| **Syndra** · NERF · Nodos de pasiva 40/60/80/100/120→**50/75/100/125/150** · W ratio 60→**50 %** · slow fijo **25 %** |

### 1.2 Cambios sistémicos relevantes (mid)

| Sistema |
|---------|
| Sin cambios sistémicos relevantes al rol. |

### 1.3 ¿Escala con crítico/otro stat? — **TODO humano** (leer kit en §2)

## 2. FICHA MATEMÁTICA (datos del lab)

| Parámetro | Valor | Fuente |
|---|---|---|
| AS ratio / base / bonus / por nivel | 0.625,0.625,0.2,0.015 | champion_attack_speed_7.3.csv |
| Bases nivel 15 | HP 2310 · Armadura 97 · MR 53 (nivel 15, ficha wr-meta) |
| Kit (habilidades con valores) | ver ficha `data/estructurada/campeones/syndra.md` | wr-meta (crudo en data/raw/campeones/) |
| Cambios 7.3/7.3a | ver §1.1 | diffs oficiales verificados contra nota EN |

## 3. MODELO Y FÓRMULAS

**Sin motor cuantitativo** (ROADMAP: motor de tanques/magos). Cálculos parciales de §0/§8:
EHP = (HP base ficha + HP ítems) × (1 + armadura/100). Supuestos en §10.

## 4. LEYES APLICADAS A SYNDRA (formato compacto — estándar v1.13.1)

- **Ley 0 — Slots:** semilla de 6 slots; validada (1 botas + 5 ítems) con upgrade T2→T3 añadido (+1 000 g, mismo slot).
- **Ley 3b — Exclusividades:** sin conflictos (items_exclusivos.csv) ✅.
- **Ley 1/2 — Crítico/AS:** TODO (el arquetipo no prioriza crítico; verificar AS útil del kit).
- **Ley 4 — Stats muertos:** TODO humano con el kit en §2.
- **Ley 5/6 — Eficiencia/timing:** ruta de §0 (curvas del vault); TODO validar recalls.
- **Ley 7 — Sistemas:** ver §1.2.

## 5. ANÁLISIS DEL PRIMER ÍTEM

Semilla wr-meta: Boots of Mana — **TODO humano:** validar
contra el meta 7.3a y el clear de jungla (smite nerf) si aplica.

## 6. BUILD FINAL RANURA POR RANURA

**TODO humano:** justificación por slot. Alternativas de la BD oficial para la matriz situacional:

| Ítem alternativo | Motivo |
|---|---|
| Titanic Hydra | **TODO numérico** (sin motor para el arquetipo — ROADMAP) |
| Overlord's Bloodmail | **TODO numérico** (sin motor para el arquetipo — ROADMAP) |
| Guardian Angel | **TODO numérico** (sin motor para el arquetipo — ROADMAP) |
| Sterak's Gage | **TODO numérico** (sin motor para el arquetipo — ROADMAP) |
| Death's Dance | **TODO numérico** (sin motor para el arquetipo — ROADMAP) |
| Nashor's Tooth | **TODO numérico** (sin motor para el arquetipo — ROADMAP) |

## 7. RUNAS · HECHIZOS · HABILIDADES

**TODO humano.** La ficha cruda (`data/estructurada/campeones/syndra.md`, sección
"Build/runas populares") trae la sugerencia comunitaria de runas como insumo.

## 8. COMPARACIÓN CONTRA LAS ALTERNATIVAS

Comparación cuantitativa de builds: **PENDIENTE del motor del arquetipo** (ROADMAP).
Con datos de 7.3a (supuestos §10):

| Métrica | 📌 Pre-7.3a | 🔬 LAB post-7.3a | Δ |
|---|---|---|---|
| Armadura total aprox. (nivel 15) | 97 | 97 | +0 |
| EHP físico aprox. | 5 536 | 5 536 | +0.0 % |

> **TODO:** al existir el motor, re-optimizar y marcar fuentes (⭐ LAB / 📌 publicada / 🌐 comunidad).

## 9. PLAN DE JUEGO

**TODO humano.** Picos de §0 Tabla B. 

## 10. VERIFICACIONES, DISCREPANCIAS Y SUPUESTOS

- **Fuentes:** ficha wr-meta (syndra) + apéndice AS oficial 7.3 · diffs cambios_*.md
  (verificados contra nota EN oficial) · items_7.3.csv · champion_winrates.csv
  (2026-10-04) · build semilla: popular wr-meta (página con contenido mixto 2025-07/2026-07 — filtrada contra BD 7.3).
- **Supuestos DECLARADOS:** bases nivel 15 de la ficha wr-meta;
  EHP sin escudos/activas.
  **Verificar en juego antes de publicar.**
- **Validación:** Ley 0 y 3b chequeadas · win rates del pipeline oficial.

## APÉNDICE A — POOL DEL ROL: veredicto automático

Alternativas del §6 (BD oficial) — veredictos numéricos pendientes del motor.

## APÉNDICE B — RUTAS DE COMPRA

Tabla B de §0 (sintetizada con curvas del vault, rol mid).

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
